"""
Generate a standalone, 100% native editable 16-slide PowerPoint deck:
  final/QM_640_RQ_Text_to_ANOVA_Methodology_Reference.pptx

Purpose:
  Reference / backup slides & ground-up foundational glossary for the defense
  evaluation committee illustrating:
    - Slide 1: General 4-Stage Text-to-ANOVA Pipeline & Bulletproof Inference Architecture
    - Slide 2: RQ1 Step-by-Step Sequence (Clustering & Prefix Routing Text-to-ANOVA)
    - Slide 3: RQ1 Deep-Dive (Why PCA-20? Who Names Clusters? Why K-Means + Logistic Regression?)
    - Slide 4: RQ2 Step-by-Step Sequence (Repeated-Measures Prompt Injection & Style/Pacing ANOVA)
    - Slide 5: RQ3 Step-by-Step Sequence (2x2 Factorial Rule/Prompt Injection & Bounded-Rate ANOVA)
    - Slide 6: RQ4 Step-by-Step Sequence (2x3 Closed-Loop Multi-Turn Simulation & Turn-Economy ANOVA)
    - Slide 7: Judge LLM Methodology (Why, When & How Judge LLMs Are Used Across RQ1–RQ4)
    - Slide 8: Glossary Part 1 — Elementary Stats, Distributions, Outliers, Correlation & PCA (Slides 11–13)
    - Slide 9: Glossary Part 2 — Hypothesis Testing Roots, Sample Size & Power (α, β, 1−β, df, F_crit, λ) (Slides 14, 17–18)
    - Slide 10: Glossary Part 3 — ANOVA Family, F-Ratio, Sphericity (ε), Interactions & Post-Hoc Tests (Slides 14–15, 22–33)
    - Slide 11: Glossary Part 4 — Effect Sizes Explained (η², ηp², Cohen's f, d, d_z, Cramér's V) (Slides 15, 17–18, 22–33)
    - Slide 12: Glossary Part 5 — Robust & Non-Parametric 'Bulletproof' Tests (Welch, HC3, Kruskal, Friedman, Mann–Whitney, ART) (Slides 14, 16, 22–33)
    - Slide 13: Glossary Part 6 — Unsupervised Clustering & Validity Metrics (K-Means, Ward, HDBSCAN, Silhouette, Davies–Bouldin, ARI, UMAP) (Slides 22–25)
    - Slide 14: Glossary Part 7 — Agreement & Routing Metrics (κ, κ_w, PABAK, p_o) & Domain Hyperparameters (λ_d, M, LogReg) (Slides 19, 23–25, 28, 31)
    - Slide 15: Glossary Part 8 — NLP Embeddings, FAISS & Domain Evaluation Metrics (MiniLM, Gemini, BERTScore, RAR, ELR, Slot F1, TGC, RER) (Slides 20, 26–33)
    - Slide 16: Defense Slide-by-Slide Decoder Cheat-Sheet (Direct Plain-English Key to Defense Slides 14–19 & 22–33)

Does NOT modify any existing report (.docx, .pdf) or other .pptx files.
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


def add_glossary_table(
    slide, left, top, width, height, headers, rows,
    col_widths=None, font_size=7.4, header_size=8.4, header_hex="#1B365D",
):
    n_rows = 1 + len(rows)
    n_cols = len(headers)
    shape = slide.shapes.add_table(n_rows, n_cols, Inches(left), Inches(top), Inches(width), Inches(height))
    tbl = shape.table
    if col_widths:
        tot = sum(col_widths)
        for ci, cw in enumerate(col_widths):
            tbl.columns[ci].width = Inches(width * (cw / tot))

    for ci, h_txt in enumerate(headers):
        cell = tbl.cell(0, ci)
        cell.fill.solid()
        cell.fill.fore_color.rgb = rgb(header_hex)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_left = cell.margin_right = Inches(0.05)
        cell.margin_top = cell.margin_bottom = Inches(0.02)
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        r = p.add_run()
        r.text = h_txt
        r.font.name = "Calibri"
        r.font.size = Pt(header_size)
        r.font.bold = True
        r.font.color.rgb = rgb("#FFFFFF")

    for ri, row in enumerate(rows):
        bg = "#F4F7FA" if ri % 2 == 1 else "#FFFFFF"
        for ci, val in enumerate(row):
            cell = tbl.cell(ri + 1, ci)
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb("#E8F5E9" if (ci == 0 and ri % 2 == 0) else ("#E3F2FD" if (ci == 0 and ri % 2 == 1) else bg))
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = cell.margin_right = Inches(0.05)
            cell.margin_top = cell.margin_bottom = Inches(0.02)
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            r = p.add_run()
            r.text = str(val)
            r.font.name = "Calibri"
            r.font.size = Pt(font_size)
            r.font.bold = (ci == 0)
            r.font.color.rgb = rgb("#0D3B66" if ci == 0 else ("#1B5E20" if ci == n_cols - 1 else "#212121"))
    return tbl


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
        "REFERENCE SLIDE 1 OF 16",
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
        "RQ1 METHODOLOGY (SLIDE 2 OF 16)",
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
        "3A. Metrics for Exp. 1A (Card 2A → Silhouette & DB)",
        [
            ("1. Cosine Silhouette Score Y_ij ∈ [-1, 1]: ", "Compares intra-cluster distance a(i) to nearest-cluster b(i): s(i) = [b(i)−a(i)]/max(a,b).", "#6A1B9A"),
            ("   • MiniLM-384d Means: ", "KM = .147, Ward = .118, HDB = .211* (39% noise), Perm = −.013.", "#1B365D"),
            ("   • Gemini-3072d Means: ", "Turn-Pool KM = .158 / Ward = .150 / HDB = .289*; Doc KM = .161 / Ward = .213 / HDB = .345*.", "#1565C0"),
            ("2. Davies–Bouldin Index (DB ↓): ", "Scatter-to-separation ratio (lowest = 2.647 at k=3 on 46-d Blocks).", "#6A1B9A"),
        ],
        bg_hex="#FFFFFF", border_hex="#6A1B9A", font_size=7.2,
    )
    add_flow_arrow(s2, xs[2] + 1.35, y_top + 3.01, width=0.28, height=0.22, color_hex="#6A1B9A", direction="down")
    add_card(
        s2, xs[2] + 0.10, y_top + 3.26, col_w - 0.20, 2.06,
        "3B. Metrics for Exp. 1B (Card 2B → Gemini Blocks ARI & κ)",
        [
            ("3. Bootstrap Stability ARI ∈ [-1, 1] (on 2B Blocks): ", "Adjusted Rand Index across subsamples of D_gold on the Gemini 46-d Blocks space: ARI = .89 in truncation grid (.87 in 6-config ablation).", "#6A1B9A"),
            ("4. Held-Out Prefix Routing Kappa (κ on 2B Router): ", "Chance-corrected agreement with M=9 reference labels y^(9) on D_test: κ = .359 (m=3) → κ = .535 (m=5, 70.1% raw) → κ = .722 (m=7) → κ = .958 (m=9, 97.3%).", "#1B5E20"),
        ],
        bg_hex="#EDE7F6", border_hex="#5E35B1", font_size=7.2,
    )

    add_flow_arrow(s2, 9.83, 3.45, width=0.25, height=0.38, color_hex="#6A1B9A", direction="right")

    add_stage_banner(s2, xs[3], y_top, col_w, col_h, "STEP 4", "Variance & Statistical Tests (4A & 4B)", "#E8F5E9", "#2E7D32")
    add_card(
        s2, xs[3] + 0.10, y_top + 0.42, col_w - 0.20, 2.55,
        "4A. Tests for 3A (Exp. 1A: N = 159 Algorithm ANOVAs)",
        [
            ("• Variance Split (df = 2, 156): ", "MS_Between (signal) ÷ MS_Within (noise; SD .019 KM vs .044 HDB).", "#2E7D32"),
            ("1. One-Way OLS + Tukey HSD: ", "MiniLM F(2,156) = 91.33, p < .001, η² = .539; Gemini Turn F = 77.09 (η² = .497); Gemini Doc F = 127.47 (η² = .620).", "#1565C0"),
            ("2. Matched-Seed RM-ANOVA: ", "F(1.72, 89.30) = 83.04, p < .001, ηp² = .615.", "#00695C"),
            ("3. Robust Welch + Rank Kruskal/Friedman: ", "Welch F(2, 89.15) = 66.98; Kruskal H(2) = 86.82; Friedman χ²(2) = 56.30 (all p < .001).", "#E65100"),
        ],
        bg_hex="#FFFFFF", border_hex="#2E7D32", font_size=7.1,
    )
    add_flow_arrow(s2, xs[3] + 1.35, y_top + 3.01, width=0.28, height=0.22, color_hex="#2E7D32", direction="down")
    add_card(
        s2, xs[3] + 0.10, y_top + 3.26, col_w - 0.20, 2.06,
        "4B. Tests for 3B (Exp. 1B: 46-d Blocks & Router Tests)",
        [
            ("1. Pre-Declared Eligibility Gate (D_gold): ", "ARI = .89 (≥ .60 threshold), smallest cluster = 25.5% (≥ 20% rule), lowest DB = 2.647 at k = 3.", "#1B5E20"),
            ("2. Archetype Profile ANOVAs & Outcome χ² (Table 13): ", "All 10 behavioral scales differ across the 3 personas (p < .001); held-out booking outcome χ² = 384.6, Cramér's V = .454 (p < .001).", "#1565C0"),
            ("3. Held-Out Routing vs. Chance (D_test, n = 401): ", "Golden vs. Test centroid t = −0.10 (p = .923, zero drift); prefix κ = .535 (m=5) → .958 (m=9), all p < .001 → Reject H01!", "#1B5E20"),
        ],
        bg_hex="#C8E6C9", border_hex="#1B5E20", font_size=7.0,
    )

    add_bottom_banner(
        s2,
        "RQ1 Defense Summary: Text dialogues are converted to 46-d hybrid 'Blocks' vectors and evaluated via Cosine Silhouette, DB, ARI, and κ. Because algorithm run variances differ (.019 vs. .044) and seeds are matched, One-Way OLS (F=91.33) is paired with Matched RM-ANOVA (F=83.04), Welch (F=66.98), and Friedman (χ²=56.30).",
    )

    # =========================================================================
    # SLIDE 3: RQ1 DEEP-DIVE (PCA vs. NAMED FEATURES vs. K-MEANS vs. LOG-REG)
    # =========================================================================
    s2b = prs.slides.add_slide(blank)
    add_header(
        s2b,
        "RQ1 DEEP-DIVE (SLIDE 3 OF 16)",
        "RQ1 Deep-Dive: Why PCA-20? Who Names the Clusters? Why K-Means + Logistic Regression?",
        "Resolving the 3 Core Methodological Questions: Constructing the 46-d 'Blocks' Vector, Deterministic Cluster Naming, and Offline Discovery vs. Online Routing",
    )

    # Col 1: Why PCA is needed (and what is NOT passed through PCA)
    add_stage_banner(s2b, xs[0], y_top, col_w, col_h, "PART 1", "Why PCA-20 Is Needed (And Where)", "#F0F4F8", "#1B365D")
    add_card(
        s2b, xs[0] + 0.10, y_top + 0.42, col_w - 0.20, 2.38,
        "1A. Two Parallel Feature Blocks (46-d Total)",
        [
            ("• Block 1 (Gemini Embedding → PCA-20): ", "Raw gemini-embedding-001 has 3,072 dimensions. ONLY this text embedding is compressed via PCA(20) into 20 unnamed components (PC1..PC20).", "#1565C0"),
            ("• Block 2 (26 Named Behavioral Cols — NO PCA!): ", "The 16 LLM behavioral fields (10 ordinal 1–5 scales + 16 one-hot goal/tone flags) are kept in their exact 26 human-named columns without PCA!", "#1B5E20"),
            ("• Fused 46-d 'Blocks' Vector X: ", "20 PCA dims + 26 named behavioral cols = 46 dimensions.", "#1B365D"),
        ],
        bg_hex="#FFFFFF", border_hex="#1B365D", font_size=7.3,
    )
    add_flow_arrow(s2b, xs[0] + 1.35, y_top + 2.84, width=0.28, height=0.20, color_hex="#1B365D", direction="down")
    add_card(
        s2b, xs[0] + 0.10, y_top + 3.08, col_w - 0.20, 2.24,
        "1B. Why K-Means Needs PCA on the 3,072-d Block",
        [
            ("• Prevents 118× Dimension Swamping: ", "K-Means sums Euclidean distance across all columns. Without PCA, 3,072 embedding dims overwhelm 26 behavioral cols (3,072 / 26 = 118×).", "#C62828"),
            ("• Curse of Dimensionality (D > 3·N_gold): ", "3,072 dims for N_gold = 933 dialogues makes pairwise Euclidean distances uniform; top 20 PCs strip 3,052 noise dims.", "#E65100"),
            ("• Ablation Proof (Table D6): ", "Raw Embedding K-Means has Cal. Silhouette = .014 & Outcome V = .342; 46-d Blocks doubles Silhouette (.033) & lifts V to .454!", "#00695C"),
        ],
        bg_hex="#E3F2FD", border_hex="#1565C0", font_size=7.2,
    )

    add_flow_arrow(s2b, 3.23, 3.45, width=0.25, height=0.38, color_hex="#1B365D", direction="right")

    # Col 2: Who names the features & clusters?
    add_stage_banner(s2b, xs[1], y_top, col_w, col_h, "PART 2", "How Clusters Get Semantic Names", "#E0F2F1", "#00695C")
    add_card(
        s2b, xs[1] + 0.10, y_top + 0.42, col_w - 0.20, 2.15,
        "2A. PCA Dimensions Are Never Named!",
        [
            ("• True Property of PCA: ", "PC1..PC20 are dense linear combinations of 3,072 floats—they have no human names.", "#C62828"),
            ("• How K-Means Uses the 46-d Vector: ", "At M = 9 user messages on D_gold (n = 933), K-Means (k = 3) uses all 46 columns (20 PCs + 26 behavioral cols) to partition dialogues into anonymous IDs {0, 1, 2}.", "#00695C"),
        ],
        bg_hex="#FFFFFF", border_hex="#00695C", font_size=7.4,
    )
    add_flow_arrow(s2b, xs[1] + 1.35, y_top + 2.61, width=0.28, height=0.20, color_hex="#00695C", direction="down")
    add_card(
        s2b, xs[1] + 0.10, y_top + 2.85, col_w - 0.20, 2.47,
        "2B. Deterministic Naming via 26 Named Columns",
        [
            ("• Pre-Declared Rule (step2i_rq1_refined_archetypes.py): ", "Computes each cluster's mean on the 10 named ordinal behavioral columns (which were NEVER passed through PCA):", "#1B365D"),
            ("  1. idxmax(destination_flexibility = 3.58/5): ", "→ Named 'Open Explorer' (25.5% of D_gold).", "#1565C0"),
            ("  2. idxmax(decisiveness = 3.66/5 of rest): ", "→ Named 'Decisive Booker' (45.0% of D_gold).", "#1B5E20"),
            ("  3. Remaining Cluster (highest price_sensitivity): ", "→ Named 'Rigid-Constraint Seeker' (29.5%).", "#E65100"),
        ],
        bg_hex="#E0F2F1", border_hex="#00695C", font_size=7.3,
    )

    add_flow_arrow(s2b, 6.53, 3.45, width=0.25, height=0.38, color_hex="#00695C", direction="right")

    # Col 3: Why K-Means alone cannot route early turns (M=3, 5)
    add_stage_banner(s2b, xs[2], y_top, col_w, col_h, "PART 3", "Why K-Means Alone Fails at M = 3, 5", "#F3E5F5", "#6A1B9A")
    add_card(
        s2b, xs[2] + 0.10, y_top + 0.42, col_w - 0.20, 2.48,
        "3A. Offline Discovery (M=9) vs. Online Routing (M=5)",
        [
            ("• Reference Taxonomy Needs M = 9 User Msgs: ", "A traveler's true behavioral persona y^(9) (revisions, option comparison, trade-offs) only stabilizes after ~9 user messages (~17 total turns, bootstrap ARI = .89).", "#6A1B9A"),
            ("• Runtime Chatbot Must Route Early (M = 3 or 5): ", "In RQ2–RQ4, the bot cannot wait until turn 17 to adapt its prompt—it must route the user by message M = 5!", "#C62828"),
        ],
        bg_hex="#FFFFFF", border_hex="#6A1B9A", font_size=7.4,
    )
    add_flow_arrow(s2b, xs[2] + 1.35, y_top + 2.94, width=0.28, height=0.20, color_hex="#6A1B9A", direction="down")
    add_card(
        s2b, xs[2] + 0.10, y_top + 3.18, col_w - 0.20, 2.14,
        "3B. Two Flaws of Using Unsupervised K-Means at M=5",
        [
            ("• Flaw 1 — Equal Coordinate Weighting: ", "At M = 3 or 5, features like revision_tendency are still unrevealed (0), yet K-Means Euclidean distance weights all 46 coordinates equally (1.0)!", "#C62828"),
            ("• Flaw 2 — Moving-Target Instability if Refit: ", "Fitting separate K-Means at M = 3 or M = 5 drops cluster stability from ARI = .89 down to .55–.65 and shifts cluster definitions every turn.", "#E65100"),
        ],
        bg_hex="#EDE7F6", border_hex="#5E35B1", font_size=7.3,
    )

    add_flow_arrow(s2b, 9.83, 3.45, width=0.25, height=0.38, color_hex="#6A1B9A", direction="right")

    # Col 4: How Logistic Regression complements K-Means
    add_stage_banner(s2b, xs[3], y_top, col_w, col_h, "PART 4", "How Logistic Regression Solves Routing", "#E8F5E9", "#2E7D32")
    add_card(
        s2b, xs[3] + 0.10, y_top + 0.42, col_w - 0.20, 2.50,
        "4A. Supervised Prefix-to-Archetype Mapping",
        [
            ("• Exact Input Features to Logistic Regression: ", "Takes the 46-d Blocks vector X^(m) at early prefix m ∈ {3, 5, 7, 9} (20 PCA prefix dims + 26 opening behavioral cols).", "#2E7D32"),
            ("• Target Labels y^(9): ", "Trained on D_gold to predict the fixed M = 9 K-Means reference archetype y^(9).", "#1B365D"),
            ("• Learns Discriminative Weights W^(m) (3 × 46): ", "Automatically up-weights early-revealed cues (information_upfront, primary_goal, opening phrasing) and down-weights unrevealed late-turn features!", "#1B5E20"),
        ],
        bg_hex="#FFFFFF", border_hex="#2E7D32", font_size=7.3,
    )
    add_flow_arrow(s2b, xs[3] + 1.35, y_top + 2.96, width=0.28, height=0.20, color_hex="#2E7D32", direction="down")
    add_card(
        s2b, xs[3] + 0.10, y_top + 3.20, col_w - 0.20, 2.12,
        "4B. Calibrated Probabilities & Held-Out Accuracy",
        [
            ("• Softmax Posterior Probabilities P(c | X^(m)): ", "Unlike hard K-Means IDs, outputs confidence scores (e.g., m=5: Open Explorer .48, Rigid .38 → m=9: Open Explorer .89).", "#1565C0"),
            ("• Held-Out D_test (n = 401) Convergence: ", "m = 3 (59.4%, κ = .359) → m = 5 (70.1%, κ = .535) → m = 7 (82.0%, κ = .722) → m = 9 (97.3%, κ = .958).", "#1B5E20"),
        ],
        bg_hex="#C8E6C9", border_hex="#1B5E20", font_size=7.3,
    )

    add_bottom_banner(
        s2b,
        "RQ1 Deep-Dive Takeaway: (1) PCA-20 compresses only the 3,072-d embedding so it doesn't swamp the 26 behavioral cols; (2) Cluster names come deterministically from the 26 non-PCA behavioral cols; (3) K-Means discovers the ground-truth personas offline at M=9, while Logistic Regression learns discriminative weights to route incomplete early prefixes (M=3, 5) online.",
    )

    # =========================================================================
    # SLIDE 4: RQ2 STEP-BY-STEP FLOWCHART
    # =========================================================================
    s3 = prs.slides.add_slide(blank)
    add_header(
        s3,
        "RQ2 METHODOLOGY (SLIDE 4 OF 16)",
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
    # SLIDE 5: RQ3 STEP-BY-STEP FLOWCHART
    # =========================================================================
    s4 = prs.slides.add_slide(blank)
    add_header(
        s4,
        "RQ3 METHODOLOGY (SLIDE 5 OF 16)",
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
    # SLIDE 6: RQ4 STEP-BY-STEP FLOWCHART
    # =========================================================================
    s5 = prs.slides.add_slide(blank)
    add_header(
        s5,
        "RQ4 METHODOLOGY (SLIDE 6 OF 16)",
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
        "RQ4 Defense Summary: Because Cluster-Adaptive policies reach the deterministic 5.00-turn protocol floor (SD = 0.00) for Decisive and Rigid personas, OLS ANOVA on log-transformed turns (F=664.43, Interaction F=10.89) is paired with HC3 heteroscedasticity-robust F (8.58), ART Rank ANOVA (209.46), and Mann–Whitney U (p<.001).",
    )

    # =========================================================================
    # SLIDE 7: JUDGE LLM METHODOLOGY (WHY, WHEN & HOW JUDGE LLMs ARE USED)
    # =========================================================================
    s6 = prs.slides.add_slide(blank)
    add_header(
        s6,
        "JUDGE LLM METHODOLOGY (SLIDE 7 OF 16)",
        "Why, When & How 'Judge LLMs' Are Used Across RQ1–RQ4 (And How Bias Is Prevented)",
        "Distinguishing Deterministic Python/Vector Scorers from Semantic LLM Judges, Cross-Tier Dual-Judge Verification, and Blind Persona Audits",
    )

    # Col 1: RQ1 Behavioral Codebook Annotator & Test-Retest Judge
    add_stage_banner(s6, xs[0], y_top, col_w, col_h, "RQ1 ROLE", "Behavioral Codebook Judge (temp=0)", "#F0F4F8", "#1B365D")
    add_card(
        s6, xs[0] + 0.10, y_top + 0.42, col_w - 0.20, 2.38,
        "1A. Why an LLM Judge/Annotator Is Needed in RQ1",
        [
            ("• Limitation of Raw Text Embeddings: ", "MiniLM/Gemini embeddings group dialogues by surface words (cities, dates) rather than latent decision style (Cal. Silhouette = .014).", "#C62828"),
            ("• Structured 16-Field Rubric (UserBehaviour): ", "gemini-2.5-flash (temp = 0.0) evaluates customer prefixes against a strict Pydantic schema (10 ordinal 1–5 scales + 6 categorical fields).", "#1B365D"),
        ],
        bg_hex="#FFFFFF", border_hex="#1B365D", font_size=7.4,
    )
    add_flow_arrow(s6, xs[0] + 1.35, y_top + 2.84, width=0.28, height=0.20, color_hex="#1B365D", direction="down")
    add_card(
        s6, xs[0] + 0.10, y_top + 3.08, col_w - 0.20, 2.24,
        "1B. How RQ1 Annotator Reliability Is Verified",
        [
            ("• Blind Test–Retest Audit (n = 200): ", "Re-annotated independently to verify quadratic weighted kappa: κ_w = .87 to .96 across the 10 ordinal scales!", "#1B5E20"),
            ("• Held-Out Criterion Audit (Fields 14–16): ", "Outcome fields (booked vs. stalled) are NEVER fed into clustering; held out strictly to test external validity (Cramér's V = .454, p < .001).", "#1565C0"),
        ],
        bg_hex="#E3F2FD", border_hex="#1565C0", font_size=7.4,
    )

    add_flow_arrow(s6, 3.23, 3.45, width=0.25, height=0.38, color_hex="#1B365D", direction="right")

    # Col 2: RQ2 Why NO Judge LLM Is Used (Avoiding Self-Preference Bias)
    add_stage_banner(s6, xs[1], y_top, col_w, col_h, "RQ2 ROLE", "Why RQ2 Uses ZERO LLM Judges", "#E0F2F1", "#00695C")
    add_card(
        s6, xs[1] + 0.10, y_top + 0.42, col_w - 0.20, 2.38,
        "2A. The Danger of Judge Self-Preference Bias",
        [
            ("• Why an LLM Judge Is NOT Used in RQ2: ", "Because gemini-2.5-flash generates the chatbot replies, asking an LLM to rate 'how natural or stylish' the reply sounds introduces severe LLM self-preference & verbosity bias!", "#C62828"),
            ("• Ground-Truth Anchor Available (y_i*): ", "Every held-out Frames turn has the real human wizard's actual reply y_i*.", "#00695C"),
        ],
        bg_hex="#FFFFFF", border_hex="#00695C", font_size=7.4,
    )
    add_flow_arrow(s6, xs[1] + 1.35, y_top + 2.84, width=0.28, height=0.20, color_hex="#00695C", direction="down")
    add_card(
        s6, xs[1] + 0.10, y_top + 3.08, col_w - 0.20, 2.24,
        "2B. Deterministic Vector & Word Scorers Used Instead",
        [
            ("• De-Lexicalized Vector Cosine: ", "Masks all entities ([CITY], [DATE], [PRICE]) and computes exact dot-product cosine against human reply y_i* in MiniLM-384d (independent encoder!) and Gemini-3072d.", "#1B5E20"),
            ("• Exact Word-Count Pacing Error: ", "|Words(ŷ_i,c) − μ_Words(Gold Archetype)|—100% deterministic Python math.", "#1B365D"),
        ],
        bg_hex="#E0F2F1", border_hex="#00695C", font_size=7.4,
    )

    add_flow_arrow(s6, 6.53, 3.45, width=0.25, height=0.38, color_hex="#00695C", direction="right")

    # Col 3: RQ3 Dual-Model Policy Compliance Judges + Regex Triangulation
    add_stage_banner(s6, xs[2], y_top, col_w, col_h, "RQ3 ROLE", "Dual-Judge + Regex Policy Audit", "#F3E5F5", "#6A1B9A")
    add_card(
        s6, xs[2] + 0.10, y_top + 0.42, col_w - 0.20, 2.38,
        "3A. Why & When Judge LLMs Are Needed in RQ3",
        [
            ("• Why Regex Alone Is Not Enough for RAR: ", "A chatbot can enforce or violate a policy (e.g., 15% discount cap, 15-day visa lead time, >4 FIT pax) using hundreds of natural-language phrasings.", "#6A1B9A"),
            ("• When Invoked: ", "Evaluates all N = 144 replies across the 2 × 2 design (18 violating + 18 compliant cases per cell) for semantic policy enforcement.", "#1B365D"),
        ],
        bg_hex="#FFFFFF", border_hex="#6A1B9A", font_size=7.4,
    )
    add_flow_arrow(s6, xs[2] + 1.35, y_top + 2.84, width=0.28, height=0.20, color_hex="#6A1B9A", direction="down")
    add_card(
        s6, xs[2] + 0.10, y_top + 3.08, col_w - 0.20, 2.24,
        "3B. 3-Way Triangulation (D + Judge J1 + Judge J2)",
        [
            ("• Auditor 1 (Deterministic Regex D): ", "Checks explicit numbers, discount caps, and refusal/remediation keywords.", "#455A64"),
            ("• Auditor 2 (Judge J1 — gemini-2.5-flash, temp=0): ", "Structured Pydantic compliance verdict.", "#1565C0"),
            ("• Auditor 3 (Judge J2 — gemini-2.5-pro, temp=0): ", "Higher-tier cross-model verification → Inter-Judge Cohen's κ(J1, J2) = .917 (95.8% raw agreement)!", "#1B5E20"),
        ],
        bg_hex="#EDE7F6", border_hex="#5E35B1", font_size=7.3,
    )

    add_flow_arrow(s6, 9.83, 3.45, width=0.25, height=0.38, color_hex="#6A1B9A", direction="right")

    # Col 4: RQ4 Blind Persona Fidelity Judge & Summary Safeguards
    add_stage_banner(s6, xs[3], y_top, col_w, col_h, "RQ4 ROLE", "Blind Persona Fidelity Judge", "#E8F5E9", "#2E7D32")
    add_card(
        s6, xs[3] + 0.10, y_top + 0.42, col_w - 0.20, 2.45,
        "4A. Why & When a Judge LLM Is Used in RQ4",
        [
            ("• Primary RQ4 Metrics Are 100% Deterministic: ", "Total Turns (T), Log Turns ln(T), and Redundant Elicitation Rate (RER) are counted by exact Python state/regex trackers—zero LLM judge needed.", "#1B365D"),
            ("• Why Judge LLM Is Needed for Simulator Audit: ", "To prove the Customer Simulator (gemini-2.5-flash) genuinely enactments the 3 personas without circularity or label leakage!", "#2E7D32"),
        ],
        bg_hex="#FFFFFF", border_hex="#2E7D32", font_size=7.3,
    )
    add_flow_arrow(s6, xs[3] + 1.35, y_top + 2.91, width=0.28, height=0.20, color_hex="#2E7D32", direction="down")
    add_card(
        s6, xs[3] + 0.10, y_top + 3.15, col_w - 0.20, 2.17,
        "4B. Blind Gemini 2.5 Pro Audit & 4 Safeguards",
        [
            ("• Blind Persona Audit (n = 45 Transcripts): ", "Independent gemini-2.5-pro judge blindly classifies anonymized user turns into the 3 archetypes: 43/45 = 95.6% accuracy, κ = .933 (p = 1.37×10⁻¹⁸)!", "#1B5E20"),
            ("• 4 Anti-Bias Safeguards: ", "(1) temp = 0.0; (2) Pydantic JSON schemas; (3) Cross-tier Pro vs. Flash audit; (4) Anchored to deterministic regex.", "#E65100"),
        ],
        bg_hex="#C8E6C9", border_hex="#1B5E20", font_size=7.3,
    )

    add_bottom_banner(
        s6,
        "Judge LLM Defense Summary: Judge LLMs are NEVER used where exact vector/Python math suffices (RQ2 style cosine & pacing; RQ3 leakage & Slot F1; RQ4 turn counts & RER). Where semantic evaluation is required (RQ1 codebook, RQ3 policy compliance, RQ4 simulator audit), the pipeline enforces temp=0, Pydantic schemas, regex triangulation, and cross-tier Gemini 2.5 Pro verification (κ = .917–.933).",
    )

    # =========================================================================
    # SLIDE 8: GLOSSARY PART 1 — ELEMENTARY DESCRIPTIVE STATS, SKEWNESS, CORRELATION & PCA
    # =========================================================================
    s8 = prs.slides.add_slide(blank)
    add_header(
        s8,
        "GLOSSARY PART 1 (SLIDE 8 OF 16)",
        "Ground-Root Foundations 1: Distributions, Skewness, Correlations (r vs. ρ) & PCA",
        "Elementary Building Blocks Behind Defense Slides 11–13 (EDA), Slide 24 (RQ1 PCA-20), and Slide 33 (RQ4 Log Turns)",
    )
    add_card(
        s8, 0.22, 0.88, 6.35, 1.10,
        "Ground-Root Intuition A: Why Normal vs. Skewed Data Changes Measurement & Correlation",
        [
            ("• Symmetric (Bell Curve) vs. Right-Skewed Data: ", "Most chats finish in 8–15 turns, but tough negotiations stretch to 35–47 turns. That 'long right tail' pulls the average (Mean M) upward and inflates variance (SD).", "#1B365D"),
            ("• Handling Skewness in 2 Ways: ", "(1) Pair linear tools (Mean, Pearson r) with rank/order tools (Median, IQR, Spearman ρ) that ignore tail extremes; (2) Apply Natural Log ln(Turns) in RQ4 to pull the right tail into a symmetric bell curve.", "#00695C"),
        ],
        bg_hex="#E3F2FD", border_hex="#1565C0", font_size=7.4,
    )
    add_card(
        s8, 6.76, 0.88, 6.35, 1.10,
        "Ground-Root Intuition B: What Principal Component Analysis (PCA) Actually Does",
        [
            ("• Everyday Analogy (Photographing a 3D Teapot): ", "If you have 10 (or 3,072) correlated columns that overlap, PCA rotates the coordinate axes to find the single best camera angle (PC1) that captures the widest spread of data, then a perpendicular angle (PC2) for the next widest spread.", "#6A1B9A"),
            ("• Two Distinct Uses of PCA in the Study: ", "(1) Visual 3-axis summary of 10 EDA variables (Slide 13: PC1=40.8%, PC2=17.2%, PC3=10.6%); (2) Compressing 3,072-d Gemini embeddings into 20 numbers (PCA-20) in RQ1 so they don't drown out the 26 behavioral columns!", "#1B5E20"),
        ],
        bg_hex="#F3E5F5", border_hex="#6A1B9A", font_size=7.4,
    )
    add_glossary_table(
        s8, 0.22, 2.04, 12.89, 4.45,
        headers=[
            "Concept / Symbol",
            "Elementary Ground-Root Meaning (Plain English — What Is It Really?)",
            "Where Used (Slides & RQ)",
            "Why Used Here (Problem Solved)",
            "Core Result Achieved in Paper",
        ],
        rows=[
            [
                "Mean (M or μ) &\nStd. Deviation (SD / σ)",
                "• Mean (M): Arithmetic average (sum ÷ count).\n• SD (σ): Typical distance of individual dialogues from the mean. Small SD = tight consistency; large SD = wide scatter.",
                "Slides 12, 22–33\nAll RQs (Tables 6–16)",
                "Summarizes central tendency and spread inside every experimental group and cell.",
                "Frames Turns: M = 14.90 (SD = 6.74) vs. MultiWOZ M = 13.52 (SD = 4.46) → Frames has 51% wider dispersion.",
            ],
            [
                "Quartiles (Q1, Q3),\nIQR & Outlier Rule\n(> Q3 + 1.5×IQR)",
                "• Sort data from smallest to largest: Q1 = 25th percentile, Q3 = 75th percentile.\n• IQR = Q3 − Q1 (spread of the middle 50%). Anything > 1.5 IQRs above Q3 is flagged as an extreme right-tail value.",
                "Slide 11 (Table 5)\nData Cleaning Audit\n(Section 3.3)",
                "Distinguishes corrupted data errors from genuine long customer negotiations.",
                "Flagged 20 Frames (>30.5 turns) & 21 MultiWOZ (>24.0 turns) dialogues; retained as real negotiations & log-transformed in RQ4.",
            ],
            [
                "Natural Log Transform\nY = ln(TGC)",
                "• Replaces raw turn count T with its natural logarithm ln(T) (e.g., ln(5)=1.609, ln(8.73)=2.152).\n• Compresses extreme high values much more than small values, turning a right-skewed tail into a bell curve.",
                "Slides 11, 14, 16, 33\nRQ4 Primary DV\n(Table 16)",
                "Positive count data (turns ≥ 5) is right-skewed; OLS ANOVA assumes symmetric normal residuals.",
                "Log Turns Prompting F(1,174) = 664.43 (p < .001, ηp² = .793); Interaction F(2,174) = 10.89 (p < .001).",
            ],
            [
                "Pearson Linear\nCorrelation (r ∈ [-1, 1])",
                "• Measures how tightly two variables fall along a straight line: +1 = perfect upward line, 0 = no linear link, −1 = downward line.\n• Sensitive to extreme tail outliers because it uses raw distances from the mean.",
                "Slide 12 (Table 7)\nBivariate EDA\n(Section 3.4)",
                "Quantifies linear strength between turn length, slot revisions, and package offers.",
                "Turns × Slot Revisions r = .602 (p < .001); Turns × Package Offers r = .636 (p < .001); Turns × Decisiveness r = −.229.",
            ],
            [
                "Spearman Rank\nCorrelation (ρ / rho)",
                "• Converts raw numbers into ranks (1st, 2nd, 3rd...) FIRST, then computes Pearson correlation on the ranks.\n• Captures any monotonic (consistently rising/falling) trend and is 100% immune to extreme outliers.",
                "Slides 12, 13, 24\nEDA (Fig 3) & RQ1\nCodebook Validation",
                "Proves correlations aren't outlier artifacts & validates ordinal 1–5 LLM ratings against corpus counts.",
                "EDA: Revisions ρ = .582, Offers ρ = .661 (matches Pearson r!). RQ1 Validation: LLM revision_tendency × real revisions ρ = .64 (p < .001).",
            ],
            [
                "Principal Component\nAnalysis (PCA) &\nLoadings (PC1..PCk)",
                "• Unsupervised matrix rotation (SVD) that compresses D correlated features into k orthogonal (uncorrelated) axes ordered by variance explained.\n• Loadings (−1 to +1) show which original variables drive each PC axis.",
                "Slide 13 (EDA Biplot)\nSlide 24 (RQ1 PCA-20\nin 46-d Blocks)",
                "In EDA: visualizes 10 variables in 3 axes. In RQ1: shrinks 3,072-d Gemini embeddings to 20 dims so they don't swamp 26 behavioral cols.",
                "EDA: PC1 (40.8% Exploration), PC2 (17.2% Decisiveness/Price), PC3 (10.6% Verbosity) = 68.6% var. RQ1: PCA-20 + 26 cols → ARI = .89.",
            ],
        ],
        col_widths=[1.85, 3.85, 1.55, 2.55, 3.09],
        font_size=7.2,
    )
    add_bottom_banner(
        s8,
        "How Slide 8 Unlocks Defense Slides 11–13: When presenting Slides 11–13, tell the committee: 'Because multi-turn negotiations have a right tail (up to 47 turns), parametric Mean/SD/Pearson r are reported side-by-side with rank-based IQR/Spearman ρ, PCA maps the 3 orthogonal behavioral dimensions (68.6% variance), and ln(Turns) is applied in RQ4.'",
    )

    # =========================================================================
    # SLIDE 9: GLOSSARY PART 2 — HYPOTHESIS TESTING ROOTS, SAMPLE SIZE & POWER (α, β, 1−β, df, F_crit, λ)
    # =========================================================================
    s9 = prs.slides.add_slide(blank)
    add_header(
        s9,
        "GLOSSARY PART 2 (SLIDE 9 OF 16)",
        "Ground-Root Foundations 2: Hypothesis Testing, α, Power (1 − β), df, F_crit & Noncentrality λ",
        "Elementary Building Blocks Behind Defense Slides 14, 17 & 18 (How Sample Sizes N = 159, 33, 144, 180 Are Derived)",
    )
    add_card(
        s9, 0.22, 0.88, 6.35, 1.10,
        "Ground-Root Intuition A: Courtroom Analogy for H0, Ha, α (False Positive) & β (False Negative)",
        [
            ("• Null Hypothesis (H0 = 'Innocent / No Effect'): ", "Starts by assuming the proposed chatbot is NO better than the baseline, and any observed difference is just random coin-flip luck.", "#1B365D"),
            ("• Type I Error (α = .05) vs. Type II Error (β = .20): ", "α = 5% max risk of convicting an innocent person (claiming a false win). β = 20% max risk of letting a real improvement go undetected because sample size N was too small → Power (1 − β) = 80% detection radar!", "#C62828"),
        ],
        bg_hex="#FFEBEE", border_hex="#C62828", font_size=7.4,
    )
    add_card(
        s9, 6.76, 0.88, 6.35, 1.10,
        "Ground-Root Intuition B: What the Noncentrality Parameter (λ) Actually Means Visually",
        [
            ("• Central F (When H0 Is True, λ = 0): ", "If prompts are identical, the F-ratio sits near 1.0. A red cutoff line is drawn at the top 5% tail called F_crit (around 3.05 to 3.92).", "#1B365D"),
            ("• Noncentral F (When Ha Is True, λ = f²·N): ", "When a real effect (f = .25) exists, adding more dialogues N pushes the entire bell curve to the right by distance λ = f²·N. Once λ reaches ~8.0 to 10.5, ≥80% of the shifted bell curve crosses F_crit!", "#1B5E20"),
        ],
        bg_hex="#E8F5E9", border_hex="#2E7D32", font_size=7.4,
    )
    add_glossary_table(
        s9, 0.22, 2.04, 12.89, 4.45,
        headers=[
            "Concept / Symbol",
            "Elementary Ground-Root Meaning (Plain English — What Is It Really?)",
            "Where Used (Slides & RQ)",
            "Why Used Here (Problem Solved)",
            "Core Result Achieved in Paper",
        ],
        rows=[
            [
                "Null (H0) vs. Alt (Ha)\n& p-Value",
                "• H0: Group means are equal (μ1 = μ2 = ...).\n• Ha: At least one group mean differs.\n• p-value: Probability of seeing an F-statistic as big as the observed value by pure luck if H0 were true. If p < .05, reject H0.",
                "Slides 9, 14–18, 22–34\nAll 4 RQs (Table 11)",
                "Provides a formal, objective falsification rule for every scientific claim.",
                "All 4 null hypotheses (H01, H02, H03, H04) rejected at p < .001 across parametric, robust, and rank tests.",
            ],
            [
                "Type I Error Rate\n(α = .05)",
                "• The 'False Alarm' ceiling: maximum acceptable probability (5%) of claiming an effect exists when H0 is actually true.\n• Why α = .20 fails (Slide 18): inflates false positives 4×, turning noise into fake discoveries.",
                "Slides 14, 17, 18\nSection 3.2 (Table 4)\nstep0_sample_size.py",
                "Protects the committee and enterprise from adopting a chatbot method that works only by chance.",
                "Fixed at α = .05 across all RQs; primary effects achieve p < .001 (100× stricter than .05).",
            ],
            [
                "Type II Error (β = .20)\n& Statistical Power\n(1 − β ≥ .80)",
                "• β (.20): Risk of a 'Missed Detection' (False Negative) when a true medium effect exists.\n• Power (1 − β = .80): Probability (≥80%) that the experiment successfully detects a true medium effect (f = .25).",
                "Slides 17, 18\nSection 3.2 (Eq. 1 &\nTable 4)",
                "Prevents underpowered small-N experiments (Slide 18: N=36 drops power to .308, missing real gains 69% of the time!).",
                "Buffered sample sizes achieve realized power of .804 (RQ1), .865 (RQ2), .847 (RQ3), and .857 (RQ4).",
            ],
            [
                "Degrees of Freedom\n(df1, df2) &\nCritical Cutoff (F_crit)",
                "• df1 (Numerator = k − 1): Number of independent group contrasts (Signal dimensions: 1 or 2).\n• df2 (Denominator = N − k): Independent data points estimating within-group noise.\n• F_crit: Exact F threshold where top 5% tail of central F(df1, df2) begins.",
                "Slides 15, 17, 18\nTables 4, 12, 14, 15, 16",
                "Determines the exact shape of the F-distribution and the hurdle F must clear to beat α = .05.",
                "F_crit = 3.05 (RQ1 df=2,156), 3.17 (RQ2), 3.92 (RQ3 df=1,140), 3.06 (RQ4 df=2,174). Observed F values (9.79 to 664.43) far exceed F_crit!",
            ],
            [
                "Noncentrality\nParameter (λ / Lambda)\nλ = f² · N",
                "• Measures total statistical signal accumulated across N samples.\n• Between-subjects: λ = f² · N (with f = .25 → f² = 0.0625).\n• Solving 0.0625 × N ≈ 8.00 (df1=1) gives N_min = 128; solving 0.0625 × N ≈ 9.88 (df1=2) gives N_min = 158!",
                "Slides 17, 18\nEquation 1 & Table 4\n(Defense Q1)",
                "Bridges target effect size (f = .25) and exact minimum sample size N_min via the noncentral F distribution.",
                "At N_min: λ = 9.88 (RQ1, N=158→159), λ = 10.50 (RQ2, N=28→33), λ = 8.00 (RQ3, N=128→144), λ = 9.88 (RQ4, N=158→180).",
            ],
            [
                "Within-Subject Corr.\n(ρ = .50) in RM Power\nλ = f²·N·m·ε / (1−ρ)",
                "• In RQ2, testing the same dialogue across m = 3 prompts means baseline dialogue difficulty correlates by ρ ≈ .50 across conditions.\n• Subtracting baseline noise divides error variance by (1 − ρ) = 0.50, multiplying λ by m/(1−ρ) = 6×!",
                "Slides 14, 17, 18\nRQ2 Power Design\n(Table 4)",
                "Explains why RQ2 needs only N = 33 dialogues (99 calls) instead of 159 dialogues to reach >80% power.",
                "At N = 33 dialogues (99 calls), RQ2 achieves 86.5% power and detects style (p < .001) & pacing (p = .007) even under ε = 0.65.",
            ],
        ],
        col_widths=[1.85, 3.85, 1.55, 2.55, 3.09],
        font_size=7.2,
    )
    add_bottom_banner(
        s9,
        "How Slide 9 Unlocks Defense Slides 17 & 18: If asked 'How were N = 159, 33, 144, and 180 selected?', point to λ = f²·N: 'At α = .05 and 80% power, a medium effect (f = .25, f² = .0625) requires noncentrality λ ≈ 8.0 (for df1=1) to 9.88 (for df1=2). Dividing λ by .0625 gives N_min = 128 and 158, plus the 10% cell-balancing buffer.'",
    )

    # =========================================================================
    # SLIDE 10: GLOSSARY PART 3 — ANOVA FAMILY, F-RATIO, SPHERICITY (ε), INTERACTIONS & POST-HOC
    # =========================================================================
    s10 = prs.slides.add_slide(blank)
    add_header(
        s10,
        "GLOSSARY PART 3 (SLIDE 10 OF 16)",
        "Ground-Root Foundations 3: The ANOVA Family, F-Ratio, Sphericity (ε), Interactions & Post-Hoc",
        "Elementary Building Blocks Behind Defense Slides 14–15 and Result Tables in Slides 22, 27, 29–30 & 32–33",
    )
    add_card(
        s10, 0.22, 0.88, 6.35, 1.10,
        "Ground-Root Intuition A: Why Multiple t-Tests Fail (And How F Works)",
        [
            ("• Why 3 t-Tests Fail: ", "If you compare 3 groups (A vs B, B vs C, A vs C) with three separate t-tests at α = .05, your chance of at least one false alarm jumps to 1 − (0.95)³ = 14.3%! ANOVA tests all groups in ONE shot while keeping α = 5%.", "#C62828"),
            ("• What F = MS_between / MS_within Means: ", "F is simply a Signal-to-Noise ratio: (Spread between group averages) ÷ (Random scatter inside groups). F ≈ 1 means pure noise; F = 91 or 664 means massive treatment signal!", "#1B365D"),
        ],
        bg_hex="#E3F2FD", border_hex="#1565C0", font_size=7.4,
    )
    add_card(
        s10, 6.76, 0.88, 6.35, 1.10,
        "Ground-Root Intuition B: Main Effects vs. Interaction (A × B) on a Line Graph",
        [
            ("• Main Effect ('Overall Lever Effect'): ", "Does flipping Switch A (e.g., turning Rules Active) raise the outcome on average across the board?", "#00695C"),
            ("• Interaction Effect A × B ('It Depends!'): ", "Does the effect of Switch A depend on Switch B? Visually: PARALLEL lines = No Interaction; NON-PARALLEL / DIVERGING / CROSSING lines = Significant Interaction (e.g., Slide 29 Panel B leakage & Slide 32 turn compression)!", "#6A1B9A"),
        ],
        bg_hex="#F3E5F5", border_hex="#6A1B9A", font_size=7.4,
    )
    add_glossary_table(
        s10, 0.22, 2.04, 12.89, 4.45,
        headers=[
            "Concept / Symbol",
            "Elementary Ground-Root Meaning (Plain English — What Is It Really?)",
            "Where Used (Slides & RQ)",
            "Why Used Here (Problem Solved)",
            "Core Result Achieved in Paper",
        ],
        rows=[
            [
                "F-Statistic (F-Ratio)\nF = MS_between / MS_within",
                "• Ratio of Mean Square Between Groups (treatment signal variance) to Mean Square Within Groups (individual error noise).\n• Null baseline: F ≈ 1.0. Large F means group averages are far apart relative to internal scatter.",
                "Slides 14, 15, 22, 27,\n30, 33 (All 4 RQs)",
                "Quantifies the signal-to-noise ratio of the experimental manipulations across all 4 RQs.",
                "RQ1: F = 91.33; RQ2: F = 9.79 (Style) & 7.10 (Pacing); RQ3: F = 43.92, 34.82, 489.52; RQ4: F = 664.43 & 10.89 (all p < .001).",
            ],
            [
                "One-Way Between-\nSubjects ANOVA",
                "• Compares means of k ≥ 3 independent groups where different experimental units sit in each group.\n• Partitions total variance into SS_Between + SS_Within.",
                "Slides 14, 22\nRQ1 Algorithm Benchmark\n(Table 12)",
                "Tests whether K-Means, Ward, and HDBSCAN produce different Cosine Silhouette scores across 159 runs.",
                "Rejects H01: MiniLM F(2,156) = 91.33 (p < .001, η² = .539); Gemini Turn F = 77.09; Gemini Doc F = 127.47.",
            ],
            [
                "Repeated-Measures\nANOVA (RM-ANOVA)",
                "• Every subject (dialogue) is measured under ALL k conditions.\n• Subtracts out between-dialogue difficulty (SS_Subjects) from the error term, isolating pure within-dialogue differences.",
                "Slides 14, 15, 22, 27\nRQ2 (N=33 × 3 prompts)\n& RQ1 Matched Seeds",
                "Dialogues vary wildly in complexity; testing all 3 prompts on the exact same 33 dialogues removes dialogue noise.",
                "Refined RQ2 Style F(1.88, 60.29) = 9.79 (p < .001, ηp² = .234); Pacing F(1.30, 41.70) = 7.10 (p = .007, ηp² = .182).",
            ],
            [
                "Sphericity &\nGreenhouse–Geisser\nCorrection (ε / Epsilon)",
                "• Sphericity: RM-ANOVA assumes the variance of differences between every pair of conditions (A−B, A−C, B−C) is equal (ε = 1.0).\n• If unequal (ε < 1.0), standard F gives too many false positives. Multiplying df1 and df2 by ε makes the p-value exact and conservative.",
                "Slides 15, 18, 27\nRQ2 RM-ANOVA\n(Table 14)",
                "Pacing error has ε = 0.65 (strong sphericity departure) and Style has ε = 0.94; GG prevents inflated Type I error.",
                "Even after multiplying df by ε = 0.65 (df = 1.30, 41.70), Pacing Error remains highly significant (p = .007) and Style is p < .001.",
            ],
            [
                "Two-Way Factorial\nANOVA (2×2 & 2×3) &\nInteraction (A × B)",
                "• Crosses two independent factors simultaneously (Factor A × Factor B).\n• Simultaneously tests 3 hypotheses: (1) Main effect of A, (2) Main effect of B, and (3) Interaction A × B (whether A's impact depends on B).",
                "Slides 14, 15, 28–30 (RQ3)\nSlides 31–33 (RQ4)",
                "RQ3 crosses Rules × Prompting (2×2); RQ4 crosses Prompting × Archetype (2×3) to test moderation/synergy.",
                "RQ3 Protective Leakage Interaction: F(1,140) = 34.82 (p < .001). RQ4 Turn Compression Interaction: F(2,174) = 10.89 (p < .001).",
            ],
            [
                "Post-Hoc Pairwise Tests:\nTukey HSD, Games–Howell\n& Holm Step-Down",
                "• Omnibus ANOVA only says 'at least one group differs.' Post-hoc tests check every specific pair (A vs B, B vs C) while keeping familywise α ≤ .05:\n  • Tukey HSD: equal variances (RQ1).\n  • Games–Howell: unequal variances (RQ1).\n  • Holm Step-Down: sequential Bonferroni for paired t-tests (RQ2).",
                "Slides 14, 22 (RQ1)\nSlide 27 (RQ2 Table E3)",
                "Pinpoints exactly which algorithm or prompting strategy beats which baseline without inflating false positives.",
                "RQ1: K-Means > Ward (Tukey & Games–Howell p < .001). RQ2: Cluster-Adaptive > Static (+31.8%, p_Holm < .001) & > Zero-Shot (p_Holm = .049).",
            ],
        ],
        col_widths=[1.85, 3.85, 1.55, 2.55, 3.09],
        font_size=7.1,
    )
    add_bottom_banner(
        s10,
        "How Slide 10 Unlocks Defense Slides 14–15, 27, 29 & 32: Tell the committee: 'Each RQ uses the exact ANOVA structure matching its design: One-Way for 3 independent algorithms (RQ1), Greenhouse–Geisser RM-ANOVA for 3 prompts on the same 33 dialogues (RQ2), 2×2 Factorial for Rules × Prompt (RQ3), and 2×3 Factorial for Prompt × Persona (RQ4).'",
    )

    # =========================================================================
    # SLIDE 11: GLOSSARY PART 4 — EFFECT SIZES EXPLAINED (η², ηp², COHEN'S f, d, d_z, CRAMÉR'S V)
    # =========================================================================
    s11 = prs.slides.add_slide(blank)
    add_header(
        s11,
        "GLOSSARY PART 4 (SLIDE 11 OF 16)",
        "Ground-Root Foundations 4: Every Effect Size Metric Explained (η², ηp², Cohen's f, d, d_z, V)",
        "Elementary Building Blocks Behind Defense Slides 15, 17–18, 22–24, 27, 30 & 33 (Practical Magnitude vs. p-Values)",
    )
    add_card(
        s11, 0.22, 0.88, 6.35, 1.10,
        "Ground-Root Intuition A: Why p-Values Are Not Enough (Statistical vs. Practical Significance)",
        [
            ("• The Limitation of p < .001: ", "A p-value only tells you that an effect is 'not zero.' With a huge sample (say N = 10,000), a useless 0.02-turn improvement can have p < .001!", "#C62828"),
            ("• What Effect Size Tells You: ", "Effect size measures HOW BIG the improvement is on a standardized scale that does NOT depend on sample size—telling businesses whether the gain is trivial (Small), noticeable (Medium), or transformative (Large).", "#1B5E20"),
        ],
        bg_hex="#E8F5E9", border_hex="#2E7D32", font_size=7.4,
    )
    add_card(
        s11, 6.76, 0.88, 6.35, 1.10,
        "Ground-Root Intuition B: The 3 Families of Effect Sizes Used in the Study",
        [
            ("1. Variance-Explained Family (η², ηp², f): ", "Used in ANOVA—asks 'What % of total/error variance in the outcome is explained by this factor?' (.01 Small, .06 Medium, .14+ Large).", "#1B365D"),
            ("2. Standardized Mean-Shift Family (Cohen's d, d_z): ", "Used in pairwise contrasts—asks 'How many standard deviations apart are the two group averages?' (0.2 Small, 0.5 Medium, 0.8+ Large).", "#1565C0"),
            ("3. Categorical Table Association (Cramér's V): ", "Used on cross-tabs—asks 'How strongly do two category labels co-occur from 0 to 1?'", "#6A1B9A"),
        ],
        bg_hex="#E3F2FD", border_hex="#1565C0", font_size=7.3,
    )
    add_glossary_table(
        s11, 0.22, 2.04, 12.89, 4.45,
        headers=[
            "Concept / Symbol",
            "Elementary Ground-Root Meaning (Plain English — What Is It Really?)",
            "Where Used (Slides & RQ)",
            "Why Used Here (Problem Solved)",
            "Core Result Achieved in Paper",
        ],
        rows=[
            [
                "Eta-Squared (η²)\nη² = SS_between / SS_total",
                "• Proportion (0% to 100%) of total outcome variance explained by group membership in One-Way ANOVA.\n• Cohen's benchmarks: .01 (1% Small), .06 (6% Medium), ≥ .14 (14%+ Large).",
                "Slides 15, 22\nRQ1 One-Way ANOVA\n(Table 12)",
                "Shows what share of Silhouette variance is driven by algorithm choice vs. random subsample noise.",
                "RQ1 Algorithm η² = .539 (MiniLM), .497 (Gemini Turn), and .620 (Gemini Doc)—explaining 50%–62% of total variance (Huge!).",
            ],
            [
                "Partial Eta-Squared (ηp²)\nSS_eff / (SS_eff + SS_err)",
                "• In multi-factor (2×2, 2×3) or RM-ANOVA, isolates one factor's variance as a share of (that factor + error), excluding other factors.\n• Benchmarks: .01 Small, .06 Medium, ≥ .14 Large.",
                "Slides 15, 22, 27, 30, 33\nRQ1–RQ4 (Tables 12–16)",
                "Standard effect size for RM-ANOVA (RQ2) and Factorial ANOVA (RQ3, RQ4) so factors can be compared fairly.",
                "All primary effects are Large: RQ2 Style ηp² = .234, Pacing ηp² = .182; RQ3 RAR ηp² = .239, Slot F1 ηp² = .778; RQ4 Turns ηp² = .793!",
            ],
            [
                "Cohen's f\nf = √[η² / (1 − η²)]",
                "• Ratio of the standard deviation of group means (σ_means) to the within-group standard deviation (σ_error).\n• Benchmarks: f = .10 Small, f = .25 Medium (≈ 6% variance), f = .40 Large (≈ 14% variance).",
                "Slides 15, 17, 18\nSample-Size Power Design\n(Section 3.2, Table 4)",
                "Direct input into the noncentral-F power equation λ = f²·N to size all four experiments a priori.",
                "Planned at f = .25 (Medium); actual observed effects in RQ1–RQ4 correspond to f = 0.47 to 1.96 (2× to 8× larger than planned!).",
            ],
            [
                "Cohen's d\n(Ȳ1 − Ȳ2) / SD_pooled",
                "• Number of standard deviations separating two independent group means.\n• Benchmarks: |d| = 0.20 Small, 0.50 Medium, ≥ 0.80 Large.",
                "Slides 8, 33\nRQ4 Simple Contrasts\n(Table 16)",
                "Quantifies the magnitude of turn reduction within each of the 3 traveler archetypes.",
                "RQ4 Turn Reductions: Decisive Booker d = −3.94, Rigid Seeker d = −3.40, Open Explorer d = −2.55 (3 to 4 SDs below baseline!).",
            ],
            [
                "Cohen's d_z (Paired)\nΔ̄ / SD_diff",
                "• Within-subject standardized mean difference for paired data: divides average within-dialogue improvement Δ̄ by the SD of the paired differences.\n• Benchmarks: 0.20 Small, 0.50 Medium, ≥ 0.80 Large.",
                "Slide 27\nRQ2 Holm Pairwise\nContrasts (Table E3)",
                "Accounts for within-dialogue pairing across the 33 held-out dialogues in RQ2.",
                "Cluster-Adaptive vs. Static Few-Shot: d_z = 0.74 (Medium-to-Large); Cluster-Adaptive vs. Zero-Shot: d_z = 0.41.",
            ],
            [
                "Cramér's V (∈ [0, 1])\n√[χ² / (N · min(R−1, C−1))]",
                "• Measures strength of association between two categorical variables in a contingency table: 0 = completely independent, 1 = perfectly predictive.",
                "Slides 19, 23, 24\nRQ1 Diagnostic & Audit\n(Tables D3, D5, D6)",
                "Diagnoses wizard confounding (Cluster × Wizard ID) and outcome confounding/validity (Cluster × Booking Outcome).",
                "Diagnosed whole-chat wizard confounding (V = .45); proved M=9 prefix limits outcome leakage during clustering (V = .20) while predicting final booking behavior (V = .454).",
            ],
        ],
        col_widths=[1.85, 3.85, 1.55, 2.55, 3.09],
        font_size=7.1,
    )
    add_bottom_banner(
        s11,
        "How Slide 11 Unlocks Defense Slides 15, 27, 30 & 33: Tell the committee: 'The study was designed to detect medium effects (Cohen's f = .25, or η² ≈ .06), and the empirical results achieved Large effect sizes across every single RQ: ηp² = .234 in RQ2, ηp² = .239–.778 in RQ3, and ηp² = .793 (d = −2.55 to −3.94) in RQ4.'",
    )

    # =========================================================================
    # SLIDE 12: GLOSSARY PART 5 — ROBUST & NON-PARAMETRIC "BULLETPROOF" TESTS
    # =========================================================================
    s12 = prs.slides.add_slide(blank)
    add_header(
        s12,
        "GLOSSARY PART 5 (SLIDE 12 OF 16)",
        "Ground-Root Foundations 5: Heteroscedasticity, Welch, HC3 & Rank Non-Parametric Tests",
        "Elementary Building Blocks Behind Defense Slides 14, 16, 22, 27, 30 & 33 (Why 3-Tier Inference Is Bulletproof)",
    )
    add_card(
        s12, 0.22, 0.88, 6.35, 1.10,
        "Ground-Root Intuition A: What 'Heteroscedasticity' Means & Why Zero-Leakage Causes It",
        [
            ("• Homoscedasticity (Equal Spread) vs. Heteroscedasticity (Unequal Spread): ", "Classical OLS ANOVA assumes every cell has roughly the same scatter (SD). When the guardrail drives entity leakage to 0.0% in Cell 4 (SD = .000) while Cell 2 has 35.9% leakage (SD = .348), the spreads are wildly unequal—that's heteroscedasticity!", "#C62828"),
            ("• How Welch & HC3 Fix It: ", "Instead of averaging all cell variances together, Welch's ANOVA and MacKinnon–White HC3 compute separate error variances for each cell/observation!", "#E65100"),
        ],
        bg_hex="#FFF8E1", border_hex="#F57F17", font_size=7.4,
    )
    add_card(
        s12, 6.76, 0.88, 6.35, 1.10,
        "Ground-Root Intuition B: How Non-Parametric Rank Tests (Kruskal, Friedman, ART) Work",
        [
            ("• The Trick of Ranking (1st, 2nd, 3rd...): ", "Non-parametric tests throw away raw decimal assumptions and sort the scores from smallest to largest (Rank 1 to Rank N). Because ranks are evenly spaced integers, skewness, floor/ceiling bounds [0,1], and outliers cannot distort the test!", "#1B5E20"),
            ("• Why Aligned Rank Transform (ART) Is Special: ", "Ordinary rank tests cannot test 2×2 or 2×3 interactions. ART subtracts out main effects first ('aligning'), ranks the residuals, and runs exact factorial ANOVA!", "#1B365D"),
        ],
        bg_hex="#E8F5E9", border_hex="#2E7D32", font_size=7.4,
    )
    add_glossary_table(
        s12, 0.22, 2.04, 12.89, 4.45,
        headers=[
            "Concept / Symbol",
            "Elementary Ground-Root Meaning (Plain English — What Is It Really?)",
            "Where Used (Slides & RQ)",
            "Why Used Here (Problem Solved)",
            "Core Result Achieved in Paper",
        ],
        rows=[
            [
                "Heteroscedasticity\n(Unequal Cell Variances)",
                "• Violation of standard ANOVA's equal-variance assumption across groups.\n• Naturally happens whenever an intervention hits a hard floor/ceiling (e.g., 0.0% leakage in RQ3 or 5.00-turn floor with SD = 0.00 in RQ4).",
                "Slides 16, 22, 30, 33\nRQ1, RQ3, RQ4",
                "Recognizes that zero-variance floor cells violate textbook OLS pooling assumptions.",
                "Addressed proactively via Tier-2 (Welch / HC3) and Tier-3 (Kruskal / Mann–Whitney / ART) tests across all RQs.",
            ],
            [
                "Welch's ANOVA &\nWelch's t-Test",
                "• Weights each group mean by the inverse of its own variance (w_j = n_j / s_j²) and adjusts degrees of freedom downward via Satterthwaite's formula.\n• Does NOT assume groups have equal SDs.",
                "Slides 14, 16, 22 (RQ1)\nSlide 30 (RQ3), Slide 33 (RQ4)",
                "RQ1 HDBSCAN has 2.3× higher SD than K-Means (.044 vs .019); RQ4 cells have unequal SDs.",
                "RQ1 Welch F(2, 89.15) = 66.98 (p < .001); RQ3 Leakage Welch t(35) = 5.90 (p < .001); RQ4 Welch t_log = −18.92, −10.97, −17.02 (all p < .001).",
            ],
            [
                "MacKinnon–White HC3\nSandwich Standard Errors",
                "• Heteroscedasticity-Consistent covariance matrix ('HC3') for regression/factorial ANOVA that estimates error variance point-by-point with finite-sample leverage penalty (1 − h_i)⁻².",
                "Slides 14, 16, 30, 33\nRQ3 (Table 15) &\nRQ4 (Table 16)",
                "Provides exact factorial main & interaction F-tests even when cells have SD = 0.000 (floor effects).",
                "RQ3: RAR HC3 F = 42.71, Leakage Sum-HC3 F = 33.85, Slot F1 HC3 F = 471.70 (all p < .001). RQ4: Prompt HC3 F = 681.53, Interaction HC3 F = 8.58 (p < .001).",
            ],
            [
                "Kruskal–Wallis H Test\n(Rank One-Way ANOVA)",
                "• Non-parametric partner of One-Way Between-Subjects ANOVA.\n• Ranks all N = 159 observations from 1 to 159 across all groups combined and tests if mean ranks differ (distributed as χ² with k − 1 df).",
                "Slides 14, 16, 22\nRQ1 Benchmark\n(Table 12)",
                "Verifies RQ1 algorithm differences without assuming normal Silhouette distributions.",
                "RQ1 MiniLM Kruskal–Wallis H(2) = 86.82, p < .001 (100% agreement with parametric F = 91.33).",
            ],
            [
                "Friedman Rank Test (χ²_F)\n(Rank RM-ANOVA)",
                "• Non-parametric partner of Repeated-Measures ANOVA.\n• Ranks the k = 3 conditions (1, 2, 3) INSIDE each dialogue/seed separately, then tests whether one condition consistently wins better ranks.",
                "Slides 14, 16, 22, 27\nRQ1 Matched Seeds &\nRQ2 (Table 14)",
                "Immune to cosine similarity skewness or extreme outlier dialogues in within-subject designs.",
                "RQ1 Matched Friedman χ²(2) = 56.30 (p < .001). RQ2 Refined Style χ²(2) = 12.50 (p = .002) & Pacing χ²(2) = 14.27 (p < .001).",
            ],
            [
                "Mann–Whitney U &\nAligned Rank Transform\n(ART) Factorial ANOVA",
                "• Mann–Whitney U: Two-group rank-sum test (U = 0.0 means 100% of Group A beat 100% of Group B!).\n• ART ANOVA (Wobbrock et al., 2011): Strips out other factors' effects ('aligns' residuals), ranks them, and runs factorial ANOVA on main & interaction effects.",
                "Slides 14, 16, 30, 33\nRQ3 (2×2) & RQ4 (2×3)\n(Tables 15 & 16)",
                "Bounded [0, 1] rates (RAR, ELR, RER) and skewed turn counts require distribution-free factorial interaction tests.",
                "RQ3 Leakage Interaction ART F = 2148.81 (p < .001), U = 1008.0. RQ4 Prompt ART F = 224.22, Interaction ART F = 209.46 (p < .001), U = 0.0, 40.5, 0.0!",
            ],
        ],
        col_widths=[1.85, 3.85, 1.55, 2.55, 3.09],
        font_size=7.0,
    )
    add_bottom_banner(
        s12,
        "How Slide 12 Unlocks Defense Slide 16: If a committee statistician challenges normality or zero-variance floor cells, reply: 'Slide 16 shows 3-Tier Triangulation: every hypothesis is tested simultaneously via (1) Parametric OLS/GG, (2) Heteroscedasticity-Robust Welch/HC3, and (3) Non-Parametric Rank Kruskal/Friedman/ART—all reaching p < .001.'",
    )

    # =========================================================================
    # SLIDE 13: GLOSSARY PART 6 — UNSUPERVISED CLUSTERING ALGORITHMS & VALIDITY METRICS
    # =========================================================================
    s13 = prs.slides.add_slide(blank)
    add_header(
        s13,
        "GLOSSARY PART 6 (SLIDE 13 OF 16)",
        "Ground-Root Foundations 6: Clustering Algorithms & Validity Metrics (Silhouette, DB, ARI, UMAP)",
        "Elementary Building Blocks Behind Defense Slides 22–25 (RQ1 Algorithm Benchmark, Cross-Corpus UMAP & Truncation Grid)",
    )
    add_card(
        s13, 0.22, 0.88, 6.35, 1.10,
        "Ground-Root Intuition A: How K-Means, Ward, and HDBSCAN Differ Fundamentally",
        [
            ("• K-Means (Centroid Partitioning — 100% Coverage): ", "Drops k = 3 'gravity centers' (centroids) into the data, assigns every customer to their nearest center, and shifts centers to the group average until stable. Every customer gets a cluster!", "#1565C0"),
            ("• Ward (Bottom-Up Tree) vs. HDBSCAN (Density Islands + 'Noise'): ", "Ward merges pairs of points that keep variance smallest. HDBSCAN only groups dense crowds and throws away 36%–39% of customers in sparser regions as '-1 Noise' (unusable when a live bot must serve 100% of users!).", "#C62828"),
        ],
        bg_hex="#E3F2FD", border_hex="#1565C0", font_size=7.3,
    )
    add_card(
        s13, 6.76, 0.88, 6.35, 1.10,
        "Ground-Root Intuition B: Judging Cluster Quality Without Pre-Existing Labels",
        [
            ("• Internal Geometry (Silhouette ↑ vs. Davies–Bouldin ↓): ", "Do members of the same cluster sit close together (small 'a') and far from other clusters (large 'b')? Silhouette (higher is better) and Davies–Bouldin (lower is better) measure this geometry.", "#6A1B9A"),
            ("• Resampling Stability (Bootstrap ARI ↑): ", "Drawing 100 random 80% subsamples of the dataset and re-running K-Means tests whether the same pairs of customers still land in the same cluster. ARI = .89 proves the clusters are rock-solid!", "#1B5E20"),
        ],
        bg_hex="#E8F5E9", border_hex="#2E7D32", font_size=7.3,
    )
    add_glossary_table(
        s13, 0.22, 2.04, 12.89, 4.45,
        headers=[
            "Concept / Symbol",
            "Elementary Ground-Root Meaning (Plain English — What Is It Really?)",
            "Where Used (Slides & RQ)",
            "Why Used Here (Problem Solved)",
            "Core Result Achieved in Paper",
        ],
        rows=[
            [
                "K-Means Clustering\n(k = 3 Centroids)",
                "• Partitions N points into k clusters by minimizing within-cluster sum of squared distances to k cluster centroids (μ_1..μ_k).\n• Guarantees 100% assignment coverage (0% dropped noise) and enforces ≥20% minimum cluster size at k = 3.",
                "Slides 22–25\nRQ1 Operational Winner\n(Tables 12, 13)",
                "Live chatbot routing requires 100% of incoming users to be assigned to an actionable persona.",
                "Selected k = 3 (45.0% Decisive Booker, 25.5% Open Explorer, 29.5% Rigid Seeker); beats Ward (p < .001) with 0% noise loss.",
            ],
            [
                "Ward's Agglomerative &\nHDBSCAN Clustering",
                "• Ward: Hierarchical bottom-up merging that minimizes within-cluster variance increase at each step.\n• HDBSCAN: Density-based clustering that extracts dense cores and rejects lower-density boundary points as unclustered noise (−1).",
                "Slide 22 (Table 12)\nRQ1 Algorithm Benchmark",
                "Benchmarks centroid partitioning (K-Means) against hierarchical (Ward) and density-based (HDBSCAN) paradigms.",
                "Ward Silhouette = .118 (< K-Means .147, p < .001). HDBSCAN gets .211–.345 ONLY after discarding 25.7%–39.1% of dialogues as noise!",
            ],
            [
                "Cosine Distance &\nCosine Silhouette\ns(i) = (b − a) / max(a,b)",
                "• Cosine Distance: 1 − cos(θ) (measures angle between vectors regardless of vector length).\n• Silhouette s(i) ∈ [−1, +1]: Compares average distance to own cluster (a) vs. nearest other cluster (b). +1 = tight & separated; 0 = on boundary; <0 = wrong cluster.",
                "Slides 22, 24\nRQ1 Primary DV\n(Figures D1–D2, Table 12)",
                "Quantifies internal cluster cohesion vs. separation in high-dimensional embedding spaces.",
                "K-Means Silhouette = .147 (MiniLM), .158 (Gemini Turn), .161 (Gemini Doc) vs. −.013 Permutation Null (F = 91.33, p < .001).",
            ],
            [
                "Davies–Bouldin Index\n(DBI ↓ — Lower Is Better)",
                "• Average ratio of (within-cluster scatter s_i + s_j) divided by (distance between cluster centroids d_ij) for each cluster and its closest neighbor.\n• LOWER DBI = tighter clusters that are farther apart!",
                "Slides 22, 24\nRQ1 Secondary Validity\n(Tables 12 & D6)",
                "Complements Silhouette by penalizing overlapping centroid neighborhoods.",
                "On 46-d Blocks (M=9), k = 3 achieves the lowest (best) Davies–Bouldin Index (DBI = 2.647) across k = 2..6.",
            ],
            [
                "Adjusted Rand Index\n(ARI ∈ [−1, 1]) &\nBootstrap Stability",
                "• Measures pairwise agreement between two clusterings (what fraction of dialogue pairs are grouped together in both runs), adjusted so random guessing = 0.0 and identical clustering = 1.0.\n• Bootstrap ARI: Mean ARI across 60–100 random subsamples vs. full D_gold.",
                "Slides 19, 24\nRQ1 Truncation & Ablation\n(Figure D4, Tables D5–D6)",
                "Tests whether discovered personas are genuine, reproducible population structures (ARI ≥ .60 threshold).",
                "Embeddings-only at M=9 gets ARI = .39 (unstable); hybrid 46-d Blocks at M=9 jumps to ARI = .89 (.87 in 6-config ablation; 93.1% core membership)!",
            ],
            [
                "Permutation Baseline &\nUMAP 2D Projection",
                "• Permutation Baseline: Randomly shuffles cluster IDs across dialogues 53 times to prove what 'zero real structure' looks like (Silhouette = −.013).\n• UMAP: Non-linear neighborhood-preserving projection from 384-d/46-d to 2D for visual scatter plots.",
                "Slides 22, 23\nFigures D2 & D3\n(Cross-Corpus Check)",
                "Permutation proves statistical significance over chance; UMAP visualizes Golden vs. Test vs. MultiWOZ overlap.",
                "Frames Golden (.466) & Test (.467) overlap perfectly on UMAP (p = .923), while MultiWOZ drops to .269 (p < .001, 0.1% Explorers).",
            ],
        ],
        col_widths=[1.85, 3.85, 1.55, 2.55, 3.09],
        font_size=7.0,
    )
    add_bottom_banner(
        s13,
        "How Slide 13 Unlocks Defense Slides 22–24: If asked 'Why not use HDBSCAN since its Silhouette (.211) is higher than K-Means (.147)?', answer: 'HDBSCAN achieves .211 only by throwing away 39.1% of customers as unclustered noise! K-Means (k=3) routes 100% of customers and achieves ARI = .89 stability and DBI = 2.647 on the 46-d Blocks space.'",
    )

    # =========================================================================
    # SLIDE 14: GLOSSARY PART 7 — AGREEMENT METRICS (κ, κ_w, PABAK) & DOMAIN HYPERPARAMETERS (λ_d, M, LOGREG)
    # =========================================================================
    s14 = prs.slides.add_slide(blank)
    add_header(
        s14,
        "GLOSSARY PART 7 (SLIDE 14 OF 16)",
        "Ground-Root Foundations 7: Cohen's Kappa (κ, κ_w, PABAK), Decay λ_d, Prefix M & LogReg",
        "Elementary Building Blocks Behind Defense Slides 19, 23–25, 28 & 31 (Routing, Inter-Rater Reliability & Domain Parameters)",
    )
    add_card(
        s14, 0.22, 0.88, 6.35, 1.10,
        "Ground-Root Intuition A: Why Raw Accuracy (%) Is Misleading & How Cohen's κ Fixes It",
        [
            ("• The Problem with Raw Agreement (p_o): ", "If two judges (or a router) classify items into 3 categories, blind random guessing already agrees ~35% of the time (p_e = .354). Saying '59% accuracy' sounds okay, but almost two-thirds of that is pure luck!", "#C62828"),
            ("• What Cohen's Kappa κ = (p_o − p_e) / (1 − p_e) Measures: ", "Kappa subtracts out random chance p_e and asks: 'Of the remaining gap between chance and 100% perfection, what fraction was actually captured?' (0 = chance, .40–.60 Moderate, .60–.80 Substantial, >.80 Almost Perfect).", "#1B5E20"),
        ],
        bg_hex="#E8F5E9", border_hex="#2E7D32", font_size=7.3,
    )
    add_card(
        s14, 6.76, 0.88, 6.35, 1.10,
        "Ground-Root Intuition B: Do Not Confuse the TWO Different 'Lambdas' (λ vs. λ_d) in the Study!",
        [
            ("1. Statistical Power Lambda (λ = f²·N on Slides 17–18): ", "Noncentrality shift of the F-distribution bell curve used to calculate sample sizes N = 159, 33, 144, 180 (values: λ = 8.00 to 10.50).", "#1565C0"),
            ("2. Turn-Recency Decay Lambda (λ_d = 0.15 on Slide 19, Eq. 2): ", "Exponential weight w_t ∝ exp(−0.15·(T − t)) when pooling turn embeddings so recent negotiation turns weigh more than 'Hi!' at Turn 1.", "#6A1B9A"),
        ],
        bg_hex="#F3E5F5", border_hex="#6A1B9A", font_size=7.3,
    )
    add_glossary_table(
        s14, 0.22, 2.04, 12.89, 4.45,
        headers=[
            "Concept / Symbol",
            "Elementary Ground-Root Meaning (Plain English — What Is It Really?)",
            "Where Used (Slides & RQ)",
            "Why Used Here (Problem Solved)",
            "Core Result Achieved in Paper",
        ],
        rows=[
            [
                "Cohen's Kappa (κ)\nκ = (p_o − p_e) / (1 − p_e)",
                "• Chance-corrected agreement between two categorical raters or between predicted and reference labels.\n• p_o = observed raw agreement; p_e = expected agreement by random chance.",
                "Slides 23–26 (RQ1/RQ2)\nSlide 28 (RQ3 Judges)\nSlide 31 (RQ4 Audit)",
                "Evaluates early-turn prefix routing, cross-model judge agreement, and blind persona classification above chance.",
                "RQ1 Routing: κ=.359 (m=3) → .535 (m=5) → .722 (m=7) → .958 (m=9). RQ3 Dual-Judge: κ=.917 (vs Regex κ=.861). RQ4 Simulator: κ=.933!",
            ],
            [
                "Quadratic Weighted\nKappa (κ_w)",
                "• Version of Cohen's κ for ordinal 1–5 scales where disagreements are weighted by squared distance (i − j)².\n• Being off by 1 point (4 vs 5) is a tiny penalty (1²=1); being off by 4 points (1 vs 5) is a 16× penalty (4²=16).",
                "Slide 24 (Table C2)\nRQ1 16-Field Codebook\nTest–Retest Audit",
                "Ordinal 1–5 behavioral ratings (flexibility, decisiveness, price sensitivity) have ordered severity.",
                "Blind test–retest audit achieves κ_w = .87 to .96 (mean .91) across all 10 ordinal behavioral scales.",
            ],
            [
                "PABAK (2·p_o − 1)\n& Exact Binomial Test",
                "• PABAK (Prevalence-Adjusted Bias-Adjusted Kappa): Adjusts κ when one category (e.g., 94% compliant) dominates prevalence.\n• Exact Binomial Test: Exact probability of getting ≥43/45 correct classifications when random chance is 1/3.",
                "Slide 28 (RQ3 Table C3)\nSlide 31 (RQ4 Persona\nAudit Table C3)",
                "Confirm that high agreement isn't distorted by class imbalance or small audit sample size.",
                "RQ3 Dual-Judge PABAK = .917 (95.8% raw agreement). RQ4 Persona Audit: 43/45 correct (95.6%), exact binomial p = 1.37 × 10⁻¹⁸!",
            ],
            [
                "Exponential Turn Decay\n(λ_d = 0.15, Eq. 2)\nw_t ∝ exp[−λ_d(T − t)]",
                "• Weights each turn embedding e_t by how close turn t is to the current turn T.\n• At λ_d = 0.15: current turn weight = 1.00, 3 turns ago = 0.64, 10 turns ago = 0.22.",
                "Slide 19 (Defense Q2)\nSection 3.3 (Eq. 2)\nstep2b sensitivity grid",
                "Prevents Turn 1 greetings ('Hello!') from diluting active constraint negotiation while keeping early trip facts.",
                "Outperforms uniform mean (λ_d = 0) and memoryless last-turn (λ_d ≥ 1), and motivates the hybrid 46-d Blocks representation.",
            ],
            [
                "Truncation Horizon\n(M = 9 User Messages)\n& Reference Labels y^(9)",
                "• Cuts off every conversation after the first M = 9 user messages (~17 total turns) before clustering.\n• y^(9): Unsupervised K-Means (k=3) cluster assignments on the M=9 46-d Blocks space.",
                "Slides 19, 24, 25\nRQ1 Discovery & Routing\n(Tables D5, 13)",
                "Clustering full chats leaks the final outcome ('Booked!' vs 'Too pricey', V = .29); M=9 captures pure shopping style.",
                "At M = 9, 62.4% of long dialogues are truncated, bootstrap stability peaks at ARI = .89, and same-feature routing consistency hits 97.3% (κ = .958).",
            ],
            [
                "Regularized Multinomial\nLogistic Regression\nP(c | X^(m)) = Softmax(W·X)",
                "• Supervised linear classifier that learns a (3 × 46) weight matrix W^(m) mapping early prefix features X^(m) to probabilities for the 3 archetypes.\n• L1/L2 regularization shrinks noisy feature weights so the model generalizes to unseen D_test.",
                "Slides 11, 20, 24, 25\nRefinedArchetypeRouter\n(routing.py)",
                "Unsupervised K-Means weights all 46 features equally and fails at M=3,5 when late features are still 0; LogReg up-weights early cues!",
                "Lifts held-out prefix routing from κ = .24 (primary whole-chat) to κ = .535 (70.1% at M=5 runtime) and κ = .722 (82.0% at M=7).",
            ],
        ],
        col_widths=[1.85, 3.85, 1.55, 2.55, 3.09],
        font_size=7.0,
    )
    add_bottom_banner(
        s14,
        "How Slide 14 Unlocks Defense Slides 19, 24–25, 28 & 31: Remember two key points for the committee: (1) Distinguish Power λ = f²·N (Slides 17–18) from Turn Decay λ_d = 0.15 (Slide 19); (2) At M=9, κ = .958 (97.3%) measures boundary consistency with unsupervised reference labels y^(9), while M=5 (κ = .535, 70.1%) is the genuine early-prefix runtime router.",
    )

    # =========================================================================
    # SLIDE 15: GLOSSARY PART 8 — NLP EMBEDDINGS, FAISS & DOMAIN EVALUATION METRICS
    # =========================================================================
    s15 = prs.slides.add_slide(blank)
    add_header(
        s15,
        "GLOSSARY PART 8 (SLIDE 15 OF 16)",
        "Ground-Root Foundations 8: NLP Embeddings, FAISS & Domain Metrics (RAR, ELR, Slot F1, TGC, RER)",
        "Elementary Building Blocks Behind Defense Slides 11, 20, 26–33 (How Chatbot Text Is Indexed, Guarded & Scored)",
    )
    add_card(
        s15, 0.22, 0.88, 6.35, 1.10,
        "Ground-Root Intuition A: Embeddings, FAISS IndexFlatIP & Why [SLOT] Masking Is Essential",
        [
            ("• Text Embeddings (MiniLM 384-d vs. Gemini 3,072-d): ", "Neural networks that turn a sentence into a list of 384 or 3,072 coordinates so sentences with similar tone/meaning point at the same angle (high cosine dot product).", "#1B365D"),
            ("• FAISS IndexFlatIP + [SLOT] Masking: ", "FAISS searches D_gold for the k = 3 closest human wizard examples in < 1 ms. Without masking hotel names/prices with [SLOT], the LLM copies stale examples ('Sapphire Bay Resort', '$1,149') into the new user's chat (35.9% leakage)!", "#C62828"),
        ],
        bg_hex="#E3F2FD", border_hex="#1565C0", font_size=7.3,
    )
    add_card(
        s15, 6.76, 0.88, 6.35, 1.10,
        "Ground-Root Intuition B: Why SBERT Style Cosine Moves in RQ2 While BERTScore Stays Flat",
        [
            ("• All 3 Prompts Reply to the Exact Same Travel Question: ", "Because Zero-Shot, Static, and Cluster-Adaptive all talk about the same user trip, broad topical embeddings (Gemini 3,072-d, p = .200) and token overlap (BERTScore F1, p = .243) stay flat at .78–.85.", "#6A1B9A"),
            ("• De-Lexicalized SBERT + Pacing Measure HOW It Is Said: ", "Once city/date/price names are masked ([CITY], [DATE], [PRICE]), sentence-level SBERT (MiniLM-384d, p < .001) and Pacing Error (p = .007) isolate conversational phrasing and conciseness!", "#1B5E20"),
        ],
        bg_hex="#E8F5E9", border_hex="#2E7D32", font_size=7.3,
    )
    add_glossary_table(
        s15, 0.22, 2.04, 12.89, 4.45,
        headers=[
            "Concept / Symbol",
            "Elementary Ground-Root Meaning (Plain English — What Is It Really?)",
            "Where Used (Slides & RQ)",
            "Why Used Here (Problem Solved)",
            "Core Result Achieved in Paper",
        ],
        rows=[
            [
                "MiniLM-384d vs.\nGemini-3072d &\nBERTScore F1",
                "• all-MiniLM-L6-v2 (384-d): Sentence-level bi-encoder sensitive to phrasing/syntax.\n• gemini-embedding-001 (3,072-d): High-capacity semantic document encoder.\n• BERTScore F1: Token-by-token contextual embedding precision/recall harmonic mean.",
                "Slides 22, 24 (RQ1)\nSlide 27 (RQ2 Table 14)\nSlide 30 (RQ3 Style)",
                "Contrasts sentence-level stylistic convergence against broad topical invariance.",
                "RQ2 De-lexicalized SBERT Style Cosine jumps to .597 (+31.8% over Static .453, F = 9.79, p < .001), while Gemini (.796) & BERTScore (.852) confirm topic preservation.",
            ],
            [
                "FAISS IndexFlatIP &\nDe-Lexicalization /\n[SLOT] Masking",
                "• FAISS IndexFlatIP: Exact inner-product search over L2-normalized vectors (equals exact cosine similarity).\n• De-lexicalization / [SLOT] Masking: Regex replacement of cities, dates, dollar amounts & promo codes with [SLOT] / [CITY] / [PRICE].",
                "Slides 11, 20, 26–30\nRQ2 Retrieval & Scoring\nRQ3 Leakage Prevention",
                "Prevents retrieval from matching surface city names and stops the LLM from hallucinating foreign exemplar entities.",
                "Partitioning FAISS into 3 archetype sub-indices + [SLOT] masking lifts style by +31.8% (RQ2) and cuts entity leakage from 35.9% to 0.0% (RQ3).",
            ],
            [
                "Pacing Calibration Error\n(word_abs_err)",
                "• Absolute difference in words between the chatbot's reply and the target archetype's human consultant norm: |Words(ŷ) − μ_Words(Archetype)|.\n• Human norms: 12.9w (Decisive), 18.6w (Explorer), 14.8w (Rigid).",
                "Slides 26, 27\nRQ2 Table 14\n(metrics.py)",
                "Measures whether the bot adapts its verbosity to fast bookers vs. exploratory shoppers.",
                "Cuts pacing error from 10.12 words (Zero-Shot) and 6.33 words (Static) down to 3.87 words (Cluster-Adaptive, F = 7.10, p = .007).",
            ],
            [
                "Rule Adherence (RAR):\nViolation Sensitivity vs.\nCompliant Specificity",
                "• RAR: Binary score (1 = correct policy handling, 0 = failure) across 5 YAML rules.\n• Violation Sensitivity: % of rule-violating requests correctly blocked/warned.\n• Compliant Specificity: % of valid requests accepted without false alarms.",
                "Slides 28, 29, 30\nRQ3 Primary DV\n(Tables 9 & 15, Fig 7A)",
                "Separates catching real policy violations (Sensitivity) from avoiding false-positive blocks on valid trips (Specificity).",
                "Rules Active raises overall RAR from .500 to .944/.931 (F = 43.92, p < .001) by lifting Violation Sensitivity from 5.6% to 98.6% (F = 498.78) while keeping Specificity high (88.9% vs 94.4%, p = .408).",
            ],
            [
                "Exemplar Leakage (ELR)\n& Factual Slot Coverage\nF1 (2·P·R / (P+R))",
                "• ELR ∈ [0, 1]: Fraction of foreign entities from retrieved few-shot exemplars that leak into the active reply.\n• Slot Coverage F1 ∈ [0, 1]: Harmonic mean of Precision and Recall of active user trip slots grounded in the reply.",
                "Slides 29, 30\nRQ3 Co-Primary DVs\n(Table 15, Figs 7B & 7C)",
                "Tests whether symbolic guardrails eliminate few-shot contamination while grounding all user constraints.",
                "Rules Active eliminates Cell 2's .359 leakage (55.6% incidence) down to .000 (Interaction F = 34.82, p < .001) and lifts Slot F1 from .208/.485 to .977/.952 (F = 489.52, p < .001).",
            ],
            [
                "Turns to Goal (TGC),\nRedundant Elicitation\n(RER) & Pareto Optimal",
                "• TGC: Total messages (user + bot) until [ACCEPT_BOOKING] (protocol floor = 5.00 turns: U1→A1→U2→A2→U3).\n• RER ∈ [0, 1]: Share of bot turns that re-ask an already stated slot.\n• Pareto Optimal: Best on ALL metrics simultaneously without trade-off loss.",
                "Slides 30–33\nRQ3 Cell 4 & RQ4\n(Table 16, Figure 8)",
                "Measures end-to-end multi-turn conversation efficiency and memory failures.",
                "RQ4 cuts turns by −29.5% (Explorer), −34.2% (Decisive, 5.00t floor), and −42.7% (Rigid, 8.73 → 5.00t floor) and drives RER from .109 to .000 (F = 63.02, p < .001).",
            ],
        ],
        col_widths=[1.85, 3.85, 1.55, 2.55, 3.09],
        font_size=7.0,
    )
    add_bottom_banner(
        s15,
        "How Slide 15 Unlocks Defense Slides 26–33: Every custom metric in RQ2–RQ4 is deterministic and directly interpretable: SBERT Style Cosine (.597), Pacing Error (3.87w), Violation Sensitivity (5.6% → 98.6%), Entity Leakage (35.9% → 0.0%), Slot F1 (.952), Turn Compression (−29.5% to −42.7%), and Redundant Questions (.109 → .000).",
    )

    # =========================================================================
    # SLIDE 16: DEFENSE SLIDE-BY-SLIDE DECODER CHEAT-SHEET (SLIDES 14–19 & 22–33)
    # =========================================================================
    s16 = prs.slides.add_slide(blank)
    add_header(
        s16,
        "DEFENSE DECODER MAP (SLIDE 16 OF 16)",
        "Slide-by-Slide Quick Reference Decoder for Defense Slides 14–19 & Slides 22–33",
        "Your 1-Page Defense Cheat-Sheet: What Each Slide Really Means, Which Terms Appear on It, and Your 10-Second Committee Answer",
    )
    add_glossary_table(
        s16, 0.22, 0.90, 12.89, 5.58,
        headers=[
            "Defense PPT Slide #",
            "Plain-English Core Message of That Slide (In 1 Simple Sentence)",
            "Terminology Appearing on That Slide (See Glossary Slides 8–15)",
            "Your 10-Second Knockout Answer If Committee Asks About This Slide",
        ],
        rows=[
            [
                "Slide 14:\nWhy Each Statistical\nTest Was Chosen",
                "Each RQ has a different experimental layout (3 independent groups, 3 repeated prompts, 2×2 grid, 2×3 grid), so each uses the exact matching ANOVA.",
                "One-Way ANOVA, RM-ANOVA (GG ε), 2×2 & 2×3 Factorial ANOVA, Type I Error Inflation (1 − 0.95³ = 14.3%), Within-Subject ρ = .50, ln(Turns).",
                "'Running multiple t-tests inflates false positives to 14.3%. Each RQ's structure is matched to its exact omnibus ANOVA while keeping familywise α = .05.'",
            ],
            [
                "Slide 15:\nMechanics of F, η²,\nInteractions & GG ε",
                "F measures Signal ÷ Noise, ηp² measures % of variance explained, non-parallel lines show Interactions (A×B), and GG ε fixes unequal pair variances.",
                "F = MS_between / MS_within, Eta-Squared (η²), Partial ηp² (.01 / .06 / .14), Main Effect vs. Interaction (A×B), Sphericity, Greenhouse–Geisser ε.",
                "'Across the experiments, F ranges from 9.79 to 664.43 (signal is 10× to 664× larger than noise) and every primary effect size is Large (ηp² = .182 to .793).'",
            ],
            [
                "Slide 16:\nBulletproof 3-Tier\nInference Triangulation",
                "To guarantee no reviewer can question normality, [0,1] bounds, or 0.0% floor variance, every RQ runs Parametric + Robust + Rank tests together.",
                "Heteroscedasticity, Welch's ANOVA, MacKinnon–White HC3 Sandwich SE, Kruskal–Wallis H, Friedman χ², Mann–Whitney U, Aligned Rank Transform (ART).",
                "'Even when zero leakage creates SD = .000 in Cell 4, HC3 sandwich variance (F = 33.85) and rank-based ART ANOVA (F = 2148.81) confirm p < .001.'",
            ],
            [
                "Slides 17 & 18:\nSample Size Power\n(α, 1−β, f, λ) & Flaws",
                "Sample sizes (159, 33, 144, 180) were derived mathematically from noncentral F (λ = f²·N) to guarantee >80% power to catch medium effects (f = .25).",
                "α = .05 (Type I), β = .20 (Type II), Power 1−β ≥ .80, Cohen's f = .25, Noncentrality λ = f²·N (8.00–10.50), F_crit, Within-Subject ρ = .50.",
                "'Solving λ = f²·N = 0.0625·N ≈ 8.0 to 9.88 gives exact minimum sizes of 128 and 158 (plus a 10% buffer). Smaller N would miss real effects 69% of the time.'",
            ],
            [
                "Slide 19:\nDomain Parameters\nλ_d = 0.15 & M = 9",
                "Recent turns are weighted with decay λ_d = 0.15 so greetings don't drown out negotiation, and prefixes are truncated at M = 9 user messages to stop outcome leakage.",
                "Exponential Turn Decay λ_d = 0.15 (Eq. 2), Prefix Truncation Horizon M ∈ {3,5,7,9}, Bootstrap ARI (.89), Outcome Cramér's V (.29 → .20), Routing κ.",
                "'Clustering whole chats leaks how the call ended (V = .29). Truncating to M = 9 user messages isolates how the customer shops with ARI = .89 stability.'",
            ],
            [
                "Slides 22 & 23:\nRQ1 Benchmark (159\nRuns) & Whole-Chat Audit",
                "K-Means (k=3) beats Ward and avoids HDBSCAN's 39% noise loss, while the diagnostic audit proved whole-chat clusters suffered from wizard confounding (V = .45).",
                "K-Means, Ward, HDBSCAN (39.1% noise), Cosine Silhouette (.147 vs −.013 null), Davies–Bouldin (DBI), Permutation Baseline, UMAP, Cramér's V = .45.",
                "'HDBSCAN drops 39% of customers as noise. K-Means (k=3) gives 100% live routing coverage, and restricting to user turns eliminates wizard confounding.'",
            ],
            [
                "Slides 24 & 25:\nRQ1 46-d Blocks, 16-Field\nCodebook & 3 Personas",
                "Combining PCA-20 Gemini prefix embeddings with 26 LLM behavioral columns at M=9 yields 3 stable personas and lifts prefix routing to 70.1%–97.3%.",
                "46-d Blocks (PCA-20 + 26 cols), 16-Field UserBehaviour Schema (Fields 14–16 held out), Quadratic Weighted κ_w (.87–.96), Spearman ρ (.64), LogReg Router κ.",
                "'Embeddings alone get ARI = .39; fusing PCA-20 with the validated behavioral schema (κ_w = .91) lifts stability to ARI = .89 and M=5 routing to 70.1% (κ = .535).'",
            ],
            [
                "Slides 26 & 27:\nRQ2 Primary (p=.211) vs.\nRefined (p<.001) & Holm",
                "Coarse routing failed in RQ2 (p = .211), but accurate Blocks routing (κ = .535) made Cluster-Adaptive prompting boost style (+31.8%) and cut pacing error to 3.87w.",
                "De-lexicalized SBERT Style Cosine (F = 9.79), Gemini Cosine & BERTScore F1 (topical controls), Pacing Error (3.87w, F = 7.10), Holm Paired t, Cohen's d_z = 0.74.",
                "'Contrasting Primary (p = .211) vs. Refined (p < .001) proves a causal mechanism: adaptive prompting works if and only if upstream persona routing is coherent.'",
            ],
            [
                "Slides 28, 29 & 30:\nRQ3 2×2 Guardrails,\nDual-Judge & Leakage",
                "Prompting alone fails safety (5.6% violation catch & 35.9% exemplar leakage), whereas Rules Active × Cluster-Adaptive achieves 98.6% enforcement & 0.0% leakage.",
                "5 YAML Rules, RAR (Violation Sens. 98.6%, Comp. Spec. 88.9%), Exemplar Leakage ELR (.359 → .000, Interaction F = 34.82), Slot F1 (.952), Dual-Judge κ = .917 / PABAK.",
                "'Figure 7B shows a classic protective interaction (F = 34.82): unguarded few-shot leaks foreign entities in 55.6% of calls, and the symbolic sanitizer reduces that to 0.0%.'",
            ],
            [
                "Slides 31, 32 & 33:\nRQ4 2×3 Simulation,\n5.00-Turn Floor & RER",
                "Combining the Verified Slot Ledger with persona-tailored package framing cuts turns to booking by 29.5%–42.7% and eliminates redundant questions (.109 → .000).",
                "4-Option Inventory (A/B/C/D), Blind Persona Audit (95.6%, κ = .933, Binomial p = 1.37e-18), ln(TGC) (F = 664.43), Interaction (F = 10.89), 5.00-Turn Floor, RER (.000).",
                "'Rigid Seekers gain the most (−42.7% turns, d = −3.40) because proactive Option A vs. D trade-off framing resolves the 5-star budget deadlock in a single turn.'",
            ],
        ],
        col_widths=[1.75, 3.35, 3.65, 4.14],
        font_size=6.9,
    )
    add_bottom_banner(
        s16,
        "How to Use Slides 8–16 During Your Defense: Keep this deck open beside your main presentation. If a committee member asks about ANY statistical test, symbol (α, β, λ, λ_d, ε, ηp², d, d_z, V, κ, κ_w, ρ), or metric on Defense Slides 14–19 or 22–33, jump directly to the matching Glossary Slide (8–15) or read the 10-second answer from Slide 16!",
    )

    # =========================================================================
    # SLIDE 17: CHESS-STYLE TURN INTELLIGENCE & NEXT-BEST-MOVE TABLEBASE (DTQ)
    # =========================================================================
    s17 = prs.slides.add_slide(blank)
    add_header(
        s17,
        "TURN INTELLIGENCE (SLIDE 17 OF 17)",
        "Chess-Style Turn Intelligence: From Cosine Top-3 (RQ2) to a 'Distance-to-Quotation' (DTQ) Tablebase",
        "How Consultative Travel Dialogue Maps to a Cooperative Hidden-Info Chess Game (POMDP) & Predicts the Optimal Next Agent Move Inside Each Cluster",
    )

    # Col 1: Chess vs Travel Chatbot (POMDP) Mapping
    add_stage_banner(s17, xs[0], y_top, col_w, col_h, "PART 1", "Chess vs. Travel Chatbot (POMDP)", "#F0F4F8", "#1B365D")
    add_card(
        s17, xs[0] + 0.10, y_top + 0.42, col_w - 0.20, 2.50,
        "1A. Exact Game-Theoretic Analogy",
        [
            ("• Checkmate (Terminal Goal S_goal): ", "Customer agrees all constraints are met & requests formal quotation (1–3 shortlisted packages) with Hot/Warm/Cold lead propensity.", "#1B5E20"),
            ("• Board State at Turn t (S_t): ", "Symbolic tuple: (C×K Cluster, Stage a–f, 9-Slot Bitmask, |P_t| Packages Left, Active Rule/Budget Conflict).", "#1B365D"),
            ("• Opponent A (Customer) & B (Agent): ", "Customer plays from persona (C×K); Agent plays move A_t (Questions + USP Pitch + Trade-Off).", "#1565C0"),
            ("• Referee (Illegal Move Filter): ", "RQ3 YAML Rule Engine + RQ4 Verified Slot Ledger.", "#C62828"),
        ],
        bg_hex="#FFFFFF", border_hex="#1B365D", font_size=7.2,
    )
    add_flow_arrow(s17, xs[0] + 1.35, y_top + 2.96, width=0.28, height=0.20, color_hex="#1B365D", direction="down")
    add_card(
        s17, xs[0] + 0.10, y_top + 3.20, col_w - 0.20, 2.12,
        "1B. Crucial Difference: Hidden-Info POMDP",
        [
            ("• Chess Is Complete Information: ", "All 64 squares & pieces are visible on Turn 1.", "#455A64"),
            ("• Travel Is a Cooperative POMDP: ", "Customer's true budget elasticity, senior/child needs & honeymoon occasion start HIDDEN! Every agent move must jointly maximize Information Gain (revealing hidden state) + Positional Narrowing (200 → 1–3 packages).", "#E65100"),
        ],
        bg_hex="#E3F2FD", border_hex="#1565C0", font_size=7.2,
    )

    add_flow_arrow(s17, 3.23, 3.45, width=0.25, height=0.38, color_hex="#1B365D", direction="right")

    # Col 2: Gaps in Cosine Top-3 (RQ2) vs. Turn-Economy Tablebase
    add_stage_banner(s17, xs[1], y_top, col_w, col_h, "PART 2", "Gap: Cosine Top-3 vs. Turn Tablebase", "#E0F2F1", "#00695C")
    add_card(
        s17, xs[1] + 0.10, y_top + 0.42, col_w - 0.20, 2.38,
        "2A. Why Cosine Top-3 (RQ2) Is Not a Move Predictor",
        [
            ("• Backward-Looking Surface Match: ", "In RQ2, FAISS retrieves top k=3 wizard turns via cos(q_t, e_j)—asking 'What did a human say in a similar context?'", "#C62828"),
            ("• Blind to Remaining Turns-to-Quote: ", "Two past wizard replies in identical state S_t get equal cosine scores even if Reply 1 closed in 1 turn while Reply 2 caused a 9-turn argument!", "#C62828"),
        ],
        bg_hex="#FFEBEE", border_hex="#C62828", font_size=7.3,
    )
    add_flow_arrow(s17, xs[1] + 1.35, y_top + 2.84, width=0.28, height=0.20, color_hex="#00695C", direction="down")
    add_card(
        s17, xs[1] + 0.10, y_top + 3.08, col_w - 0.20, 2.24,
        "2B. Exhaustive Symbolic Turn Tablebase (Turn-Q DB)",
        [
            ("• Finite Symbolic Hash (Like Chess Zobrist Keys): ", "While raw text is infinite, canonical state S_t × discrete agent move A_t is finite and indexable!", "#00695C"),
            ("• 3 Metrics Stored per (S_t, A_t) Entry: ", "\n  1. DTQ = E[T_quote − t | S_t, A_t] (Distance-to-Quotation)\n  2. Δ|P_t| = E[|P_t| − |P_{t+1}|] (Package Narrowing)\n  3. Q*(S_t, A_t) = P(Quotation Win | S_t, A_t)", "#1B5E20"),
        ],
        bg_hex="#E0F2F1", border_hex="#00695C", font_size=7.2,
    )

    add_flow_arrow(s17, 6.53, 3.45, width=0.25, height=0.38, color_hex="#00695C", direction="right")

    # Col 3: Dedicated Turn Intelligence Module Inside Hierarchical Clusters
    add_stage_banner(s17, xs[2], y_top, col_w, col_h, "PART 3", "Turn Intelligence Inside C × K Clusters", "#F3E5F5", "#6A1B9A")
    add_card(
        s17, xs[2] + 0.10, y_top + 0.42, col_w - 0.20, 2.38,
        "3A. Why Move Prediction Lives Inside C × K",
        [
            ("• Optimal Move Depends on Opponent Persona: ", "In chess and sales, the best move depends on who sits across the board!", "#6A1B9A"),
            ("• Concrete Example at Stage d (38 Packages Left): ", "\n  • For (Family, Economy, Rigid Seeker): [Bundle Senior+Breakfast + Pitch 4★ Exact vs 5★ +3d Shift] → DTQ = 1.0 turn.\n  • For (Couple, Honeymoon, Explorer): [Compare 2 Romantic USP Packages + Ask Tempo] → DTQ = 1.5 turns.", "#1B365D"),
        ],
        bg_hex="#FFFFFF", border_hex="#6A1B9A", font_size=7.2,
    )
    add_flow_arrow(s17, xs[2] + 1.35, y_top + 2.84, width=0.28, height=0.20, color_hex="#6A1B9A", direction="down")
    add_card(
        s17, xs[2] + 0.10, y_top + 3.08, col_w - 0.20, 2.24,
        "3B. Advantage-Weighted Retrieval Formula",
        [
            ("• Upgrading FAISS from Cosine to Value-Ranked: ", "Score(e_j | S_t, q_t) = α·cos(q_t, e_j) + β·Q*(S_t, A_j) − γ·DTQ(S_t, A_j).", "#6A1B9A"),
            ("• 2-Ply Customer Simulator Lookahead: ", "Simulates how Persona k will reply to candidate moves A_1, A_2, A_3 and picks A_t* with lowest remaining DTQ!", "#1B5E20"),
        ],
        bg_hex="#EDE7F6", border_hex="#5E35B1", font_size=7.3,
    )

    add_flow_arrow(s17, 9.83, 3.45, width=0.25, height=0.38, color_hex="#6A1B9A", direction="right")

    # Col 4: Decoupled Runtime Execution -> Quotation Checkmate
    add_stage_banner(s17, xs[3], y_top, col_w, col_h, "PART 4", "Decoupled Move + Style → Checkmate", "#E8F5E9", "#2E7D32")
    add_card(
        s17, xs[3] + 0.10, y_top + 0.42, col_w - 0.20, 2.65,
        "4A. Three-Way Division of Labor at Every Turn",
        [
            ("1. WHAT Move to Play (Turn Intelligence Engine): ", "Selects optimal discrete action A_t* from Cluster (C×K) Turn-Q DB to cut 200 → 1–3 packages in minimum DTQ turns.", "#E65100"),
            ("2. HOW to Phrase It (RQ2 Partitioned FAISS): ", "Retrieves top-3 [SLOT]-masked winning exemplars matching Cluster (C×K) and Move A_t* with target word pacing.", "#1565C0"),
            ("3. WHETHER Move Is Legal (RQ3 Rules + RQ4 Ledger): ", "Referee blocks rule violations (98.6% guard, 0.0% leakage) & forbids re-asking known slots (.000 RER).", "#1B5E20"),
        ],
        bg_hex="#FFFFFF", border_hex="#2E7D32", font_size=7.2,
    )
    add_flow_arrow(s17, xs[3] + 1.35, y_top + 3.11, width=0.28, height=0.20, color_hex="#2E7D32", direction="down")
    add_card(
        s17, xs[3] + 0.10, y_top + 3.35, col_w - 0.20, 1.97,
        "4B. Terminal 'Quotation Checkmate' Achieved",
        [
            ("• Minimum Turns to Agreed Quotation: ", "Customer confirms direct or negotiated constraints and requests 1–3 package quotations in minimum turns.", "#1B5E20"),
            ("• Calibrated Lead Handoff (Stage f): ", "Outputs Hot / Warm / Cold lead propensity based on final DTQ trajectory & urgency signals.", "#1B365D"),
        ],
        bg_hex="#C8E6C9", border_hex="#1B5E20", font_size=7.3,
    )

    add_bottom_banner(
        s17,
        "Chess Turn-Intelligence Summary: By compressing infinite text into canonical symbolic states S_t inside each Hierarchical Cluster (C×K), a 'Distance-to-Quotation' (DTQ) Turn Tablebase predicts the exact Next Best Agent Move A_t* (WHAT to play), while FAISS supplies persona phrasing (HOW to say it) and Symbolic Rules act as the Referee.",
    )

    # =========================================================================
    # SLIDE 18: PICTORIAL VISUALIZATION OF CENTRAL F (λ=0) vs. NONCENTRAL F (λ=f²·N)
    # =========================================================================
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.stats import f as f_dist
    from scipy.stats import ncf as ncf_dist

    fig_path = os.path.join(ROOT, "figures", "final", "fig_central_vs_noncentral_f.png")
    os.makedirs(os.path.dirname(fig_path), exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(13.2, 3.65), dpi=220, sharey=True)
    x = np.linspace(0.02, 13.5, 600)
    df1 = 2

    panels = [
        (
            "Panel A: When H₀ Is True (No Real Effect)\nCentral F (f = 0, λ = 0, df = 2, 156)",
            159, 0.0,
            "95% of runs stay left of F_crit = 3.05.\nOnly 5% (red tail = α = .05) cross F_crit by pure luck.",
        ),
        (
            "Panel B: Underpowered Small Sample (N = 36)\nNoncentral F (f = .25, λ = f²·N = 2.25)",
            36, 0.25 * 0.25 * 36,
            "Curve shifts right slightly (λ = 2.25), but 69.2% (β)\nstill falls LEFT of F_crit → Only 30.8% Power (Fails!)",
        ),
        (
            "Panel C: Powered Sample (N = 159)\nNoncentral F (f = .25, λ = f²·N = 9.94)",
            159, 0.25 * 0.25 * 159,
            "Adding N pushes curve right by λ = 9.94!\nNow 80.4% (Green = Power 1−β) crosses F_crit = 3.05!",
        ),
    ]

    for ax, (p_title, N_val, lam, note_txt) in zip(axes, panels):
        df2 = N_val - 3
        f_crit = f_dist.ppf(0.95, df1, df2)
        y_null = f_dist.pdf(x, df1, df2)
        ax.plot(x, y_null, color="#1565C0", lw=2.2, label="Central F (H₀: λ = 0)")
        ax.fill_between(
            x, 0, y_null, where=(x >= f_crit),
            color="#EF5350", alpha=0.45, label=f"Type I Error α = 5% (x ≥ {f_crit:.2f})",
        )
        if lam > 0:
            y_alt = ncf_dist.pdf(x, df1, df2, lam)
            pwr = 1.0 - ncf_dist.cdf(f_crit, df1, df2, lam)
            beta = 1.0 - pwr
            ax.plot(x, y_alt, color="#1B5E20", lw=2.5, label=f"Noncentral F (Hₐ: λ = {lam:.2f})")
            ax.fill_between(
                x, 0, y_alt, where=(x >= f_crit),
                color="#4CAF50", alpha=0.38, label=f"Power (1−β) = {pwr*100:.1f}% (Crosses F_crit)",
            )
            ax.fill_between(
                x, 0, y_alt, where=(x < f_crit),
                color="#FFB300", alpha=0.28, label=f"Missed Effect β = {beta*100:.1f}% (Left of F_crit)",
            )
            ax.annotate(
                f"Shift λ = {lam:.2f} →",
                xy=(min(9.5, 1.0 + lam / 2.0), 0.36),
                xytext=(0.8, 0.36),
                arrowprops=dict(arrowstyle="->", color="#00695C", lw=2.0),
                fontsize=8.5, fontweight="bold", color="#00695C",
            )
        ax.axvline(f_crit, color="#C62828", ls="--", lw=2.0, label=f"Red Cutoff F_crit = {f_crit:.2f}")
        ax.set_title(p_title, fontsize=9.5, fontweight="bold", color="#1B365D", pad=6)
        ax.set_xlabel("F-Statistic Value (Signal ÷ Noise)", fontsize=8.5, fontweight="bold")
        ax.set_xlim(0, 13.0)
        ax.set_ylim(0, 0.88)
        ax.grid(True, linestyle=":", alpha=0.4)
        ax.legend(loc="upper right", fontsize=7.2, frameon=True)
        ax.text(
            0.50, 0.48, note_txt,
            transform=ax.transAxes, fontsize=7.6, fontweight="bold",
            color="#1B365D", bbox=dict(boxstyle="round,pad=0.3", fc="#FFF8E1", ec="#F57F17", lw=1.0),
        )
    axes[0].set_ylabel("Probability Density", fontsize=9.0, fontweight="bold")
    plt.tight_layout()
    plt.savefig(fig_path, dpi=220)
    plt.close(fig)

    s18 = prs.slides.add_slide(blank)
    add_header(
        s18,
        "PICTORIAL POWER GUIDE (SLIDE 18 OF 18)",
        "Pictorial Explanation: Central F (λ = 0) vs. Noncentral F (λ = f²·N), F_crit & 80% Power",
        "Visualizing How Increasing Sample Size N Pushes the Green Noncentral-F Bell Curve Right Across the Red F_crit Line",
    )
    s18.shapes.add_picture(fig_path, Inches(0.22), Inches(0.88), width=Inches(12.89), height=Inches(3.60))

    add_card(
        s18, 0.22, 4.55, 4.18, 1.92,
        "1. Panel A — Central F (When H₀ Is True, λ = 0)",
        [
            ("• Blue Curve Sits Near F ≈ 1.0: ", "When there is NO real difference between prompts/algorithms, Signal ≈ Noise, so F hovers around 1.0.", "#1565C0"),
            ("• The Red Cutoff Line (F_crit = 3.05): ", "A vertical red line is drawn so only the top 5% tail (red shaded area = α = .05) sits to the right. Any F > 3.05 rejects H₀.", "#C62828"),
        ],
        bg_hex="#E3F2FD", border_hex="#1565C0", font_size=7.4,
    )
    add_card(
        s18, 4.57, 4.55, 4.18, 1.92,
        "2. Panel B — Too Small Sample N = 36 (λ = 2.25)",
        [
            ("• Why Small N Fails Even When Ha Is True: ", "A real medium effect (f = .25 → f² = 0.0625) exists, but with only N = 36, the shift is tiny: λ = 0.0625 × 36 = 2.25.", "#E65100"),
            ("• 69.2% False Negative Risk (β): ", "Most of the green curve (69.2%, yellow area) is still trapped to the LEFT of the red F_crit line! Only 30.8% crosses F_crit.", "#C62828"),
        ],
        bg_hex="#FFF8E1", border_hex="#F57F17", font_size=7.4,
    )
    add_card(
        s18, 8.93, 4.55, 4.18, 1.92,
        "3. Panel C — Powered Sample N = 159 (λ = 9.94 → 80.4% Power)",
        [
            ("• How Increasing N Pushes the Curve Right: ", "Because λ = f²·N = 0.0625 × 159 = 9.94, larger N physically shoves the entire green curve to the right!", "#1B5E20"),
            ("• ≥80% Now Crosses F_crit (Green Area): ", "Once λ reaches ~8.0 (df₁=1) to ~9.88 (df₁=2), over 80% of the green curve sits to the RIGHT of F_crit → 80.4% Power!", "#1B5E20"),
        ],
        bg_hex="#E8F5E9", border_hex="#2E7D32", font_size=7.4,
    )

    add_bottom_banner(
        s18,
        "One-Sentence Visual Takeaway: The red line (F_crit ≈ 3.05) is fixed by α = 5% on the Blue curve (λ = 0). Multiplying sample size N in λ = f²·N acts like a bulldozer that pushes the Green curve to the right until ≥80% of its area crosses that red F_crit finish line!",
    )

    # =========================================================================
    # SLIDE 19: PICTORIAL GUIDE TO ETA-SQUARED (η² / ηp²) AS SIMPLE PIE SLICES
    # =========================================================================
    fig_eta_path = os.path.join(ROOT, "figures", "final", "fig_eta_squared_explained.png")
    fig, axes = plt.subplots(1, 5, figsize=(13.2, 3.25), dpi=220)
    pie_specs = [
        ("Planned Target\n(f = .25 → η² = .059)", 5.9, "#F57F17"),
        ("RQ1 Clustering\n(η² = .539 → 53.9%)", 53.9, "#1565C0"),
        ("RQ2 Style Cosine\n(ηp² = .234 → 23.4%)", 23.4, "#00897B"),
        ("RQ3 Slot F1\n(ηp² = .778 → 77.8%)", 77.8, "#6A1B9A"),
        ("RQ4 Log Turns\n(ηp² = .793 → 79.3%)", 79.3, "#2E7D32"),
    ]
    for ax, (title_p, sig_p, col_p) in zip(axes, pie_specs):
        noise_p = 100.0 - sig_p
        wedges, _ = ax.pie(
            [sig_p, noise_p],
            colors=[col_p, "#E0E6ED"],
            startangle=90,
            counterclock=False,
            wedgeprops=dict(width=0.48, edgecolor="white", linewidth=2),
        )
        ax.text(0, 0.06, f"{sig_p:.1f}%", ha="center", va="center", fontsize=13, fontweight="bold", color=col_p)
        ax.text(0, -0.18, "Signal", ha="center", va="center", fontsize=8.5, fontweight="bold", color="#37474F")
        ax.set_title(title_p, fontsize=9.2, fontweight="bold", color="#1B365D", pad=4)
        ax.text(
            0, -1.25,
            f"Noise = {noise_p:.1f}%",
            ha="center", va="center", fontsize=8.0, color="#546E7A", fontweight="bold",
        )
    plt.tight_layout()
    plt.savefig(fig_eta_path, dpi=220)
    plt.close(fig)

    s19 = prs.slides.add_slide(blank)
    add_header(
        s19,
        "ETA-SQUARED MADE EASY (SLIDE 19 OF 19)",
        "Pictorial Guide to Eta-Squared (η² / ηp²): Just Move the Decimal 2 Places to Get '% of the Pie'!",
        "Zero Scary Math Required: How to Explain η², ηp², and Why f = .25 Equals ~6% Using a 17-Slice Pizza",
    )
    s19.shapes.add_picture(fig_eta_path, Inches(0.22), Inches(0.88), width=Inches(12.89), height=Inches(3.18))

    add_card(
        s19, 0.22, 4.14, 4.18, 2.32,
        "1. What Eta-Squared (η² / ηp²) Means in 5 Seconds",
        [
            ("• Rule #1 — Move the Decimal 2 Places: ", "Whenever you see η² = .539 or ηp² = .793, just multiply by 100: it literally means 53.9% or 79.3% of the Pie!", "#1B5E20"),
            ("• What the Pie Represents: ", "Every outcome has two parts: [Method Signal] + [Random Noise] = 100%. Eta-Squared is simply the % slice explained by the experimental factor!", "#1B365D"),
            ("• Cohen's 3 Benchmarks: ", "1% (.01) = Small | 6% (.06) = Medium | ≥14% (.14) = Large. All four RQs (23.4% to 79.3%) are Large!", "#1565C0"),
        ],
        bg_hex="#E3F2FD", border_hex="#1565C0", font_size=7.4,
    )
    add_card(
        s19, 4.57, 4.14, 4.18, 2.32,
        "2. The '17-Slice Pizza Trick' for f = .25 → η² = 5.9%",
        [
            ("• Step 1 (f = .25 is 1/4): ", "Saying f = 0.25 just means Signal spread is 1 and Noise spread is 4 (a 1-to-4 ratio).", "#E65100"),
            ("• Step 2 (Square Both to Get Pizza Slices): ", "Signal slices = 1² = 1 slice. Noise slices = 4² = 16 slices.", "#E65100"),
            ("• Step 3 (Count the Whole Pizza): ", "1 slice of Signal + 16 slices of Noise = 17 total slices! And 1 out of 17 (1 ÷ 17) = 5.88% (≈ 6%, or η² = .059)!", "#1B5E20"),
        ],
        bg_hex="#FFF8E1", border_hex="#F57F17", font_size=7.4,
    )
    add_card(
        s19, 8.93, 4.14, 4.18, 2.32,
        "3. Exact Sentences to Say to the Defense Committee",
        [
            ("• For RQ1 (η² = .539): ", "'53.9% of the difference in cluster quality comes from which algorithm was selected!'", "#1565C0"),
            ("• For RQ2 (ηp² = .234): ", "'23.4% of style convergence comes from Cluster-Adaptive prompting!'", "#00695C"),
            ("• For RQ3 (ηp² = .778) & RQ4 (ηp² = .793): ", "'Nearly 80% (77.8% and 79.3%) of the improvement in slot grounding and turn speed comes directly from the neuro-symbolic architecture, and only ~20% is random noise!'", "#1B5E20"),
        ],
        bg_hex="#E8F5E9", border_hex="#2E7D32", font_size=7.4,
    )

    add_bottom_banner(
        s19,
        "Never Worry About the Eta-Squared Formula Again: If a professor asks 'What does ηp² = .793 mean?', just smile and say: 'Move the decimal two places—it means 79.3% of the variance pie is explained by the prompting policy, and only 20.7% is random noise (more than 5× Cohen's 14% Large threshold)!'",
    )

    os.makedirs(os.path.dirname(OUT_PPTX), exist_ok=True)
    prs.save(OUT_PPTX)
    print(f"Saved standalone 19-slide RQ Text-to-ANOVA Methodology & Glossary PPTX: {OUT_PPTX} (Total slides: {len(prs.slides)})")


if __name__ == "__main__":
    build_deck()

