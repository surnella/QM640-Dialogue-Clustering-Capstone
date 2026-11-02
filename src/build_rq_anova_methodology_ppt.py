"""
Generate a standalone, 100% native editable 5-slide PowerPoint deck:
  final/QM_640_RQ_Text_to_ANOVA_Methodology_Reference.pptx

Purpose:
  Reference / backup slides for the defense evaluation committee illustrating
  the exact step-by-step sequence of how chatbot text requests and responses
  are injected with experimental conditions, converted into numerical scores,
  shaped for normality vs. skewness, and analyzed via triangulated ("bulletproof")
  ANOVA variations across RQ1–RQ4:
    - Slide 1: General 4-Stage Text-to-ANOVA Pipeline & Bulletproof Inference Architecture
    - Slide 2: RQ1 Step-by-Step Sequence (Clustering & Prefix Routing Text-to-ANOVA)
    - Slide 3: RQ2 Step-by-Step Sequence (Repeated-Measures Prompt Injection & Style/Pacing ANOVA)
    - Slide 4: RQ3 Step-by-Step Sequence (2x2 Factorial Rule/Prompt Injection & Bounded-Rate ANOVA)
    - Slide 5: RQ4 Step-by-Step Sequence (2x3 Closed-Loop Multi-Turn Simulation & Turn-Economy ANOVA)

Does NOT modify any existing report (.docx, .pdf) or existing .pptx files.
"""

import os
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PPTX = os.path.join(ROOT, "final", "QM_640_RQ_Text_to_ANOVA_Methodology_Reference.pptx")


def rgb(hex_str):
    h = hex_str.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def set_line_dash(shape, dash="dash"):
    ln = shape.line._get_or_add_ln()
    prstDash = OxmlElement("a:prstDash")
    prstDash.set("val", dash)
    ln.append(prstDash)


def add_arrow_head(line_or_connector, head_end=True, tail_end=False):
    ln = line_or_connector.line._get_or_add_ln()
    if tail_end:
        head = OxmlElement("a:headEnd")
        head.set("type", "triangle")
        head.set("w", "med")
        head.set("len", "med")
        ln.append(head)
    if head_end:
        tail = OxmlElement("a:tailEnd")
        tail.set("type", "triangle")
        tail.set("w", "med")
        tail.set("len", "med")
        ln.append(tail)


def add_header(slide, badge_text, title_text, subtitle_text):
    hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.82))
    hdr.fill.solid()
    hdr.fill.fore_color.rgb = rgb("#1B365D")
    hdr.line.fill.background()

    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.25), Inches(0.12), Inches(2.55), Inches(0.24))
    badge.adjustments[0] = 0.25
    badge.fill.solid()
    badge.fill.fore_color.rgb = rgb("#008080")
    badge.line.fill.background()
    tf_b = badge.text_frame
    tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_b = tf_b.paragraphs[0]
    p_b.alignment = PP_ALIGN.CENTER
    r_b = p_b.add_run()
    r_b.text = badge_text
    r_b.font.name = "Calibri"
    r_b.font.size = Pt(8.5)
    r_b.font.bold = True
    r_b.font.color.rgb = rgb("#FFFFFF")

    tb = slide.shapes.add_textbox(Inches(2.90), Inches(0.06), Inches(10.20), Inches(0.42))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = title_text
    r.font.name = "Calibri"
    r.font.size = Pt(15.5)
    r.font.bold = True
    r.font.color.rgb = rgb("#FFFFFF")

    tb2 = slide.shapes.add_textbox(Inches(0.25), Inches(0.45), Inches(12.85), Inches(0.32))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    r2 = p2.add_run()
    r2.text = subtitle_text
    r2.font.name = "Calibri"
    r2.font.size = Pt(10.0)
    r2.font.italic = True
    r2.font.color.rgb = rgb("#B3E5FC")


def add_stage_banner(slide, left, top, width, height, step_label, title, bg_hex, border_hex):
    sh = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(height),
    )
    sh.adjustments[0] = 0.02
    sh.fill.solid()
    sh.fill.fore_color.rgb = rgb(bg_hex)
    sh.line.color.rgb = rgb(border_hex)
    sh.line.width = Pt(1.75)

    hdr = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(0.34),
    )
    hdr.adjustments[0] = 0.08
    hdr.fill.solid()
    hdr.fill.fore_color.rgb = rgb(border_hex)
    hdr.line.fill.background()
    tf = hdr.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.08)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r1 = p.add_run()
    r1.text = f"{step_label}: "
    r1.font.name = "Calibri"
    r1.font.size = Pt(9.5)
    r1.font.bold = True
    r1.font.color.rgb = rgb("#FFF59D")
    r2 = p.add_run()
    r2.text = title
    r2.font.name = "Calibri"
    r2.font.size = Pt(9.5)
    r2.font.bold = True
    r2.font.color.rgb = rgb("#FFFFFF")
    return sh


def add_card(
    slide, left, top, width, height, title, bullets,
    bg_hex="#FFFFFF", border_hex="#1565C0", title_hex=None,
    shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, font_size=8.0, dashed=False,
):
    sh = slide.shapes.add_shape(
        shape_type, Inches(left), Inches(top), Inches(width), Inches(height),
    )
    if shape_type == MSO_SHAPE.ROUNDED_RECTANGLE:
        sh.adjustments[0] = 0.04
    sh.fill.solid()
    sh.fill.fore_color.rgb = rgb(bg_hex)
    sh.line.color.rgb = rgb(border_hex)
    sh.line.width = Pt(1.35)
    if dashed:
        set_line_dash(sh, "dash")

    tf = sh.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Inches(0.07)
    tf.margin_right = Inches(0.07)
    tf.margin_top = Inches(0.05)
    tf.margin_bottom = Inches(0.04)

    if title:
        p0 = tf.paragraphs[0]
        p0.alignment = PP_ALIGN.LEFT
        p0.space_after = Pt(2.0)
        r0 = p0.add_run()
        r0.text = title
        r0.font.name = "Calibri"
        r0.font.size = Pt(font_size + 0.9)
        r0.font.bold = True
        r0.font.color.rgb = rgb(title_hex or border_hex)
        first_used = True
    else:
        first_used = False

    for b in bullets:
        p = tf.add_paragraph() if first_used else tf.paragraphs[0]
        first_used = True
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(1.4)
        if isinstance(b, tuple):
            prefix, rest, col = b
            r1 = p.add_run()
            r1.text = prefix
            r1.font.name = "Calibri"
            r1.font.size = Pt(font_size)
            r1.font.bold = True
            r1.font.color.rgb = rgb(col)
            r2 = p.add_run()
            r2.text = rest
            r2.font.name = "Calibri"
            r2.font.size = Pt(font_size)
            r2.font.color.rgb = rgb("#212121")
        else:
            r = p.add_run()
            r.text = b
            r.font.name = "Calibri"
            r.font.size = Pt(font_size)
            r.font.color.rgb = rgb("#212121")
    return sh


def add_flow_arrow(slide, left, top, width=0.22, height=0.36, color_hex="#1B365D", direction="right"):
    shape_map = {
        "right": MSO_SHAPE.RIGHT_ARROW,
        "down": MSO_SHAPE.DOWN_ARROW,
        "up": MSO_SHAPE.UP_ARROW,
    }
    arr = slide.shapes.add_shape(
        shape_map[direction], Inches(left), Inches(top), Inches(width), Inches(height),
    )
    arr.fill.solid()
    arr.fill.fore_color.rgb = rgb(color_hex)
    arr.line.fill.background()
    return arr


def add_bottom_banner(slide, text, bg_hex="#FFF8E1", border_hex="#F57F17", text_hex="#1B365D"):
    box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.22), Inches(6.55), Inches(12.89), Inches(0.80),
    )
    box.adjustments[0] = 0.04
    box.fill.solid()
    box.fill.fore_color.rgb = rgb(bg_hex)
    box.line.color.rgb = rgb(border_hex)
    box.line.width = Pt(1.6)
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.12)
    tf.margin_right = Inches(0.12)
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = text
    r.font.name = "Calibri"
    r.font.size = Pt(8.8)
    r.font.bold = True
    r.font.color.rgb = rgb(text_hex)
    return box


def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: GENERAL 4-STAGE TEXT-TO-ANOVA PIPELINE & METHODOLOGY OVERVIEW
    # =========================================================================
    s1 = prs.slides.add_slide(blank)
    add_header(
        s1,
        "REFERENCE SLIDE 1 OF 5",
        "General Methodology: How Chatbot Text Requests & Responses Become ANOVA-Ready",
        "Universal 4-Stage Sequence across RQ1–RQ4: Separating Golden Training from Held-Out Testing, Text-to-Numeric Scoring, and 3-Tier 'Bulletproof' ANOVA",
    )

    col_w = 2.98
    col_h = 5.45
    y_top = 0.96
    xs = [0.22, 3.52, 6.82, 10.12]

    # Stage 1
    add_stage_banner(s1, xs[0], y_top, col_w, col_h, "STAGE 1", "Golden vs. Test Split & Input", "#F0F4F8", "#1B365D")
    add_card(
        s1, xs[0] + 0.10, y_top + 0.42, col_w - 0.20, 1.55,
        "1A. Strict Train / Test Separation",
        [
            ("• Golden Discovery Set (D_gold, n = 933): ", "70% split used ONLY offline to fit K-Means centroids, train the Blocks prefix router, build FAISS exemplar sub-indices, and compute human word norms.", "#1B365D"),
            ("• Held-Out Test Set (D_test, n = 401): ", "30% unseen dialogues used exclusively to generate test requests x_i.", "#00695C"),
        ],
        bg_hex="#FFFFFF", border_hex="#1B365D", font_size=7.7,
    )
    add_flow_arrow(s1, xs[0] + 1.35, y_top + 2.02, width=0.28, height=0.22, color_hex="#1B365D", direction="down")
    add_card(
        s1, xs[0] + 0.10, y_top + 2.28, col_w - 0.20, 1.45,
        "1B. Held-Out Customer Request (x_i)",
        [
            ("• Input Prefix Text: ", "Unseen customer utterances (e.g., origin, destination, dates, budget, questions).", "#1B365D"),
            ("• Structured Context State: ", "Active slot ledger S_i and seeded Tier-2 enterprise policy state (in RQ3/RQ4).", "#1B365D"),
        ],
        bg_hex="#E3F2FD", border_hex="#1565C0", font_size=7.7,
    )
    add_flow_arrow(s1, xs[0] + 1.35, y_top + 3.78, width=0.28, height=0.22, color_hex="#1B365D", direction="down")
    add_card(
        s1, xs[0] + 0.10, y_top + 4.04, col_w - 0.20, 1.28,
        "Why This Prevents Data Leakage",
        [
            ("• Zero Overlap: ", "Test dialogues never appear in the FAISS retrieval pool or router training set.", "#1B5E20"),
            ("• Identical Seed (seed = 42): ", "Guarantees deterministic, replicable sampling across cells.", "#1B5E20"),
        ],
        bg_hex="#E8F5E9", border_hex="#2E7D32", font_size=7.7,
    )

    add_flow_arrow(s1, 3.23, 3.45, width=0.25, height=0.38, color_hex="#1B365D", direction="right")

    # Stage 2
    add_stage_banner(s1, xs[1], y_top, col_w, col_h, "STAGE 2", "Prompt Condition Injection", "#E0F2F1", "#00695C")
    add_card(
        s1, xs[1] + 0.10, y_top + 0.42, col_w - 0.20, 1.65,
        "2A. Controlled Prompt Assembly P(x_i, c)",
        [
            ("• Base Context Kept Constant: ", "Customer request x_i and LLM engine (gemini-2.5-flash, temp = 0.2) are held fixed.", "#00695C"),
            ("• Experimental Factor c Injected: ", "Only the treatment factor changes across conditions (e.g., Zero-Shot vs. Static FAISS vs. Cluster-Adaptive + Rules).", "#00695C"),
        ],
        bg_hex="#FFFFFF", border_hex="#00695C", font_size=7.7,
    )
    add_flow_arrow(s1, xs[1] + 1.35, y_top + 2.12, width=0.28, height=0.22, color_hex="#00695C", direction="down")
    add_card(
        s1, xs[1] + 0.10, y_top + 2.38, col_w - 0.20, 1.42,
        "2B. Chatbot Text Generation (ŷ_i,c)",
        [
            ("• Single-Turn Reply (RQ2, RQ3): ", "Chatbot outputs natural-language response ŷ_i,c to the test prompt.", "#00695C"),
            ("• Multi-Turn Transcript (RQ4): ", "Closed-loop turn-by-turn text exchange until [ACCEPT_BOOKING].", "#00695C"),
        ],
        bg_hex="#E0F2F1", border_hex="#00695C", font_size=7.7,
    )
    add_flow_arrow(s1, xs[1] + 1.35, y_top + 3.85, width=0.28, height=0.22, color_hex="#00695C", direction="down")
    add_card(
        s1, xs[1] + 0.10, y_top + 4.10, col_w - 0.20, 1.22,
        "Experimental Designs Used",
        [
            ("• Within-Subjects (RQ1 seeds, RQ2): ", "Same test unit runs through all conditions (removes baseline unit noise).", "#1B365D"),
            ("• Factorial (RQ3 2×2, RQ4 2×3): ", "Tests main effects A, B and interaction A×B.", "#1B365D"),
        ],
        bg_hex="#FFF8E1", border_hex="#F57F17", font_size=7.6,
    )

    add_flow_arrow(s1, 6.53, 3.45, width=0.25, height=0.38, color_hex="#00695C", direction="right")

    # Stage 3
    add_stage_banner(s1, xs[2], y_top, col_w, col_h, "STAGE 3", "Text-to-Numeric & Distribution", "#F3E5F5", "#6A1B9A")
    add_card(
        s1, xs[2] + 0.10, y_top + 0.42, col_w - 0.20, 2.28,
        "3A. Four Deterministic Scorers g(ŷ_i,c) → Y_i,c",
        [
            ("1. Vector Cosine Similarity ([-1, 1]): ", "De-lexicalizes entities ([CITY], [PRICE]), embeds text via MiniLM (384-d) or Gemini (3,072-d), takes dot product u·v.", "#6A1B9A"),
            ("2. Word Pacing Error (≥ 0 words): ", "|Words(ŷ_i,c) − μ_Words(target archetype)|.", "#6A1B9A"),
            ("3. Set / Regex Proportions ([0, 1]): ", "Exact Python string/set checks for Rule Adherence (RAR), Foreign Entity Leakage (ELR), Slot F1, and Redundant Questions (RER).", "#6A1B9A"),
            ("4. Turn Counts (T ≥ 5) & Log Turns: ", "Total messages to package agreement & ln(T).", "#6A1B9A"),
        ],
        bg_hex="#FFFFFF", border_hex="#6A1B9A", font_size=7.4,
    )
    add_flow_arrow(s1, xs[2] + 1.35, y_top + 2.74, width=0.28, height=0.22, color_hex="#6A1B9A", direction="down")
    add_card(
        s1, xs[2] + 0.10, y_top + 3.00, col_w - 0.20, 2.32,
        "3B. Normal vs. Skewed / Bounded Handling",
        [
            ("• Unimodal Cosines (Normal): ", "Continuous averages over 384–3,072 dims; CLT stabilizes cell means.", "#1B365D"),
            ("• Right-Skewed Counts (Turns/Words): ", "Natural log transform Y = ln(Turns) compresses right tail & stabilizes variance.", "#E65100"),
            ("• Bounded [0, 1] Floor/Ceiling Zeros: ", "When Rules Active drives leakage/RER to .000 (SD = .000), cell variances become unequal (heteroscedastic) → requires Tier 2 & Tier 3 tests in Stage 4!", "#C62828"),
        ],
        bg_hex="#EDE7F6", border_hex="#5E35B1", font_size=7.4,
    )

    add_flow_arrow(s1, 9.83, 3.45, width=0.25, height=0.38, color_hex="#6A1B9A", direction="right")

    # Stage 4
    add_stage_banner(s1, xs[3], y_top, col_w, col_h, "STAGE 4", "Variance & 'Bulletproof' ANOVA", "#E8F5E9", "#2E7D32")
    add_card(
        s1, xs[3] + 0.10, y_top + 0.42, col_w - 0.20, 1.72,
        "4A. How ANOVA Computes & Compares Variances",
        [
            ("• Signal (MS_Between): ", "Variance of group/cell means around grand mean = SS_Effect / df_Effect.", "#2E7D32"),
            ("• Noise (MS_Within / Error): ", "Pooled variance of individual dialogues around their own cell mean = SS_Error / df_Error.", "#2E7D32"),
            ("• F-Statistic & Effect Size: ", "F = MS_Between / MS_Within; Partial ηp² = SS_Effect / (SS_Effect + SS_Error).", "#1B365D"),
        ],
        bg_hex="#FFFFFF", border_hex="#2E7D32", font_size=7.4,
    )
    add_flow_arrow(s1, xs[3] + 1.35, y_top + 2.18, width=0.28, height=0.22, color_hex="#2E7D32", direction="down")
    add_card(
        s1, xs[3] + 0.10, y_top + 2.44, col_w - 0.20, 2.88,
        "4B. 3-Tier 'Bulletproof' ANOVA Triangulation",
        [
            ("Tier 1 — Parametric ANOVA: ", "One-Way OLS (RQ1), Greenhouse–Geisser Sphericity-Corrected RM-ANOVA (RQ2), and Two-Way OLS Factorial ANOVA (RQ3, RQ4).", "#1565C0"),
            ("Tier 2 — Heteroscedasticity-Robust ANOVA: ", "Welch's ANOVA (RQ1) & MacKinnon–White HC3 Sandwich Variance (RQ3, RQ4)—valid even when zero-leakage cells have SD = .000!", "#E65100"),
            ("Tier 3 — Non-Parametric Rank ANOVA: ", "Kruskal–Wallis H (RQ1), Friedman χ² (RQ2), and Aligned Rank Transform (ART) Factorial ANOVA (RQ3, RQ4)—converts skewed scores to ranks 1..N so skewness cannot distort p-values!", "#1B5E20"),
        ],
        bg_hex="#C8E6C9", border_hex="#1B5E20", font_size=7.3,
    )

    add_bottom_banner(
        s1,
        "Key Defense Takeaway: Every RQ converts raw text into deterministic numbers via Python/vector scorers (metrics.py) and requires 100% concordance across Parametric (OLS/GG), Heteroscedasticity-Robust (Welch/HC3), and Distribution-Free Rank (ART/Friedman/Kruskal) ANOVAs before rejecting H0.",
    )

    # =========================================================================
    # SLIDE 2: RQ1 STEP-BY-STEP FLOWCHART
    # =========================================================================
    s2 = prs.slides.add_slide(blank)
    add_header(
        s2,
        "RQ1 METHODOLOGY (SLIDE 2 OF 5)",
        "RQ1 Step-by-Step: From Raw Dialogue Text to Archetype Clustering & Routing ANOVA",
        "How customer utterances are annotated via LLM schema, embedded into 46-d 'Blocks' vectors, scored by Cosine Silhouette, and tested across N = 159 runs",
    )

    add_stage_banner(s2, xs[0], y_top, col_w, col_h, "STEP 1", "Dialogue Text & LLM Codebook Input", "#F0F4F8", "#1B365D")
    add_card(
        s2, xs[0] + 0.10, y_top + 0.42, col_w - 0.20, 2.35,
        "1A. Corpus Split & Prefix Truncation",
        [
            ("• Analytic Sample: ", "1,334 Microsoft Frames human–human travel dialogues (D_gold = 933 discovery; D_test = 401 held-out) + 1,499 MultiWOZ 2.2 dialogues.", "#1B365D"),
            ("• Role & Prefix Filtering: ", "Extracts ONLY customer turns (wizard turns excluded to prevent wizard confounding V = .45) and truncates to the first M = 9 user messages (preventing end-of-chat outcome leakage V = .29).", "#00695C"),
        ],
        bg_hex="#FFFFFF", border_hex="#1B365D", font_size=7.5,
    )
    add_flow_arrow(s2, xs[0] + 1.35, y_top + 2.82, width=0.28, height=0.22, color_hex="#1B365D", direction="down")
    add_card(
        s2, xs[0] + 0.10, y_top + 3.08, col_w - 0.20, 2.24,
        "1B. Dual Text-to-Feature Extraction",
        [
            ("• Path 1 (Semantic Embeddings): ", "User prefix text encoded via all-MiniLM-L6-v2 (384-d) and gemini-embedding-001 (3,072-d → PCA-20).", "#1565C0"),
            ("• Path 2 (LLM Behavioral Codebook): ", "User prefix text fed into gemini-2.5-flash (temp = 0) with 16-field UserBehaviour Pydantic prompt: 10 ordinal (1–5) scales + 3 categorical fields (encoded into 26 cols; κ_w = .87–.96). Fields 14–16 held out for audit.", "#6A1B9A"),
        ],
        bg_hex="#E3F2FD", border_hex="#1565C0", font_size=7.4,
    )

    add_flow_arrow(s2, 3.23, 3.45, width=0.25, height=0.38, color_hex="#1B365D", direction="right")

    add_stage_banner(s2, xs[1], y_top, col_w, col_h, "STEP 2", "Algorithm & Truncation Conditions", "#E0F2F1", "#00695C")
    add_card(
        s2, xs[1] + 0.10, y_top + 0.42, col_w - 0.20, 2.40,
        "2A. Experiment 1A: 3 Clustering Groups (N = 159)",
        [
            ("• 53 Matched Subsamples (n = 500 each): ", "Drawn from D_gold using shared random seeds s = 1..53.", "#00695C"),
            ("• Group 1 — K-Means (k = 3): ", "Partitions 100% of dialogues around 3 centroids.", "#1565C0"),
            ("• Group 2 — Ward Agglomerative (k = 3): ", "Bottom-up variance-minimizing hierarchy.", "#00695C"),
            ("• Group 3 — HDBSCAN (Density): ", "Discards 39.1% (MiniLM) / 35.8% (Gemini turn pool) of dialogues as unclustered noise!", "#C62828"),
            ("• Null Baseline: ", "53 random label-permutation runs.", "#455A64"),
        ],
        bg_hex="#FFFFFF", border_hex="#00695C", font_size=7.4,
    )
    add_flow_arrow(s2, xs[1] + 1.35, y_top + 2.86, width=0.28, height=0.22, color_hex="#00695C", direction="down")
    add_card(
        s2, xs[1] + 0.10, y_top + 3.12, col_w - 0.20, 2.20,
        "2B. Experiment 1B: 46-d 'Blocks' & Prefix Router",
        [
            ("• 46-d Hybrid 'Blocks' Vector X^(9): ", "Concatenates z-scored PCA-20 Gemini user prefix + 26 encoded LLM behavioral columns (weighted 1:2).", "#00695C"),
            ("• Reference Archetypes y^(9) (k = 3): ", "1. Decisive Booker (45.0%), 2. Open Explorer (25.5%), 3. Rigid-Constraint Seeker (29.5%).", "#1B5E20"),
            ("• Prefix Classifiers (m ∈ {3, 5, 7, 9}): ", "Multinomial Logistic Regression trained on D_gold to predict y^(9) on held-out D_test (n = 401).", "#1B365D"),
        ],
        bg_hex="#E0F2F1", border_hex="#00695C", font_size=7.4,
    )

    add_flow_arrow(s2, 6.53, 3.45, width=0.25, height=0.38, color_hex="#00695C", direction="right")

    add_stage_banner(s2, xs[2], y_top, col_w, col_h, "STEP 3", "Conversion to Numeric Metrics", "#F3E5F5", "#6A1B9A")
    add_card(
        s2, xs[2] + 0.10, y_top + 0.42, col_w - 0.20, 2.55,
        "3A. How Cluster Outputs Become Numbers",
        [
            ("1. Cosine Silhouette Score Y_ij ∈ [-1, 1]: ", "For each dialogue i, compares mean intra-cluster cosine distance a(i) to nearest-cluster distance b(i): s(i) = [b(i) − a(i)] / max(a(i), b(i)), averaged across the n = 500 subsample.", "#6A1B9A"),
            ("   • MiniLM Means: ", "K-Means = .147 (.019), Ward = .118 (.040), HDBSCAN = .211 (.044 on 60.9% non-noise), Perm = −.013.", "#1B365D"),
            ("2. Davies–Bouldin Index (DB ↓): ", "Ratio of within-cluster scatter to between-centroid separation (lowest = 2.647 at k = 3 on 46-d Blocks).", "#6A1B9A"),
        ],
        bg_hex="#FFFFFF", border_hex="#6A1B9A", font_size=7.4,
    )
    add_flow_arrow(s2, xs[2] + 1.35, y_top + 3.01, width=0.28, height=0.22, color_hex="#6A1B9A", direction="down")
    add_card(
        s2, xs[2] + 0.10, y_top + 3.26, col_w - 0.20, 2.06,
        "3B. Stability & Routing Agreement Numbers",
        [
            ("3. Bootstrap Stability ARI ∈ [-1, 1]: ", "Adjusted Rand Index across 60 subsamples of D_gold: ARI = .89 in truncation grid (.87 in 6-config ablation).", "#6A1B9A"),
            ("4. Held-Out Prefix Routing Kappa (κ): ", "Chance-corrected agreement with M=9 reference labels y^(9) on D_test: κ = .359 (m=3) → κ = .535 (m=5, 70.1% raw) → κ = .722 (m=7) → κ = .958 (m=9, 97.3% same-feature consistency).", "#1B5E20"),
        ],
        bg_hex="#EDE7F6", border_hex="#5E35B1", font_size=7.4,
    )

    add_flow_arrow(s2, 9.83, 3.45, width=0.25, height=0.38, color_hex="#6A1B9A", direction="right")

    add_stage_banner(s2, xs[3], y_top, col_w, col_h, "STEP 4", "Variance & ANOVA Variations Used", "#E8F5E9", "#2E7D32")
    add_card(
        s2, xs[3] + 0.10, y_top + 0.42, col_w - 0.20, 1.80,
        "4A. Variance Decomposition Across 159 Runs",
        [
            ("• Between-Algorithm Signal (df_1 = 2): ", "MS_Between = Σ 53·(Ȳ_alg − Ȳ_..)^2 / 2.", "#2E7D32"),
            ("• Within-Algorithm Noise (df_2 = 156): ", "MS_Within = ΣΣ (Y_ij − Ȳ_j)^2 / 156 (notice SD differs: .019 KM vs. .044 HDBSCAN!).", "#C62828"),
            ("• Matched-Seed Structure: ", "Seeds s = 1..53 are paired across the 3 algorithms.", "#1B365D"),
        ],
        bg_hex="#FFFFFF", border_hex="#2E7D32", font_size=7.4,
    )
    add_flow_arrow(s2, xs[3] + 1.35, y_top + 2.26, width=0.28, height=0.22, color_hex="#2E7D32", direction="down")
    add_card(
        s2, xs[3] + 0.10, y_top + 2.52, col_w - 0.20, 2.80,
        "4B. 4 'Bulletproof' ANOVA Variations in RQ1",
        [
            ("1. One-Way OLS ANOVA + Tukey HSD: ", "MiniLM F(2, 156) = 91.33, p < .001, η² = .539; Gemini Turn-Pool F = 77.09 (η² = .497); Gemini Doc F = 127.47 (η² = .620).", "#1565C0"),
            ("2. Matched-Seed Repeated-Measures ANOVA: ", "Accounts for shared subsample seeds s = 1..53: F(1.72, 89.30) = 83.04, p < .001, ηp² = .615.", "#00695C"),
            ("3. Welch's Heteroscedastic ANOVA + Games–Howell: ", "Handles unequal run variance (.019 vs .044 SD): Welch F(2, 89.15) = 66.98, p < .001.", "#E65100"),
            ("4. Non-Parametric Kruskal–Wallis & Friedman: ", "Kruskal H(2) = 86.82, p < .001; Paired Friedman χ²(2) = 56.30, p < .001 → Reject H01!", "#1B5E20"),
        ],
        bg_hex="#C8E6C9", border_hex="#1B5E20", font_size=7.2,
    )

    add_bottom_banner(
        s2,
        "RQ1 Defense Summary: Text dialogues are converted to 46-d hybrid 'Blocks' vectors and evaluated via Cosine Silhouette, DB, ARI, and κ. Because algorithm run variances differ (.019 vs. .044) and seeds are matched, we pair One-Way OLS (F=91.33) with Matched RM-ANOVA (F=83.04), Welch (F=66.98), and Friedman (χ²=56.30).",
    )

    # =========================================================================
    # SLIDE 3: RQ2 STEP-BY-STEP FLOWCHART
    # =========================================================================
    s3 = prs.slides.add_slide(blank)
    add_header(
        s3,
        "RQ2 METHODOLOGY (SLIDE 3 OF 5)",
        "RQ2 Step-by-Step: Prompt Injection Across 3 Conditions & Repeated-Measures ANOVA",
        "How the exact same N = 33 held-out dialogues are fed through 3 prompting strategies (99 LLM calls), converted to style/pacing numbers, and tested via RM-ANOVA",
    )

    add_stage_banner(s3, xs[0], y_top, col_w, col_h, "STEP 1", "Held-Out Input & Live Prefix Routing", "#F0F4F8", "#1B365D")
    add_card(
        s3, xs[0] + 0.10, y_top + 0.42, col_w - 0.20, 2.35,
        "1A. Stratified Held-Out Test Sample (N = 33)",
        [
            ("• 33 Unseen Dialogues from D_test: ", "11 Decisive Bookers, 11 Open Explorers, and 11 Rigid-Constraint Seekers (powered at 1−β = .865 for medium effect f = .25).", "#1B365D"),
            ("• Input Dialogue Context (x_i): ", "Multi-turn customer + wizard conversation history up to target turn t, paired with the actual human wizard's next reply y_i* (held out as ground-truth reference).", "#00695C"),
        ],
        bg_hex="#FFFFFF", border_hex="#1B365D", font_size=7.5,
    )
    add_flow_arrow(s3, xs[0] + 1.35, y_top + 2.82, width=0.28, height=0.22, color_hex="#1B365D", direction="down")
    add_card(
        s3, xs[0] + 0.10, y_top + 3.08, col_w - 0.20, 2.24,
        "1B. Early Prefix Routing (M = 5 User Msgs)",
        [
            ("• Runtime Router Input: ", "Only the first M = 5 customer messages (≈ 9 total turns) of dialogue i are fed into RefinedArchetypeRouter (κ = .535, 70.1% accuracy).", "#1565C0"),
            ("• Predicted Archetype ĉ_i: ", "Outputs predicted persona label (Decisive Booker, Open Explorer, or Rigid-Constraint Seeker) + query embedding q_i for FAISS retrieval.", "#6A1B9A"),
        ],
        bg_hex="#E3F2FD", border_hex="#1565C0", font_size=7.5,
    )

    add_flow_arrow(s3, 3.23, 3.45, width=0.25, height=0.38, color_hex="#1B365D", direction="right")

    add_stage_banner(s3, xs[1], y_top, col_w, col_h, "STEP 2", "3 Prompt Conditions on Same Dialogue", "#E0F2F1", "#00695C")
    add_card(
        s3, xs[1] + 0.10, y_top + 0.42, col_w - 0.20, 1.55,
        "Condition 1: Zero-Shot Baseline (33 Calls)",
        [
            ("• Prompt Injected: ", "[Base Travel System Role] + [Active Dialogue Context x_i].", "#455A64"),
            ("• Missing Elements: ", "No few-shot exemplars; no archetype pacing directive (produces verbose 25.45-word generic replies).", "#C62828"),
        ],
        bg_hex="#FFFFFF", border_hex="#455A64", font_size=7.4,
    )
    add_flow_arrow(s3, xs[1] + 1.35, y_top + 2.00, width=0.28, height=0.18, color_hex="#00695C", direction="down")
    add_card(
        s3, xs[1] + 0.10, y_top + 2.20, col_w - 0.20, 1.50,
        "Condition 2: Static Few-Shot (k = 3, 33 Calls)",
        [
            ("• Prompt Injected: ", "[Base Role] + [k = 3 nearest exemplars from ONE global unpartitioned FAISS index] + [Active Context x_i].", "#1565C0"),
            ("• Limitation: ", "Retrieves mismatched persona styles & rigid 14.48-word length regardless of who is talking.", "#C62828"),
        ],
        bg_hex="#E3F2FD", border_hex="#1565C0", font_size=7.4,
    )
    add_flow_arrow(s3, xs[1] + 1.35, y_top + 3.73, width=0.28, height=0.18, color_hex="#00695C", direction="down")
    add_card(
        s3, xs[1] + 0.10, y_top + 3.93, col_w - 0.20, 1.40,
        "Condition 3: Cluster-Adaptive Few-Shot (33 Calls)",
        [
            ("• Combined Treatment Package Injected: ", "[Base Role] + [Routed Archetype Pacing & Style Directive for ĉ_i] + [k = 3 [SLOT]-masked exemplars from Archetype FAISS Sub-Index I_ĉ] + [Context x_i].", "#1B5E20"),
        ],
        bg_hex="#E0F2F1", border_hex="#00695C", font_size=7.4,
    )

    add_flow_arrow(s3, 6.53, 3.45, width=0.25, height=0.38, color_hex="#00695C", direction="right")

    add_stage_banner(s3, xs[2], y_top, col_w, col_h, "STEP 3", "Chatbot Text → Numeric Scores", "#F3E5F5", "#6A1B9A")
    add_card(
        s3, xs[2] + 0.10, y_top + 0.42, col_w - 0.20, 2.55,
        "3A. De-Lexicalized Style Cosine Similarity",
        [
            ("• Step 3.1 — Entity Masking: ", "mask_text_for_style() replaces cities, dates, prices & numbers with [CITY], [DATE], [PRICE], [NUM] in both chatbot reply ŷ_i,c and human reference y_i*.", "#6A1B9A"),
            ("• Step 3.2 — Primary DV (SBERT 384-d Cosine): ", "Y_i,c = cos(MiniLM(ŷ_i,c), MiniLM(y_i*)) → Zero-Shot = .530 (.132), Static = .453 (.169), Cluster-Adaptive = .597 (.086).", "#1B5E20"),
            ("• Step 3.3 — Topical Controls (Gemini & BERTScore): ", "Gemini 3,072-d (.775–.796, p=.200) & BERTScore F1 (.844–.852, p=.243) stay flat because all 3 replies address the same travel topic!", "#1B365D"),
        ],
        bg_hex="#FFFFFF", border_hex="#6A1B9A", font_size=7.3,
    )
    add_flow_arrow(s3, xs[2] + 1.35, y_top + 3.01, width=0.28, height=0.22, color_hex="#6A1B9A", direction="down")
    add_card(
        s3, xs[2] + 0.10, y_top + 3.26, col_w - 0.20, 2.06,
        "3B. Pacing Calibration Error (Words)",
        [
            ("• Formula: ", "Y_i,c^err = |Words(ŷ_i,c) − μ_Words(Gold Archetype)|, where Golden human wizard norms are 12.9w (Decisive), 18.6w (Explorer), 14.8w (Rigid).", "#6A1B9A"),
            ("• Numeric Result: ", "Cuts pacing error from 10.12w (Zero-Shot) and 6.33w (Static) down to 3.87 words (Cluster-Adaptive)!", "#1B5E20"),
        ],
        bg_hex="#EDE7F6", border_hex="#5E35B1", font_size=7.4,
    )

    add_flow_arrow(s3, 9.83, 3.45, width=0.25, height=0.38, color_hex="#6A1B9A", direction="right")

    add_stage_banner(s3, xs[3], y_top, col_w, col_h, "STEP 4", "Within-Subjects Variance & RM-ANOVA", "#E8F5E9", "#2E7D32")
    add_card(
        s3, xs[3] + 0.10, y_top + 0.42, col_w - 0.20, 1.95,
        "4A. How Repeated-Measures Isolates Signal",
        [
            ("• Removing Dialogue Difficulty (SS_Subjects): ", "Each dialogue i has its own mean Ȳ_i. across the 3 prompts. RM-ANOVA subtracts SS_Subjects from total variance!", "#2E7D32"),
            ("• Pure Within-Dialogue Error (df = 64): ", "SS_Error = Σ_i Σ_c (Y_ic − Ȳ_i. − Ȳ_.c + Ȳ_..)^2.", "#2E7D32"),
            ("• Sphericity Check (ε): ", "Variance of pairwise differences checked via Greenhouse–Geisser ε (Style ε = .94; Pacing ε = .65).", "#E65100"),
        ],
        bg_hex="#FFFFFF", border_hex="#2E7D32", font_size=7.3,
    )
    add_flow_arrow(s3, xs[3] + 1.35, y_top + 2.41, width=0.28, height=0.22, color_hex="#2E7D32", direction="down")
    add_card(
        s3, xs[3] + 0.10, y_top + 2.66, col_w - 0.20, 2.66,
        "4B. 'Bulletproof' ANOVA Variations in RQ2",
        [
            ("1. Greenhouse–Geisser RM-ANOVA (df = ε·df): ", "• SBERT Style: F(1.88, 60.29) = 9.79, p < .001, ηp² = .234.\n• Pacing Error: F(1.30, 41.70) = 7.10, p = .007, ηp² = .182.\n• Contrast with Primary Archetypes (κ=.24): F = 1.61, p = .211 (null).", "#1565C0"),
            ("2. Holm–Bonferroni Step-Down Paired t-Tests: ", "Adaptive vs. Static: Δ = +.144 (+31.8%), t(32) = 4.26, p_Holm < .001, d_z = 0.74; Adaptive vs. Zero-Shot: t(32) = 2.37, p_Holm = .049.", "#E65100"),
            ("3. Non-Parametric Friedman Rank Test (χ²): ", "Ranks the 3 replies (1st, 2nd, 3rd) inside each dialogue: Style χ²(2) = 12.50 (p = .002); Pacing χ²(2) = 14.27 (p < .001) → Reject H02!", "#1B5E20"),
        ],
        bg_hex="#C8E6C9", border_hex="#1B5E20", font_size=7.1,
    )

    add_bottom_banner(
        s3,
        "RQ2 Defense Summary: Running the exact same 33 test dialogues through all 3 prompts removes baseline dialogue noise (SS_Subjects). Greenhouse–Geisser RM-ANOVA (F=9.79, p<.001), Holm paired t-tests (d_z=0.74), and non-parametric Friedman rank tests (χ²=12.50, p=.002) confirm significant style & pacing convergence.",
    )

    # =========================================================================
    # SLIDE 4: RQ3 STEP-BY-STEP FLOWCHART
    # =========================================================================
    s4 = prs.slides.add_slide(blank)
    add_header(
        s4,
        "RQ3 METHODOLOGY (SLIDE 4 OF 5)",
        "RQ3 Step-by-Step: 2 × 2 Factorial Rule/Prompt Injection & Bounded-Rate ANOVA",
        "How 36 held-out dialogues × 4 factorial cells (N = 144) are scored for Rule Adherence, Entity Leakage, and Slot F1, and analyzed via OLS, Sum-HC3, and ART ANOVA",
    )

    add_stage_banner(s4, xs[0], y_top, col_w, col_h, "STEP 1", "36 Dialogues + Seeded Policy States", "#F0F4F8", "#1B365D")
    add_card(
        s4, xs[0] + 0.10, y_top + 0.42, col_w - 0.20, 2.35,
        "1A. 36 Held-Out Test Dialogues (12 / Archetype)",
        [
            ("• Complete Within-Dialogue Crossing: ", "Each of the 36 held-out test dialogues is evaluated across all 4 cells of the 2 × 2 design (36 × 4 = 144 total LLM evaluations).", "#1B365D"),
            ("• Active User Slot Ledger (S_i): ", "Contains current traveler's true origin, destination, departure date, duration, adult count, and budget.", "#00695C"),
        ],
        bg_hex="#FFFFFF", border_hex="#1B365D", font_size=7.5,
    )
    add_flow_arrow(s4, xs[0] + 1.35, y_top + 2.82, width=0.28, height=0.22, color_hex="#1B365D", direction="down")
    add_card(
        s4, xs[0] + 0.10, y_top + 3.08, col_w - 0.20, 2.24,
        "1B. 50% Violating vs. 50% Compliant States",
        [
            ("• 18 Rule-Violating Cases per Cell: ", "Seeded to trigger 1 of 5 YAML rules (Table 9): <15d visa lead time, <6m passport validity, >4 FIT adults, >15% promo discount, or <$500 intl budget (tests Sensitivity).", "#C62828"),
            ("• 18 Policy-Compliant Cases per Cell: ", "Satisfy all 5 YAML rules (tests Specificity—ensuring the rule engine does not falsely block valid bookings!).", "#1B5E20"),
        ],
        bg_hex="#E3F2FD", border_hex="#1565C0", font_size=7.4,
    )

    add_flow_arrow(s4, 3.23, 3.45, width=0.25, height=0.38, color_hex="#1B365D", direction="right")

    add_stage_banner(s4, xs[1], y_top, col_w, col_h, "STEP 2", "2 × 2 Factorial Prompt Injection", "#E0F2F1", "#00695C")
    add_card(
        s4, xs[1] + 0.10, y_top + 0.42, col_w - 0.20, 2.38,
        "Factor A: Rules Off (Cells 1 & 2, n = 72)",
        [
            ("• Cell 1 (Rules Off × Zero-Shot, n = 36): ", "Prompt contains only a natural-language policy summary + dialogue context x_i.", "#455A64"),
            ("• Cell 2 (Rules Off × Cluster-Adaptive, n = 36): ", "Natural-language policy summary + Archetype Directive + k = 3 UNMASKED FAISS exemplars (containing foreign hotels/airlines/prices like 'Sapphire Bay Resort', '$1,149', 'VIP25').", "#C62828"),
        ],
        bg_hex="#FFEBEE", border_hex="#C62828", font_size=7.4,
    )
    add_flow_arrow(s4, xs[1] + 1.35, y_top + 2.84, width=0.28, height=0.22, color_hex="#00695C", direction="down")
    add_card(
        s4, xs[1] + 0.10, y_top + 3.10, col_w - 0.20, 2.22,
        "Factor A: Rules Active (Cells 3 & 4, n = 72)",
        [
            ("• Cell 3 (Rules Active × Zero-Shot, n = 36): ", "RuleEngine.evaluate(S_i) injects deterministic pre-check block ([RULE_VISA_LEAD_TIME TRIGGERED]) + Verified Slot Ledger.", "#1565C0"),
            ("• Cell 4 (Rules Active × Cluster-Adaptive, n = 36): ", "Integrated Governance Package: RuleEngine pre-check directive + Verified Slot Ledger + [SLOT]-masked archetype exemplars + post-generation entity leakage sanitizer!", "#1B5E20"),
        ],
        bg_hex="#E0F2F1", border_hex="#00695C", font_size=7.3,
    )

    add_flow_arrow(s4, 6.53, 3.45, width=0.25, height=0.38, color_hex="#00695C", direction="right")

    add_stage_banner(s4, xs[2], y_top, col_w, col_h, "STEP 3", "Text Response → 4 Numeric Scores", "#F3E5F5", "#6A1B9A")
    add_card(
        s4, xs[2] + 0.10, y_top + 0.42, col_w - 0.20, 2.65,
        "3A. Compliance & Leakage Proportions [0, 1]",
        [
            ("1. Rule Adherence (RAR ∈ {0, 1}): ", "Regex verifier + Dual-Judge (gemini-2.5-flash & gemini-2.5-pro, κ = .917): scores 1 if violation is enforced (Sensitivity: 5.6% Off → 100.0% / 97.2% Active) or compliant case accepted (Specificity: 94.4% vs. 88.9%); Overall Acc: .500 → .944 / .931.", "#6A1B9A"),
            ("2. Exemplar Leakage Rate (ELR ∈ [0, 1]): ", "|Leaked foreign exemplar entities in ŷ| / |E_foreign|. Cell 2 spikes to .359 (55.6% incidence); Cells 1, 3, 4 = .000 (0.0% incidence)!", "#C62828"),
        ],
        bg_hex="#FFFFFF", border_hex="#6A1B9A", font_size=7.3,
    )
    add_flow_arrow(s4, xs[2] + 1.35, y_top + 3.11, width=0.28, height=0.20, color_hex="#6A1B9A", direction="down")
    add_card(
        s4, xs[2] + 0.10, y_top + 3.34, col_w - 0.20, 1.98,
        "3B. Slot Grounding F1 & Style Cosine",
        [
            ("3. Factual Slot Coverage F1 ∈ [0, 1]: ", "2·Prec·Rec / (Prec + Rec) of active user slots grounded in ŷ: jumps from .208 / .485 (Rules Off) to .977 / .952 (Rules Active).", "#1B5E20"),
            ("4. De-Lexicalized Style Cosine: ", "Cluster-Adaptive lifts style cosine (.414/.428 → .507/.506) even when Rules are Active!", "#1565C0"),
        ],
        bg_hex="#EDE7F6", border_hex="#5E35B1", font_size=7.4,
    )

    add_flow_arrow(s4, 9.83, 3.45, width=0.25, height=0.38, color_hex="#6A1B9A", direction="right")

    add_stage_banner(s4, xs[3], y_top, col_w, col_h, "STEP 4", "2 × 2 Variance & 'Bulletproof' ANOVA", "#E8F5E9", "#2E7D32")
    add_card(
        s4, xs[3] + 0.10, y_top + 0.42, col_w - 0.20, 2.15,
        "4A. 2 × 2 Variance Partition & 3-Zero-Cell Identity",
        [
            ("• Orthogonal Partition (df_error = 140): ", "SS_Total = SS_Rules + SS_Prompt + SS_(Rules×Prompt) + SS_Error.", "#2E7D32"),
            ("• Why Leakage Has F = 34.82 for All 3 Terms: ", "Because 3 of 4 cells have zero leakage (Y_11 = Y_21 = Y_22 = 0, Y_12 = .359), all three (+1/−1) contrasts equal |±Y_12|/4 with identical SS = 1.161 and F(1, 140) = (n·Ȳ_12²)/s_12² = 34.82!", "#E65100"),
        ],
        bg_hex="#FFFFFF", border_hex="#2E7D32", font_size=7.2,
    )
    add_flow_arrow(s4, xs[3] + 1.35, y_top + 2.61, width=0.28, height=0.20, color_hex="#2E7D32", direction="down")
    add_card(
        s4, xs[3] + 0.10, y_top + 2.84, col_w - 0.20, 2.48,
        "4B. 'Bulletproof' ANOVA Variations in RQ3",
        [
            ("1. Two-Way OLS Factorial ANOVA: ", "• RAR Rules: Acc F(1,140)=43.92; Viol. Sens F(1,68)=498.78 (p<.001, ηp²=.880); Comp. Spec F=0.69 (p=.408).\n• Leakage Interaction: F(1,140)=34.82 (p<.001, ηp²=.199).\n• Slot F1 Rules: F(1,140)=489.52 (p<.001, ηp²=.778).", "#1565C0"),
            ("2. Sum-Coded HC3 Sandwich + Simple-Effect Welch t: ", "Sum-HC3 Interaction F = 33.85 (p < .001); Simple-effect Welch t(35) = 5.90 (p < .001) comparing .359 vs .000.", "#E65100"),
            ("3. Non-Parametric ART ANOVA & Exact Tests: ", "ART Interaction F = 2148.81 (p < .001); Mann–Whitney U = 1008.0 (p < .001); Fisher's exact p = 4.68×10⁻⁸ → Reject H03!", "#1B5E20"),
        ],
        bg_hex="#C8E6C9", border_hex="#1B5E20", font_size=7.0,
    )

    add_bottom_banner(
        s4,
        "RQ3 Defense Summary: Bounded [0, 1] compliance/leakage rates and the 3-zero-cell leakage floor (.000, .359, .000, .000) violate equal-variance assumptions. Pairing OLS 2×2 ANOVA with Sum-coded HC3 sandwich variance (F=33.85), Welch's t (t=5.90), and rank-based ART ANOVA (F=2148.81) makes the inference mathematically bulletproof.",
    )

    # =========================================================================
    # SLIDE 5: RQ4 STEP-BY-STEP FLOWCHART
    # =========================================================================
    s5 = prs.slides.add_slide(blank)
    add_header(
        s5,
        "RQ4 METHODOLOGY (SLIDE 5 OF 5)",
        "RQ4 Step-by-Step: 2 × 3 Multi-Turn Simulation & Turn-Economy Factorial ANOVA",
        "How 180 unique held-out seed dialogues run in closed-loop multi-turn simulation, convert to Log Turns & RER, and are tested via OLS, HC3, and ART ANOVA",
    )

    add_stage_banner(s5, xs[0], y_top, col_w, col_h, "STEP 1", "180 Seed Trips & Persona Simulator", "#F0F4F8", "#1B365D")
    add_card(
        s5, xs[0] + 0.10, y_top + 0.42, col_w - 0.20, 2.45,
        "1A. 180 Independent Seed Dialogues (n = 30/cell)",
        [
            ("• Between-Subjects 2 × 3 Design (N = 180): ", "60 unique held-out test dialogues per archetype (30 Zero-Shot + 30 Cluster-Adaptive = 180 independent multi-turn episodes).", "#1B365D"),
            ("• Initial Slot Seeding (Turn 1): ", "Customer opens with 3 of 5 core slots stated (origin, destination, departure date) and withholds 2 slots (duration_nights, budget_amount) until asked.", "#00695C"),
            ("• 4-Option Package Inventory: ", "Option A (4★ exact, 88% budget), Option B (3.5★ saver, 72%), Option C (5★ exact, 118% OVER budget!), Option D (5★ +3d shifted dates, 94% budget).", "#E65100"),
        ],
        bg_hex="#FFFFFF", border_hex="#1B365D", font_size=7.3,
    )
    add_flow_arrow(s5, xs[0] + 1.35, y_top + 2.91, width=0.28, height=0.20, color_hex="#1B365D", direction="down")
    add_card(
        s5, xs[0] + 0.10, y_top + 3.14, col_w - 0.20, 2.18,
        "1B. Blind Persona Simulator Validation (κ = .933)",
        [
            ("• Customer Simulator Rules: ", "Decisive accepts first valid match; Explorer requires comparing ≥2 options; Rigid demands 5★ under budget and pushes back on Option A unless given the Option A vs. D trade-off.", "#1565C0"),
            ("• Blind Gemini 2.5 Pro Audit (n = 45): ", "95.6% blind classification accuracy (43/45, exact binomial p = 1.37×10⁻¹⁸, κ = .933).", "#1B5E20"),
        ],
        bg_hex="#E3F2FD", border_hex="#1565C0", font_size=7.3,
    )

    add_flow_arrow(s5, 3.23, 3.45, width=0.25, height=0.38, color_hex="#1B365D", direction="right")

    add_stage_banner(s5, xs[1], y_top, col_w, col_h, "STEP 2", "Turn-by-Turn Policy Injection", "#E0F2F1", "#00695C")
    add_card(
        s5, xs[1] + 0.10, y_top + 0.42, col_w - 0.20, 1.95,
        "Mode 1: Zero-Shot Baseline (n = 90 Episodes)",
        [
            ("• Prompt Injected Each Turn: ", "Generic helpful travel assistant prompt + raw dialogue history.", "#455A64"),
            ("• Failure Modes: ", "Asks missing slots one-by-one, re-asks already stated slots (10.9% RER), and offers only Option A first—causing 8.73-turn pushback loops with Rigid Seekers!", "#C62828"),
        ],
        bg_hex="#FFEBEE", border_hex="#C62828", font_size=7.4,
    )
    add_flow_arrow(s5, xs[1] + 1.35, y_top + 2.41, width=0.28, height=0.20, color_hex="#00695C", direction="down")
    add_card(
        s5, xs[1] + 0.10, y_top + 2.64, col_w - 0.20, 2.68,
        "Mode 2: Cluster-Adaptive + Slot Ledger (n = 90)",
        [
            ("• Routed via Blocks (M = 9, κ = .958) + Verified Informed Slot Ledger: ", "Injects [Informed Slots: {...} | Missing Slots: {...} — NEVER re-ask informed slots; bundle missing slots in 1 question].", "#00695C"),
            ("• Archetype-Specific Turn-Economy Policy: ", "\n  1. Decisive Booker: Immediate Option A quote.\n  2. Open Explorer: Side-by-side Option A vs. Option B comparison table in 1 turn.\n  3. Rigid Seeker: Proactive single-turn trade-off explaining Option C's budget conflict + offering Option A (4★ exact) & Option D (5★ shifted).", "#1B5E20"),
        ],
        bg_hex="#E0F2F1", border_hex="#00695C", font_size=7.2,
    )

    add_flow_arrow(s5, 6.53, 3.45, width=0.25, height=0.38, color_hex="#00695C", direction="right")

    add_stage_banner(s5, xs[2], y_top, col_w, col_h, "STEP 3", "Multi-Turn Text → Numeric Scores", "#F3E5F5", "#6A1B9A")
    add_card(
        s5, xs[2] + 0.10, y_top + 0.42, col_w - 0.20, 2.75,
        "3A. Total Turns, 5.00-Turn Floor & Log Turns",
        [
            ("• Total Turns Definition: ", "total_turns = user_turns + assistant_turns until [ACCEPT_BOOKING].", "#6A1B9A"),
            ("• Why 5.00 Turns (SD = 0.00) Is the Protocol Floor: ", "U1 (3 slots) → A1 (bundled ask for duration+budget) → U2 (2 slots) → A2 (archetype-tailored package quote) → U3 ([ACCEPT_BOOKING]) = 5 messages!", "#E65100"),
            ("• Log Transformation Y = ln(total_turns): ", "Normalizes right-skewed turn counts:\n  • Rigid Seeker: 8.73 → 5.00 (−42.7%, d = −3.40)\n  • Decisive Booker: 7.60 → 5.00 (−34.2%, d = −3.94)\n  • Open Explorer: 7.47 → 5.27 (−29.5%, d = −2.55)", "#1B5E20"),
        ],
        bg_hex="#FFFFFF", border_hex="#6A1B9A", font_size=7.2,
    )
    add_flow_arrow(s5, xs[2] + 1.35, y_top + 3.21, width=0.28, height=0.20, color_hex="#6A1B9A", direction="down")
    add_card(
        s5, xs[2] + 0.10, y_top + 3.44, col_w - 0.20, 1.88,
        "3B. Redundant Elicitation Rate (RER ∈ [0, 1])",
        [
            ("• Regex Slot-Question Detector: ", "detect_asked_slots() inspects every assistant turn for questions about slots already present in Informed Slots.", "#6A1B9A"),
            ("• Numeric Result: ", "Drops from .194 (Decisive), .061 (Explorer), .072 (Rigid) [mean .109] in Zero-Shot to .000 across all 90 Cluster-Adaptive dialogues!", "#1B5E20"),
        ],
        bg_hex="#EDE7F6", border_hex="#5E35B1", font_size=7.3,
    )

    add_flow_arrow(s5, 9.83, 3.45, width=0.25, height=0.38, color_hex="#6A1B9A", direction="right")

    add_stage_banner(s5, xs[3], y_top, col_w, col_h, "STEP 4", "2 × 3 Variance & 'Bulletproof' ANOVA", "#E8F5E9", "#2E7D32")
    add_card(
        s5, xs[3] + 0.10, y_top + 0.42, col_w - 0.20, 1.95,
        "4A. 2 × 3 Variance Partition (df_error = 174)",
        [
            ("• Decomposition Across 6 Cells (n = 30/cell): ", "SS_Total = SS_Prompt(df=1) + SS_Arch(df=2) + SS_(Prompt×Arch)(df=2) + SS_Error(df=174).", "#2E7D32"),
            ("• Why the Interaction (F = 10.89) Is Significant: ", "Turn compression is non-uniform—steepest for Rigid-Constraint Seekers (−3.73 turns, −42.7%) where proactive trade-off framing resolves the Option C budget deadlock in 1 turn!", "#1B365D"),
        ],
        bg_hex="#FFFFFF", border_hex="#2E7D32", font_size=7.3,
    )
    add_flow_arrow(s5, xs[3] + 1.35, y_top + 2.41, width=0.28, height=0.20, color_hex="#2E7D32", direction="down")
    add_card(
        s5, xs[3] + 0.10, y_top + 2.64, col_w - 0.20, 2.68,
        "4B. 'Bulletproof' ANOVA Variations in RQ4",
        [
            ("1. Two-Way OLS ANOVA (Log Turns & Raw Turns): ", "• Log Turns: Prompt F(1,174) = 664.43 (p<.001, ηp²=.793); Arch F(2,174) = 5.55 (p=.005); Interaction F(2,174) = 10.89 (p<.001, ηp²=.111).\n• Raw Turns: Prompt F = 457.74; Interaction F = 14.37.\n• RER: Prompt F = 63.02; Interaction F = 9.70 (p<.001).", "#1565C0"),
            ("2. MacKinnon–White HC3 Sandwich + Welch's t: ", "Handles SD = 0.00 protocol floor in 2 cells: HC3 Prompt F = 681.53 (p<.001); HC3 Interaction F = 8.58 (p<.001); Welch t_log = −18.92, −10.97, −17.02 (all p<.001).", "#E65100"),
            ("3. Non-Parametric ART ANOVA & Mann–Whitney U: ", "ART Prompt F = 224.22, Interaction F = 209.46 (p<.001); Mann–Whitney U = 0.0, 40.5, 0.0 (all p<.001) → Reject H04!", "#1B5E20"),
        ],
        bg_hex="#C8E6C9", border_hex="#1B5E20", font_size=7.0,
    )

    add_bottom_banner(
        s5,
        "RQ4 Defense Summary: Because Cluster-Adaptive policies reach the deterministic 5.00-turn protocol floor (SD = 0.00) for Decisive and Rigid personas, we pair OLS ANOVA on log-transformed turns (F=664.43, Interaction F=10.89) with HC3 heteroscedasticity-robust F (8.58), ART Rank ANOVA (209.46), and Mann–Whitney U (p<.001).",
    )

    os.makedirs(os.path.dirname(OUT_PPTX), exist_ok=True)
    prs.save(OUT_PPTX)
    print(f"Saved standalone 5-slide RQ Text-to-ANOVA Methodology PPTX: {OUT_PPTX} (Total slides: {len(prs.slides)})")


if __name__ == "__main__":
    build_deck()

