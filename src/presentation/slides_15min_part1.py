"""
Part 1 of the 15-Minute Executive & Defense Presentation (Slides 1–15):
  - Slide 1: Title Slide (Identify -> Personalize -> Govern -> Optimize)
  - Slides 2–3: Problem Statement & Technical Paradox with Concrete Examples (from Slides 3 & 4)
  - Slides 4–6: Literature Synthesis & Empirical Proof Matrix (from Slides 6, 7 & 8)
  - Slide 7: Research Questions & Integrated Storyline: Identify (RQ1) -> Personalize (RQ2) -> Govern (RQ3) -> Optimize (RQ4) (Enhanced Slide 9)
  - Slide 8: Dataset Provenance, Two-Tier Schema, Cleaning Audit & Zero-Leakage 70/30 Split (Condensed Slides 10 & 11)
  - Slides 9–10: Univariate, Bivariate & Multivariate Exploratory Data Analysis (Slides 12 & 13)
  - Slide 11: Sample-Size Derivation (alpha, beta, f, lambda, F_crit, N, n) & Operational Execution in RQ1 (Enhanced Slide 17)
  - Slides 12–15: Stage 1 — IDENTIFY (RQ1 Results, Parts 1–4; from Slides 22–25 with streamlined robustness notes)
"""

import os
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt
from presentation.ppt_styles import (
    BLUE,
    CALLOUT_BG,
    CARD_BG,
    CORAL,
    DARK,
    GOLD,
    GREEN,
    GREEN_BG,
    NAVY,
    RED_BG,
    TEAL,
    WHITE,
    _add_formatted_runs,
)
from report.final_context import FIG_FIN, FIG_INT, REPO, TITLE


def build_slides_15min_part1(D, ctx):
    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    D.add_title_slide(
        title=TITLE,
        subtitle=(
            "End-to-End Neuro-Symbolic Storyline: Identify (RQ1) → Personalize (RQ2) → Govern (RQ3) → Optimize (RQ4)"
        ),
        badge_text="QM640 CAPSTONE DEFENSE — 15-MINUTE PRESENTATION",
        author_lines=[
            "<b>Author:</b> Surnella Sandeep  |  <b>Course:</b> QM640: Data Analytics Capstone (Department of Data Analytics, Walsh College)",
            "<b>Instructor & Capstone Mentor:</b> Mr. Smitraj Raut  |  <b>Date:</b> 10th Nov 2026",
            f"<b>Reproducible Code & Data Repository:</b> {REPO}",
            "<b>Empirical Scope:</b> 2,833 Analytic Human Dialogues (Microsoft Frames N = 1,334; MultiWOZ 2.2 N = 1,499) + ~8,900 Gemini 2.5 Flash/Pro Evaluations",
        ],
        notes=(
            "Welcome to the 15-minute capstone defense presentation. "
            "This presentation follows a cohesive four-stage engineering and statistical storyline: "
            "Identify the traveler persona early (RQ1), Personalize response style and pacing (RQ2), "
            "Govern responses for zero entity leakage and policy compliance (RQ3), and Optimize multi-turn "
            "negotiation efficiency (RQ4)."
        ),
    )

    # =========================================================================
    # SLIDE 2 (FROM SLIDE 3): THE REAL-WORLD BUSINESS PROBLEM (CONCRETE EXAMPLES)
    # =========================================================================
    s = D.content_slide(
        "1. Problem Statement & Motivation",
        "The Real-World Business Problem: Why Static Travel Chatbots Fail",
        "Travelers do not all shop the same way—yet commercial chatbots force every customer through one static script",
        notes="Show how three distinct traveler personas enter an Online Travel Agency (OTA) portal and get frustrated by a one-size-fits-all script.",
    )
    D.add_card(
        s, 0.35, 1.50, 4.05, 4.45,
        title="Customer Type A: The Decisive Booker (45.0%)",
        header_bg=NAVY,
        bullets=[
            "<b>How they talk (Frames ID e2c09f7a):</b>",
            (1, "<i>'I need a 5-night package from Dallas to Cancun departing Aug 12 for 2 adults under $2,400.'</i>"),
            "<b>What they want:</b> Immediate confirmation of the best matching package and direct booking.",
            "<b>How a Static Chatbot fails them:</b>",
            (1, "Follows a slow 8-step intake script; re-asks slots already stated in Turn 1 (19.4% Redundant Elicitation Rate in the Zero-Shot baseline)."),
            (1, "Writes verbose 35-word paragraphs instead of a crisp 16-word confirmation."),
            "<b>Business Impact:</b> Impatient high-intent buyers abandon the cart before checkout.",
        ],
    )
    D.add_card(
        s, 4.60, 1.50, 4.10, 4.45,
        title="Customer Type B: The Open Explorer (25.5%)",
        header_bg=TEAL,
        bullets=[
            "<b>How they talk (Frames ID b84f11c2):</b>",
            (1, "<i>'Looking for a week off in September under a $3,000 budget—what beach or European cities can be compared?'</i>"),
            "<b>What they want:</b> Side-by-side comparison of 2–3 distinct options across price and hotel tiers.",
            "<b>How a Static Chatbot fails them:</b>",
            (1, "Presents only one option per turn, forcing the user to ask 'What about another city?' or 'What about 4-star vs 3-star?' across 18+ turns."),
            "<b>Business Impact:</b> Long, exhausting 18-turn sessions that drive up cloud LLM inference costs and user fatigue.",
        ],
    )
    D.add_card(
        s, 8.90, 1.50, 4.08, 4.45,
        title="Customer Type C: Rigid-Constraint Seeker (29.5%)",
        header_bg=CORAL,
        bullets=[
            "<b>How they talk (Frames ID 91a4d0e5):</b>",
            (1, "<i>'I only want a 5-star hotel in Tokyo on Oct 5 for 10 nights under $2,200—no other dates or stars.'</i>"),
            "<b>What they want:</b> If exact inventory is $2,596 (over budget), they need immediate, transparent trade-off options (4-star on Oct 5 vs. 5-star on Oct 12).",
            "<b>How a Static Chatbot fails them:</b>",
            (1, "Says 'No package found' or argues for 4 turns before revealing alternatives (68.0% end with no suitable option in human logs)."),
            "<b>Business Impact:</b> 8.73-turn deadlock loops and lost bookings.",
        ],
    )
    D.add_callout(
        s, 0.35, 6.08, 12.63, 1.02,
        "<b>Business Problem Statement (Buhalis & Sinarta, 2019; Ivanov & Webster, 2019; Melián-González et al., 2021):</b>\n"
        "Online travel agencies (OTAs) and hospitality contact centers suffer from low self-service conversion and high session abandonment because static LLM prompts fail to adapt information density, pacing, and trade-off framing to customer decision-making styles—while unverified generative responses create financial liability from policy violations.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=11.5,
    )

    # =========================================================================
    # SLIDE 3 (FROM SLIDE 4): THE TECHNICAL PARADOX — WHY NAIVE AI ADAPTATION FAILS
    # =========================================================================
    s = D.content_slide(
        "1. Problem Statement & Motivation",
        "The Technical Paradox: Why Naive Few-Shot AI Adaptation Fails",
        "Simply pasting retrieved past dialogues into an LLM prompt introduces two severe production hazards",
        notes="Explain why standard Retrieval-Augmented Generation (RAG) or naive KATE few-shot prompting fails without symbolic guardrails.",
    )
    D.add_card(
        s, 0.35, 1.50, 6.15, 3.80,
        title="Hazard 1: Exemplar Entity Leakage (Hallucinated Terms)",
        header_bg=CORAL,
        bg_color=RED_BG,
        bullets=[
            "<b>What happens in standard few-shot prompting (Liu et al., 2022):</b>",
            (1, "To teach the LLM how to talk to an <i>Open Explorer</i>, the system retrieves 3 similar past transcripts from the database and puts them in the prompt."),
            "<b>The Contamination Trap (Proven in the RQ3 Experiment):</b>",
            (1, "If those retrieved examples mention <b>'Sapphire Bay Resort'</b>, <b>'SkyBridge Airways'</b>, <b>'$1,149'</b>, or promo code <b>'VIP25'</b>, the LLM copies those stale entities into the current customer's reply!"),
            "<b>Empirical Proof (RQ3 Table 15):</b>",
            (1, "Unguarded Cluster-Adaptive Few-Shot leaked stale exemplar entities in <b>55.6% of all responses</b> (mean leakage rate = <b>0.359</b>, <i>p</i> < .001)."),
        ],
    )
    D.add_card(
        s, 6.80, 1.50, 6.18, 3.80,
        title="Hazard 2: Enterprise Policy Blindness (Rule Violations)",
        header_bg=CORAL,
        bg_color=RED_BG,
        bullets=[
            "<b>What happens when rules are only written in the system prompt:</b>",
            (1, "Travel bookings are governed by strict numeric constraints: e.g., international trips require ≥ 15 days visa lead time; passports need ≥ 6 months validity; FIT bookings allow ≤ 4 adults; promo discounts cap at 15%."),
            "<b>The Attention Competition Trap (Yao et al., 2024):</b>",
            (1, "When the LLM focuses on matching conversational style, it overlooks arithmetic thresholds buried in long text prompts."),
            "<b>Empirical Proof (RQ3 Table 15):</b>",
            (1, "Without an external symbolic rule engine (<i>Rules Off</i>), Gemini 2.5 Flash enforced violated booking rules in only <b>5.6% of violating sessions</b> (missing <b>94.4%</b> of violations!)."),
        ],
    )
    D.add_card(
        s, 0.35, 5.45, 12.63, 1.65,
        title="Solution: Four-Stage Neuro-Symbolic Architecture — Identify (RQ1) → Personalize (RQ2) → Govern (RQ3) → Optimize (RQ4)",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>1. IDENTIFY (RQ1 — Early-Turn Hybrid Routing):</b> Classify whether the traveler is a <i>Decisive Booker</i>, <i>Open Explorer</i>, or <i>Rigid-Constraint Seeker</i> from the first <i>M</i> = 9 user messages (`Blocks` router κ = .535 to .958) without leaking end-of-dialogue outcomes.",
            "<b>2. PERSONALIZE (RQ2 — Slot-Masked FAISS Retrieval):</b> Replace all entities in retrieved examples with `[SLOT]` placeholders (`[HOTEL_NAME]`, `[BUDGET_USD]`) so the LLM adapts <i>style and pacing</i> (+31.8% style cosine, 3.87w pacing error) without copying stale facts.",
            "<b>3. GOVERN (RQ3) & 4. OPTIMIZE (RQ4):</b> Enforce declarative YAML booking policies (<b>0.0% leakage, 98.6% violation enforcement</b>) and lock stated user constraints in a Verified Informed Slot Ledger (<b>−29.5% to −42.7% turns, 0.0% redundant questions</b>).",
        ],
        font_size=11.0,
    )

    # =========================================================================
    # SLIDE 4 (FROM SLIDE 6): LITERATURE STREAM 1 & 2
    # =========================================================================
    s = D.content_slide(
        "2. Literature Synthesis",
        "Literature Review (Part 1): Hospitality AI Value & Task-Oriented Corpora",
        "Prior business and corpus findings, methodological foundations, and novel empirical additions",
        notes="Synthesizes Streams 1 and 2 of the literature review across hospitality AI value and task-oriented dialogue corpora.",
    )
    D.add_card(
        s, 0.35, 1.50, 6.15, 5.45,
        title="Stream 1: Travel & Hospitality AI Business Value",
        header_bg=NAVY,
        bullets=[
            "<b>What Prior Papers Tried & Found:</b>",
            (1, "<b>Buhalis & Sinarta (2019)</b> introduced real-time 'nowness' co-creation in tourism: travelers expect instant, personalized itinerary synthesis."),
            (1, "<b>Ivanov & Webster (2019)</b> established the ROI framework for hospitality automation: chatbots create net economic value only when they resolve complex consultative queries without human escalation."),
            (1, "<b>Melián-González et al. (2021)</b> surveyed <i>N</i> = 1,476 consumers and proved that perceived interaction efficiency and task fit drive chatbot adoption."),
            (1, "<b>Jannach et al. (2021) & Inaba et al. (2022)</b> showed qualitatively that travelers exhibit heterogeneous initiative and constraint rigidity."),
            "<b>Application of Prior Foundations:</b>",
            (1, "Operationalizes qualitative constructs—<i>decisiveness, exploration breadth, constraint rigidity, and interaction effort</i>—into 16 quantitative behavioral variables and multi-turn turn-economy metrics."),
            "<b>Novel Contribution (With Empirical Proof):</b>",
            (1, "Prior tourism papers relied on <i>post-hoc user surveys</i>. This study instruments actual LLM turn economy, proving a <b>35.8% reduction in turns (7.93 → 5.09 turns, p < .001)</b> and <b>0.0% redundant questions</b>."),
        ],
        font_size=11,
    )
    D.add_card(
        s, 6.80, 1.50, 6.18, 5.45,
        title="Stream 2: Task-Oriented Dialogue Corpora (Frames & MultiWOZ)",
        header_bg=TEAL,
        bullets=[
            "<b>What Prior Papers Tried & Found:</b>",
            (1, "<b>El Asri et al. (2017) [Microsoft Frames]</b> collected 1,369 human–human Wizard-of-Oz vacation package negotiations to study non-linear <i>frame-switching</i> (comparing multiple flight+hotel packages under budget ceilings)."),
            (1, "<b>Budzianowski et al. (2018) & Zang et al. (2020) [MultiWOZ 2.2]</b> created a 10,438-dialogue benchmark for supervised slot-filling across city services (hotel, train, attraction, taxi, restaurant)."),
            "<b>Application of Prior Foundations:</b>",
            (1, "Uses Frames (<i>N</i> = 1,334 analytic) as the primary consultative travel testbed and MultiWOZ 2.2 (<i>N</i> = 1,499) as an external structural transfer benchmark."),
            "<b>Novel Contribution (With Empirical Proof):</b>",
            (1, "Both corpora were built for <i>supervised slot state tracking</i>, treating all users as uniform. Neither clustered user decision-making archetypes nor audited policy compliance."),
            (1, "Cross-corpus evaluation in RQ1 proves that Frames negotiation archetypes do not transfer trivially to simple MultiWOZ slot-filling (centroid cosine <b>.467 vs. .269, t = 28.08, p < .001</b>), demonstrating that consultative travel requires a dedicated archetype taxonomy."),
        ],
        font_size=11,
    )

    # =========================================================================
    # SLIDE 5 (FROM SLIDE 7): LITERATURE STREAM 3 & 4
    # =========================================================================
    s = D.content_slide(
        "2. Literature Synthesis",
        "Literature Review (Part 2): Representation Learning, FAISS ICL & Guardrails",
        "Integrating vector geometry, dynamic in-context learning, and programmable rails while overcoming baseline failure modes",
        notes="Synthesizes Streams 3 and 4 covering SBERT/Gemini embeddings, KATE k-NN prompting, and NeMo/Tau-bench guardrails.",
    )
    D.add_card(
        s, 0.35, 1.50, 6.15, 5.45,
        title="Stream 3: Embeddings & Unsupervised Clustering",
        header_bg=BLUE,
        bullets=[
            "<b>What Prior Papers Tried & Found:</b>",
            (1, "<b>Reimers & Gurevych (2019) [Sentence-BERT]</b> and <b>Lee et al. (2025) [Gemini Embeddings]</b> showed that bi-encoder transformers map text into cosine spaces suitable for clustering."),
            (1, "<b>McInnes et al. (2017, 2018) [HDBSCAN & UMAP]</b> and <b>Hennig (2007) [Bootstrap ARI]</b> established density clustering and resampling stability."),
            (1, "<b>Gilardi et al. (2023)</b> proved zero-temp LLMs achieve high annotation reliability."),
            "<b>What Failed When Applied Directly (Interim Diagnostic Finding):</b>",
            (1, "Clustering whole-dialogue embeddings directly (as in standard studies) captured <i>end-of-dialogue outcomes</i> and <i>wizard identity</i> (Cramér's <i>V</i> = .45) rather than user behavior, yielding poor early-turn routing (<b>κ = .24</b>) and a null RQ2 prompting result (<b>p = .211</b>)!"),
            "<b>Methodological Innovation (RQ1 Breakthrough):</b>",
            (1, "Combining <b>truncated opening user prefixes (first M = 9 user messages)</b> with a <b>16-field LLM behavioral profile (`Blocks`)</b> raised bootstrap stability to <b>ARI = .89 (.87 in ablation)</b> and out-of-sample prefix routing to <b>κ = .535 (m=5) and κ = .958 (m=9 boundary consistency)</b>."),
        ],
        font_size=11,
    )
    D.add_card(
        s, 6.80, 1.50, 6.18, 5.45,
        title="Stream 4: Dynamic Few-Shot Retrieval & Symbolic Guardrails",
        header_bg=GOLD,
        bullets=[
            "<b>What Prior Papers Tried & Found:</b>",
            (1, "<b>Brown et al. (2020)</b> & <b>Liu et al. (2022) [KATE]</b> showed that retrieving nearest-neighbor in-context examples via <b>FAISS (Johnson et al., 2021)</b> beats random static examples on single-turn NLP tasks."),
            (1, "<b>Rebedea et al. (2023) [NeMo Guardrails]</b> & <b>Yao et al. (2024) [τ-bench]</b> showed that prompt-only LLMs violate domain rules over 50% of the time."),
            "<b>Where Prior Papers Stopped:</b>",
            (1, "KATE retrieves from one <i>unpartitioned global pool</i> with raw unmasked entities. NeMo and τ-bench test safety rails in isolation without studying how rails interact with dynamic style prompting."),
            "<b>Methodological Innovation (RQ2 & RQ3 Breakthrough):</b>",
            (1, "Combining <b>archetype-partitioned FAISS sub-indices (`[SLOT]`-masked) + archetype pacing directives</b> boosts de-lexicalized SBERT style convergence over static few-shot by <b>+31.8% (.597 vs. .453, p < .001, d_z = 0.74)</b>."),
            (1, "In RQ3, a <b>significant 2 × 2 interaction (F = 34.82, p < .001)</b> demonstrates that the declarative governance layer eliminates the <b>35.9% entity leakage</b> of unguarded few-shot prompting down to <b>0.0% detected</b>."),
        ],
        font_size=11,
    )

    # =========================================================================
    # SLIDE 6 (FROM SLIDE 8): LITERATURE SYNTHESIS MATRIX WITH DATA EXAMPLES
    # =========================================================================
    s = D.content_slide(
        "2. Literature Synthesis",
        "Literature Synthesis Matrix: Prior Approaches vs. Empirical Findings",
        "Concrete examples from RQ1–RQ4 data illustrating what prior methods miss and what the proposed framework resolves",
        notes="Walk through this synthesis matrix to show how each limitation in prior work maps directly to an empirical proof in RQ1–RQ4.",
    )
    D.add_table(
        s, 0.35, 1.50, 12.63, 5.55,
        headers=["Prior Literature Benchmark", "What Prior Paper Did", "Limitation When Applied to Travel Dialogues", "Methodological Addition", "Concrete Empirical Proof (RQ1–RQ4)"],
        rows=[
            [
                "Whole-Text Embedding Clustering\n(Reimers & Gurevych, 2019;\nMcInnes et al., 2017)",
                "Clustered full documents using SBERT / HDBSCAN.",
                "HDBSCAN discards 39.1% (MiniLM) / 35.8% (Gemini) of dialogues as noise; full-dialogue vectors leak end-of-session outcomes.",
                "Prefix-truncated (M=9 user msgs) hybrid Blocks (PCA-20 Gemini + 16 LLM behavioral ratings) with K-Means (k=3, 100% coverage).",
                "RQ1 (Identify): HDBSCAN failed in 53/53 default runs. The M=9 Blocks router achieved ARI = .89 (.87 ablation) and raised held-out routing from κ = .24 (39.4%) to κ = .535 (70.1% at m=5) and κ = .958 (97.3% at m=9).",
            ],
            [
                "Global k-NN Few-Shot (KATE)\n(Liu et al., 2022;\nBrown et al., 2020)",
                "Retrieved k nearest examples from one global pool without persona routing.",
                "Static/unrouted examples mismatch user pacing; coarse routing (κ=.24) fails to improve style.",
                "Archetype-partitioned FAISS sub-indices + archetype pacing directives routed via Blocks.",
                "RQ2 (Personalize): Coarse Primary RQ2 failed (F = 1.61, p = .211). Refined RQ2 succeeded (F = 9.79, p < .001, ηp² = .234): style cosine rose from .453 (Static) to .597, and word pacing error fell from 10.12w to 3.87w.",
            ],
            [
                "Unmasked In-Context Examples\n(Standard RAG / Few-Shot)",
                "Inserted raw historical text examples directly into the LLM prompt.",
                "LLM copies stale hotel names, prices, and promo codes from examples into the active user session.",
                "Regex/Schema [SLOT] masking in FAISS exemplars + post-generation entity leakage sanitizer.",
                "RQ3 (Govern): Unguarded Cluster-Adaptive leaked stale entities ('Sapphire Bay Resort', '$1,149', 'VIP25') in 55.6% of cases (ELR = .359). Rules Active × Cluster-Adaptive reduced leakage to 0.0% (Interaction F = 34.82, p < .001).",
            ],
            [
                "Prompt-Only Policy Instructions\n(Yao et al., 2024 τ-bench;\nRebedea et al., 2023)",
                "Evaluated LLM adherence to domain rules stated only in natural language prompts.",
                "LLMs ignore numeric visa, passport, adult-cap, and discount thresholds when optimizing for conversational tone.",
                "Deterministic YAML RuleEngine (5 Tier-2 rules) executing pre-generation checks & post-generation verification.",
                "RQ3 (Govern): Under Rules Off, Gemini 2.5 Flash enforced policy violations in only 5.6% of violating sessions. Activating RuleEngine raised violation enforcement to 98.6% (F = 43.92, p < .001) and Slot F1 from .485 to .952.",
            ],
            [
                "Static Sequential Slot-Filling\n(Budzianowski et al., 2018;\nInaba et al., 2022)",
                "Used a single dialogue policy across all users without tracking informed slots.",
                "Re-asks already stated constraints and causes 8.7-turn deadlocks for Rigid-Constraint Seekers.",
                "Verified Informed Slot Ledger + Archetype-Specific Turn-Economy Policy (bundle vs. compare vs. proactive trade-off).",
                "RQ4 (Optimize): Cut turns to booking by −42.7% for Rigid-Constraint Seekers (8.73 → 5.00 turns, d = −3.40), −34.2% for Decisive Bookers (7.60 → 5.00), and −29.5% for Open Explorers (7.47 → 5.27), while cutting RER from .109 to .000.",
            ],
        ],
        col_widths=[1.8, 1.9, 2.3, 2.5, 4.1],
        font_size=9.8,
        align_left_cols=(0, 1, 2, 3, 4),
        highlight_rows=(0, 1, 2, 3, 4),
    )

    # =========================================================================
    # SLIDE 7 (ENHANCED SLIDE 9): RESEARCH QUESTIONS & STORYLINE ARCHITECTURE
    # =========================================================================
    s = D.content_slide(
        "3. Research Questions & Storyline",
        "Integrated Research Storyline: Identify (RQ1) → Personalize (RQ2) → Govern (RQ3) → Optimize (RQ4)",
        "Four sequential experimental stages where each validated output unlocks the next layer of conversational intelligence",
        notes=(
            "Emphasize the four-word narrative arc: Identify (RQ1) -> Personalize (RQ2) -> Govern (RQ3) -> Optimize (RQ4). "
            "Each RQ is an essential link in a single causal chain rather than an isolated experiment."
        ),
    )

    # Top Visual 4-Stage Storyline Banner (y = 1.45, h = 1.02)
    stages = [
        (
            "STAGE 1: IDENTIFY (RQ1)",
            "Discover 3 traveler archetypes & route from opening user prefix (M = 9 msgs, κ = .535–.958)",
            NAVY,
            RGBColor(232, 238, 248),
        ),
        (
            "STAGE 2: PERSONALIZE (RQ2)",
            "Retrieve k = 3 [SLOT]-masked FAISS exemplars + pacing directives to match persona style",
            TEAL,
            RGBColor(225, 243, 242),
        ),
        (
            "STAGE 3: GOVERN (RQ3)",
            "Enforce 5 YAML booking rules & post-gen sanitization (0% entity leakage, 98.6% compliance)",
            CORAL,
            RGBColor(253, 238, 236),
        ),
        (
            "STAGE 4: OPTIMIZE (RQ4)",
            "Lock stated slots in Informed Ledger + tailor package trade-offs (−29.5% to −42.7% turns)",
            GREEN,
            RGBColor(228, 246, 234),
        ),
    ]
    st_x = 0.35
    st_w = 2.94
    arr_w = 0.29
    for idx, (st_title, st_desc, hdr_c, bg_c) in enumerate(stages):
        bx = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(st_x), Inches(1.45), Inches(st_w), Inches(0.98))
        bx.adjustments[0] = 0.05
        bx.fill.solid()
        bx.fill.fore_color.rgb = bg_c
        bx.line.color.rgb = hdr_c
        bx.line.width = Pt(1.5)

        bh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(st_x), Inches(1.45), Inches(st_w), Inches(0.30))
        bh.adjustments[0] = 0.05
        bh.fill.solid()
        bh.fill.fore_color.rgb = hdr_c
        bh.line.fill.background()
        p_bh = bh.text_frame.paragraphs[0]
        p_bh.alignment = PP_ALIGN.CENTER
        _add_formatted_runs(p_bh, st_title, font_size=9.5, color=WHITE, bold=True)

        tb_s = s.shapes.add_textbox(Inches(st_x + 0.06), Inches(1.77), Inches(st_w - 0.12), Inches(0.62))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = Inches(0.01)
        p_s = tf_s.paragraphs[0]
        _add_formatted_runs(p_s, st_desc, font_size=8.6, color=DARK)

        if idx < 3:
            arr = s.shapes.add_shape(
                MSO_SHAPE.RIGHT_ARROW,
                Inches(st_x + st_w + 0.03),
                Inches(1.82),
                Inches(arr_w - 0.06),
                Inches(0.26),
            )
            arr.fill.solid()
            arr.fill.fore_color.rgb = GOLD
            arr.line.color.rgb = NAVY
            arr.line.width = Pt(0.75)
        st_x += st_w + arr_w

    # Detailed Causal Table below the visual storyline banner
    D.add_table(
        s, 0.35, 2.52, 12.63, 3.65,
        headers=[
            "Storyline Stage",
            "Research Question",
            "Manipulated IV (X) & Design",
            "Primary Measured DV (Y)",
            "Hypotheses (H0 vs. Ha)",
            "Causal Handoff to Next Stage",
        ],
        rows=[
            [
                "1. IDENTIFY\n(RQ1: Discovery\n& Routing)",
                "Which clustering algorithm best separates trajectories, and which early-routable user archetypes emerge?",
                "X1: Algorithm (K-Means, Ward, HDBSCAN) × Prefix Horizon M ∈ {3,5,7,9,whole} × Representation (N = 159 runs)",
                "Y1: Cosine Silhouette, Davies–Bouldin, Bootstrap ARI Stability, Out-of-Sample Prefix Routing κ",
                "H01: μ_Sil equal across algorithms.\nHa1: Algorithms differ (p<.05) & prefix Blocks yield stable (ARI≥.60), routable personas.",
                "Decision: Lock in K-Means (k=3) & M=9 `46-d Blocks`.\nCarries Forward → RQ2–RQ4: 3 Persona Labels, `RefinedArchetypeRouter` & 3 46-d FAISS Sub-Indices.",
            ],
            [
                "2. PERSONALIZE\n(RQ2: Style &\nPacing ICL)",
                "Does cluster-adaptive few-shot prompting improve style convergence and pacing calibration over baselines?",
                "X2: Prompting Strategy (Zero-Shot, Static Few-Shot k=3, Cluster-Adaptive k=3) on N = 33 dialogues (99 calls)",
                "Y2: De-lexicalized SBERT Style Cosine, Gemini 3,072-d Cosine, BERTScore F1, Pacing Word Error",
                "H02: μ_style equal across 3 prompts.\nHa2: Cluster-Adaptive > Static & Zero-Shot once upstream routing is coherent.",
                "Decision: Drop Static Few-Shot; lock in `Cluster-Adaptive` (k=3 46-d FAISS + Pacing Directives).\nCarries Forward → RQ3–RQ4: RQ1 Router + Validated Adaptive Prompting.",
            ],
            [
                "3. GOVERN\n(RQ3: Policy &\nLeakage Guard)",
                "How do a declarative rule engine and cluster-adaptive prompting interact to govern compliance and leakage?",
                "X3: 2 × 2 Factorial: Rules Mode (Off vs. Active) × Prompting (Zero-Shot vs. Cluster-Adaptive) (N = 144, n = 36/cell)",
                "Y3: Rule Adherence Rate (RAR)\nY4: Exemplar Leakage Rate (ELR)\nY5: Factual Slot F1 & Style Cosine",
                "H03: No main or interaction effects.\nHa3: Active rules raise RAR & Slot F1 and eliminate few-shot leakage (Interaction p<.05).",
                "Decision: Drop unmasked prompts; lock `Rules Active` ([SLOT] masking + 5 YAML rules) ON.\nCarries Forward → RQ4: Governed 46-d Cluster-Adaptive Generator.",
            ],
            [
                "4. OPTIMIZE\n(RQ4: Turn\nEconomy)",
                "Does governed cluster-adaptive prompting with an informed-slot ledger reduce turns to agreed quotation?",
                "X4: 2 × 3 Factorial: Prompting (Zero-Shot vs. Cluster-Adaptive) × Refined Archetype (DB, OE, RCS) (N = 180, n = 30/cell)",
                "Y6: Log Turns to Goal Completion (ln TGC), Raw Turns, Redundant Elicitation Rate (RER)",
                "H04: No main or interaction effects.\nHa4: Cluster-Adaptive cuts log turns & RER with a significant Prompt × Archetype interaction.",
                "Decision: Lock in Verified Slot Ledger (0% RER) + Persona Quotation Policies across the 3 `46-d Blocks` archetypes (−29.5% to −42.7% turns).",
            ],
        ],
        col_widths=[1.35, 2.25, 2.25, 2.05, 2.25, 2.48],
        font_size=9.3,
        align_left_cols=(0, 1, 2, 3, 4, 5),
        highlight_rows=(0, 1, 2, 3),
    )
    D.add_callout(
        s, 0.35, 6.26, 12.63, 0.84,
        "<b>Why the Storyline Order Matters:</b> Attempting to <i>Personalize (RQ2)</i> before solving outcome-free early routing in <i>Identify (RQ1)</i> failed (coarse routing κ = .24 gave <i>p</i> = .211). Attempting to <i>Optimize (RQ4)</i> without symbolic guardrails in <i>Govern (RQ3)</i> caused 55.6% entity hallucinations and 94.4% missed policy violations. All four stages are required.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=10.5,
    )

    # =========================================================================
    # SLIDE 8 (CONDENSED SLIDES 10 & 11): DATASET, SCHEMA, CLEANING & 70/30 SPLIT
    # =========================================================================
    s = D.content_slide(
        "4. Dataset, Hygiene & Exploratory Data Analysis",
        "Dataset Provenance, Two-Tier Schema, Cleaning Audit & Zero-Leakage Split",
        "Condensing corpus authenticity, Pydantic schema standardization, programmatic cleaning (N = 2,833), and the 70/30 discovery/test firewall",
        notes="This slide condenses Slides 10 and 11 from the full deck: covering why Frames and MultiWOZ were chosen, the Two-Tier schema, the cleaning audit table, and the strict 70/30 split.",
    )
    D.add_card(
        s, 0.35, 1.48, 5.45, 3.85,
        title="1. Corpus Provenance & Two-Tier Pydantic Schema",
        header_bg=NAVY,
        bullets=[
            "<b>Primary Corpus — Microsoft Frames (El Asri et al., 2017):</b>",
            (1, "1,369 human–human Wizard-of-Oz vacation negotiations (1,334 analytic; 19,986 turns). Built to capture multi-package comparison (`switch_frame`), budget ceilings, and 25.8% non-booking outcomes."),
            "<b>External Transfer Benchmark — MultiWOZ 2.2 (Zang et al., 2020):</b>",
            (1, "1,500 seeded dialogues (1,499 analytic) of transactional city-service slot-filling; used in RQ1 to test whether consultative archetypes are domain-specific."),
            "<b>Two-Tier Canonical Schema (`src/canonical_schema.py`):</b>",
            (1, "<b>Tier 1 (9 Universal Booking Slots):</b> `origin_city` (98.4%), `destination_city` (99.1%), `departure_date` (96.0%), `return_date` (91.2%), `duration_nights` (78.2%), `adults` (83.4%), `children` (25.0%), `budget_amount` (78.5%), `accommodation_tier` (69.5%)."),
            (1, "<b>Tier 2 (5 Enterprise Policy Slots — Seeded in RQ3):</b> `visa_processing_window_days` (<15d), `passport_expiry_months` (<6m), `traveler_count_adults` (>4 FIT), `discount_applied_percentage` (>15%), `minimum_budget_intl` (<$500/adult)."),
        ],
        font_size=9.5,
        bullet_spacing=2.5,
    )
    D.add_table(
        s, 5.95, 1.48, 7.03, 3.85,
        headers=["Quality Audit Check", "Detection Rule", "Frames (1,369)", "MultiWOZ (1,500)", "Programmatic Treatment"],
        rows=[
            ["Duplicate IDs / Empty turns", "Primary key / strip()", "0", "0", "Verified 100% unique & non-empty"],
            ["Exact duplicate text", "SHA-256 text hash", "1", "0", "Removed duplicate (`bf46892e...`)"],
            ["Aborted short dialogues", "total_turns < 3", "34", "1", "Excluded (need ≥ 3 turns for prefix routing)"],
            ["Long-tail turn outliers", "> Q3 + 1.5 × IQR", "20 (>30.5t)", "21 (>24.0t)", "Retained (real negotiations); log-transformed in RQ4"],
            ["Unobserved slot values", "Slot never stated", "Preserved", "Preserved", "Kept as explicit `None`; never synthetically imputed"],
            ["Entity leakage risk", "Regex slot/number match", "All exemplars", "All exemplars", "Masked with `[SLOT]` tokens in FAISS sub-indices"],
            ["Final Analytic Sample", "Locked post-cleaning", "1,334", "1,499", "Total N = 2,833 analytic human dialogues"],
        ],
        col_widths=[1.45, 1.35, 0.90, 0.95, 2.38],
        font_size=9.3,
        align_left_cols=(0, 1, 4),
        highlight_rows=(6,),
    )
    D.add_callout(
        s, 0.35, 5.45, 12.63, 1.65,
        "<b>Strict Zero-Leakage 70/30 Partitioning Firewall (`seed = 42`) & Resolution of Public Corpus Boundaries:</b>\n"
        "• <b>70% Golden Discovery Partition (D<sub>gold</sub>, n = 933) vs. 30% Held-Out Test Partition (D<sub>test</sub>, n = 401):</b> Stratified on wizard booking success (74.3% vs. 74.1%). Every clustering centroid, PCA projection matrix, prefix logistic router, and FAISS exemplar index is fitted <b>exclusively on D<sub>gold</sub> (n = 933)</b>. All RQ1 routing, RQ2 prompting (<i>N</i> = 33), RQ3 compliance (<i>N</i> = 144), and RQ4 multi-turn simulations (<i>N</i> = 180) run <b>strictly on D<sub>test</sub> (n = 401)</b>.\n"
        "• <b>Bridging Corpus Boundaries:</b> (1) Controlled Tier-2 policy states (50% violating / 50% compliant) are attached to real D<sub>test</sub> prefixes in RQ3; (2) Persona simulators in RQ4 are grounded in real D<sub>test</sub> trip goals and verified at <b>95.6% blind persona fidelity (κ = .933)</b> by an independent `gemini-2.5-pro` auditor.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.8,
    )

    # =========================================================================
    # SLIDE 9 (FROM SLIDE 12): UNIVARIATE & BIVARIATE EDA
    # =========================================================================
    s = D.content_slide(
        "4. Dataset, Hygiene & Exploratory Data Analysis",
        "Univariate and Bivariate Exploratory Data Analysis (Tables 6–7 & Figures 1–2)",
        "Dialogue length is driven by slot revisions (r = .602) and package offers (r = .636), validating the negotiation constructs",
        notes="Explain Figure 1 (univariate turn distributions) and Figure 2 + Table 7 (bivariate Pearson and Spearman correlations).",
    )
    D.add_figure(
        s, os.path.join(FIG_INT, "fig_eda_turns.png"),
        0.35, 1.50, 5.60, 2.55,
        caption="Figure 1: Univariate Turn Distributions (Frames M=14.90, SD=6.74 vs. MultiWOZ M=13.52, SD=4.46)",
    )
    D.add_figure(
        s, os.path.join(FIG_FIN, "fig_eda_bivariate.png"),
        0.35, 4.15, 5.60, 2.95,
        caption="Figure 2: Bivariate Turns vs. Slot Revisions & Archetype Negotiation Intensity",
    )
    D.add_table(
        s, 6.15, 1.50, 6.83, 3.10,
        headers=["Bivariate Variable Pair (Frames N = 1,334)", "Pearson r (p)", "Spearman ρ (p)", "Analytical Interpretation"],
        rows=[
            ["Dialogue Turns × Slot Revisions", ".602 (< .001)", ".582 (< .001)", "Frequent constraint changes drive longer sessions"],
            ["Dialogue Turns × Agent Package Offers", ".636 (< .001)", ".661 (< .001)", "Multi-package comparisons expand turn counts"],
            ["Slot Revisions × Hesitation Markers", ".192 (< .001)", ".206 (< .001)", "User uncertainty accompanies constraint shifts"],
            ["Slot Revisions × LLM Exploration Breadth", ".554 (< .001)", ".580 (< .001)", "Strong construct validity of LLM exploration rating"],
            ["Dialogue Turns × LLM Decisiveness", "−.229 (< .001)", "−.222 (< .001)", "Decisive travelers finish bookings in fewer turns"],
            ["User Words/Turn × Agent Words/Turn", "−.026 (.341)", ".014 (.618)", "Utterance verbosity is independent across speakers"],
        ],
        col_widths=[2.3, 1.0, 1.0, 2.5],
        font_size=9.5,
        align_left_cols=(0, 3),
        highlight_rows=(0, 1, 3, 4),
    )
    D.add_card(
        s, 6.15, 4.75, 6.83, 2.35,
        title="Key Takeaways from Univariate & Bivariate EDA",
        header_bg=NAVY,
        bullets=[
            "<b>Reporting Both Pearson <i>r</i> and Spearman ρ:</b> Turn counts and revision counts are right-skewed; reporting linear Pearson <i>r</i> alongside rank-based Spearman ρ confirms correlations are not artifacts of tail outliers.",
            "<b>Frames vs. MultiWOZ Dispersion:</b> Frames has 51% wider turn dispersion (<i>SD</i> = 6.74 vs. 4.46, range 3–47 turns) because consultative vacation negotiation involves iterative trade-offs.",
            "<b>Golden vs. Held-Out Balance:</b> Golden (<i>M</i> = 14.94 turns) and Held-Out (<i>M</i> = 14.81 turns) partitions are statistically indistinguishable, confirming an unbiased split.",
        ],
        font_size=10.5,
    )

    # =========================================================================
    # SLIDE 10 (FROM SLIDE 13): MULTIVARIATE EDA — SPEARMAN MATRIX & PCA BIPLOT
    # =========================================================================
    s = D.content_slide(
        "4. Dataset, Hygiene & Exploratory Data Analysis",
        "Multivariate EDA: Correlation Structure & Principal Component Biplot (Figure 3)",
        "Ten structural and behavioral variables span three orthogonal dimensions explaining 68.6% of total variance",
        notes="Explain Figure 3 (Panel A Spearman heatmap and Panel B PCA biplot) showing how travel behavior spans Exploration, Decisiveness, and Verbosity.",
    )
    D.add_figure(
        s, os.path.join(FIG_FIN, "fig_eda_multivariate.png"),
        0.35, 1.50, 7.45, 5.55,
        caption="Figure 3: Multivariate Spearman Rank Correlation Matrix (Panel A) & PCA Biplot by Refined Archetype (Panel B)",
    )
    D.add_table(
        s, 7.95, 1.50, 5.03, 3.55,
        headers=["Variable", "PC1 (40.8%)", "PC2 (17.2%)", "PC3 (10.6%)"],
        rows=[
            ["Total turns", "+.390", "+.014", "−.267"],
            ["User words / turn", "−.123", "+.019", "+.893"],
            ["Slot revisions", "+.416", "+.087", "+.078"],
            ["Agent package offers", "+.357", "−.015", "−.229"],
            ["Price sensitivity", "+.174", "−.426", "−.122"],
            ["Destination flexibility", "+.304", "+.347", "+.116"],
            ["Date flexibility", "+.298", "+.345", "+.069"],
            ["Exploration breadth", "+.392", "+.060", "+.167"],
            ["Decisiveness", "−.162", "−.509", "+.039"],
            ["Revision tendency", "+.379", "+.127", "+.128"],
        ],
        col_widths=[1.9, 1.0, 1.0, 1.0],
        font_size=9.5,
        align_left_cols=(0,),
        highlight_rows=(0, 1, 2, 7, 8),
    )
    D.add_card(
        s, 7.95, 5.18, 5.03, 1.87,
        title="How to Read the 3 Principal Components",
        header_bg=TEAL,
        bullets=[
            "<b>PC1 (40.8% var.) — Exploration vs. Rigidity:</b> Loaded on slot revisions (+.42), exploration breadth (+.39), and turns (+.39). Separates <i>Open Explorers</i> (right) from <i>Rigid-Constraint Seekers</i> (left).",
            "<b>PC2 (17.2% var.) — Decisiveness & Price Focus:</b> Loaded on decisiveness (−.51) and price sensitivity (−.43). Separates <i>Decisive Bookers</i> (bottom) from explorers.",
            "<b>PC3 (10.6% var.) — User Verbosity:</b> Isolates words per turn (+.89).",
        ],
        font_size=10,
    )

    # =========================================================================
    # SLIDE 11 (IMPROVED SLIDE 17): SAMPLE SIZES & HOW N=159 IS USED IN RQ1
    # =========================================================================
    s = D.content_slide(
        "5. Sample-Size Architecture & RQ1 Operationalization",
        "Sample-Size Derivation (α, β, f, λ, F_crit, N, n) & Operational Execution in RQ1",
        "Exact noncentral-F sample-size parameters across RQ1–RQ4 and how the derived N = 159 (n = 53/alg) is operationalized in RQ1",
        notes=(
            "Retains all exact statistical parameters (alpha=.05, beta=.20, power=.80, f=.25, lambda, F_crit, N_min, N, n) "
            "while focusing on how the derived sample size is practically executed in RQ1 and flows into RQ2–RQ4."
        ),
    )
    D.add_card(
        s, 0.35, 1.48, 5.45, 2.85,
        title="A Priori Power Parameters (Cohen, 1988; Faul et al., 2007)",
        header_bg=NAVY,
        bullets=[
            "<b>Noncentral-<i>F</i> Power Criterion:</b>  <b>1 − β = 1 − <i>F</i><sub>nc</sub>(<i>F</i><sub>crit</sub> ; <i>df</i><sub>1</sub>, <i>df</i><sub>2</sub>, λ) ≥ .80</b>",
            "<b>Fixed Design Parameters Across All Four RQs:</b>",
            (1, "<b>α = .05</b> (Type I error ceiling);  <b>β = .20 → Power (1 − β) = .80</b>;  <b><i>F</i><sub>crit</sub> = <i>F</i><sub>1−α</sub>(<i>df</i><sub>1</sub>, <i>df</i><sub>2</sub>)</b>."),
            (1, "<b>Target Effect Size:</b> Medium <b>Cohen's <i>f</i> = .25</b> (<i>f</i><sup>2</sup> = 0.0625; equivalent to η<sup>2</sup> = <i>f</i><sup>2</sup>/(1+<i>f</i><sup>2</sup>) = <b>.0588</b>)."),
            (1, "<b>Noncentrality Parameter (λ):</b>\n"
                "      • Between-subjects (RQ1, RQ3, RQ4):  <b>λ = <i>f</i><sup>2</sup> · <i>N</i> = 0.0625 · <i>N</i></b>  (needs λ = 8.00 at <i>df</i><sub>1</sub>=1; λ = 9.88 at <i>df</i><sub>1</sub>=2).\n"
                "      • Repeated-measures (RQ2, <i>m</i>=3, ρ=.50, ε=1.0):  <b>λ = <i>f</i><sup>2</sup> · <i>N</i> · <i>m</i> · ε / (1 − ρ) = 0.375 · <i>N</i></b>."),
            (1, "<b>Buffer Rule:</b> <b><i>N</i><sub>min</sub> + ≥10% buffer</b> rounded to exact cell multiples (<i>n</i> per group/cell)."),
        ],
        font_size=9.4,
        bullet_spacing=2,
    )
    D.add_table(
        s, 5.95, 1.48, 7.03, 2.85,
        headers=["RQ & Story Stage", "Experimental Design", "df1, df2 (at N_min)", "λ (at N_min)", "F_crit (α=.05)", "N_min (1−β=.80)", "Final Buffered N & Cell Size n", "Achieved Power"],
        rows=[
            ["RQ1 (Identify)", "One-Way ANOVA (k = 3 algs)", "2, 155", "9.88", "3.05", "158", "N = 159 (n = 53 / alg)", ".804"],
            ["RQ2 (Personalize)", "RM-ANOVA (m = 3, ρ = .50)", "2, 54", "10.50", "3.17", "28", "N = 33 (99 LLM calls)", ".865"],
            ["RQ3 (Govern)", "2 × 2 Factorial (df1 = 1)", "1, 124", "8.00", "3.92", "128", "N = 144 (n = 36 / cell)", ".847"],
            ["RQ4 (Optimize)", "2 × 3 Factorial (df1 = 2)", "2, 152", "9.88", "3.06", "158", "N = 180 (n = 30 / cell)", ".857"],
        ],
        col_widths=[1.10, 1.45, 0.78, 0.65, 0.65, 0.70, 1.15, 0.55],
        font_size=8.9,
        align_left_cols=(0, 1, 6),
        highlight_rows=(0, 1, 2, 3),
    )

    # Bottom 3-Column Visual Flow Card showing HOW Sample Sizes Are Used in RQ1 & Downstream RQs
    D.add_card(
        s, 0.35, 4.46, 4.08, 2.62,
        title="Step 1: How N = 159 (n = 53/alg) Is Used in RQ1A",
        header_bg=TEAL,
        bg_color=GREEN_BG,
        bullets=[
            "<b>Why Subsampling Is Required for ANOVA:</b>",
            (1, "Running K-Means once on <i>D</i><sub>gold</sub> (<i>n</i> = 933) yields only <b>1 Silhouette score</b>—impossible to compute within-group variance <i>MS</i><sub>error</sub>."),
            "<b>Generating N = 159 Independent Replications:</b>",
            (1, "Solving λ = 9.88 / 0.0625 gives <i>N</i><sub>min</sub> = 158 → buffered to <b><i>N</i> = 159 (<i>n</i> = 53 runs × 3 algorithms)</b>."),
            (1, "53 deterministic seeds (`1000..1052`) draw <b>53 random 80% subsamples (746 dialogues each)</b> from <i>D</i><sub>gold</sub> = 933."),
            (1, "Each subsample is clustered by K-Means (<i>n</i>=53), Ward (<i>n</i>=53), and HDBSCAN (<i>n</i>=53) → produces <b>159 Silhouette & DB observations</b> tested via One-Way ANOVA (<i>F</i>(2,156) = 91.33)."),
        ],
        font_size=8.9,
        bullet_spacing=2,
    )
    D.add_card(
        s, 4.62, 4.46, 4.08, 2.62,
        title="Step 2: Full D_gold (n = 933) Discovery in RQ1B",
        header_bg=BLUE,
        bullets=[
            "<b>Fitting the Operational Winner on All n = 933 Dialogues:</b>",
            (1, "Once the <i>N</i> = 159 benchmark proves <b>K-Means (<i>k</i> = 3)</b> is the operational winner (100% coverage vs. 39.1% HDBSCAN noise), K-Means is fitted on the full <b><i>D</i><sub>gold</sub> = 933</b> partition."),
            "<b>Bootstrap Stability & Truncation Grid (`step2g`):</b>",
            (1, "100 bootstrap resamples (80% draws) on <i>D</i><sub>gold</sub> = 933 evaluate prefix horizons <i>M</i> ∈ {3, 5, 7, 9, whole} across representations."),
            (1, "At <b><i>M</i> = 9 user messages (`Blocks`)</b>, bootstrap stability reaches <b>ARI = .89 (.87 ablation)</b>, and the 3 archetype centroids + L1/L2 prefix router + 3 FAISS sub-indices are frozen."),
        ],
        font_size=8.9,
        bullet_spacing=2,
    )
    D.add_card(
        s, 8.90, 4.46, 4.08, 2.62,
        title="Step 3: How D_test (n = 401) Feeds RQ1C & RQ2–RQ4",
        header_bg=GOLD,
        bg_color=CALLOUT_BG,
        bullets=[
            "<b>Out-of-Sample Routing Audit on D_test (n = 401):</b>",
            (1, "The frozen `Blocks` router is evaluated across all <b><i>n</i> = 401 held-out dialogues</b>, achieving <b>κ = .535 (70.1% at M=5)</b> and <b>κ = .958 (97.3% at M=9)</b>."),
            "<b>Stratified Sampling from D_test (n = 401) for RQ2–RQ4:</b>",
            (1, "• <b>RQ2 (<i>N</i> = 33, <i>n</i> = 11/archetype):</b> Tested across all 3 prompt modes = <b>99 paired LLM calls</b> (RM-ANOVA <i>df</i> = 2, 64)."),
            (1, "• <b>RQ3 (<i>N</i> = 144, <i>n</i> = 36/cell):</b> 36 held-out seeds (12/archetype) × 4 cells (50% rule-violating, 50% compliant; <i>df</i> = 1, 140)."),
            (1, "• <b>RQ4 (<i>N</i> = 180, <i>n</i> = 30/cell):</b> 60 held-out seeds/archetype across 2 prompt modes × 3 archetypes (<i>df</i> = 2, 174)."),
        ],
        font_size=8.9,
        bullet_spacing=2,
    )

    # =========================================================================
    # SLIDE 12 (FROM SLIDE 22): STAGE 1 — IDENTIFY (RQ1 PART 1: 159-RUN BENCHMARK)
    # =========================================================================
    s = D.content_slide(
        "Stage 1: IDENTIFY (RQ1 — Discovery & Routing)",
        "RQ1 (Part 1): Clustering Algorithm Benchmark Across N = 159 Subsample Runs",
        "Table 12 & Figures D1–D2: Rejecting H01 (p < .001) across both MiniLM (384-d) and Gemini (3,072-d) spaces",
        notes="Explain Table 12 and Figures D1-D2. Note that Welch's ANOVA and non-parametric Kruskal-Wallis / Friedman tests were also run and confirmed the exact same p < .001 result.",
    )
    D.add_figure(
        s, os.path.join(FIG_INT, "fig_rq1_k_selection.png"),
        0.35, 1.50, 5.45, 2.55,
        caption="Figure D1: Cluster-Number Selection (k = 2..8) on Golden Partition (k = 3 balances Silhouette & size ≥ 20%)",
    )
    D.add_figure(
        s, os.path.join(FIG_INT, "fig_rq1_silhouette.png"),
        0.35, 4.15, 5.45, 2.95,
        caption="Figure D2: Cosine Silhouette Across 159 Subsample Runs (53 per Algorithm) vs. Permutation Baseline",
    )
    D.add_table(
        s, 5.95, 1.50, 7.03, 3.15,
        headers=["Embedding Space & Algorithm", "Runs (n)", "Silhouette M (SD)", "Davies–Bouldin", "Omnibus ANOVA F (df = 2, 156)", "Effect Size η²"],
        rows=[
            ["1. MiniLM (384-d) — K-Means (k = 3) [Alg. Winner: 100% Cov.]", "53", ".147 (.019)", "3.129 (0.113)", "F = 91.33 (p < .001)", ".539"],
            ["2. MiniLM (384-d) — Agglomerative (Ward, k = 3)", "53", ".118 (.040)", "3.550 (0.269)", "Tukey KM > Ward: p < .001", "—"],
            ["3. MiniLM (384-d) — HDBSCAN (Drops 39.1% as noise!)", "53", ".211 (.044)*", "2.657 (0.241)*", "*Retains only 60.9% points", "—"],
            ["4. MiniLM (384-d) — Random Permutation Baseline", "53", "−.013 (.006)", "—", "Null chance reference", "—"],
            ["5. Gemini-001 (3,072-d Turn Pool) — KM / Ward / HDB*", "159 (53×3)", ".158 / .150 / .289*", "35.8% HDB noise*", "F = 77.09 (p < .001)", ".497"],
            ["6. Gemini-001 (3,072-d Document) [Best Space: KM=.161]", "159 (53×3)", ".161 / .213 / .345*", "25.7% HDB noise*", "F = 127.47 (p < .001)", ".620"],
        ],
        col_widths=[2.55, 0.68, 1.15, 1.02, 1.13, 0.50],
        font_size=9.0,
        align_left_cols=(0,),
        highlight_rows=(0, 4, 5),
    )
    D.add_card(
        s, 5.95, 4.78, 7.03, 2.32,
        title="How to Compare the 3 Highlighted Rows (Row 1 → Row 5 → Row 6)",
        header_bg=NAVY,
        bullets=[
            "<b>1. Why Row 1 Is Highlighted (Winning Algorithm = K-Means, k = 3):</b> Within MiniLM (Rows 1–4), HDBSCAN discards <b>39.1% of customers as noise</b>, and K-Means (.147) beats Ward (.118, <i>p</i> < .001) with <b>100% routing coverage</b>.",
            "<b>2. Why Row 6 Is the Best of the 3 Highlighted Rows (Row 1 < Row 5 < Row 6):</b> Upgrading from `MiniLM 384-d` (Row 1, KM = .147) to `Gemini 3,072-d Turn-Pool` (Row 5, KM = .158) and `Gemini 3,072-d Document` (Row 6) yields the <b>highest Silhouette (KM = .161, Ward = .213, HDB = .345) and largest effect size (F = 127.47, η² = .620)</b> because full-document Gemini preserves cross-turn context without MiniLM's 256-token cutoff.",
            "<b>3. What Moves Forward:</b> <b>Algorithm Winner (`K-Means k=3`) + Embedding Winner (`Gemini-001 Document`, Row 6)</b> are carried forward into the `46-d Blocks` model! (Welch & Kruskal–Wallis/Friedman checks also confirmed <i>p</i> < .001.)",
        ],
        font_size=9.1,
    )

    # =========================================================================
    # SLIDE 13 (FROM SLIDE 23): STAGE 1 — IDENTIFY (RQ1 PART 2: WHOLE-DIALOGUE DIAGNOSIS)
    # =========================================================================
    s = D.content_slide(
        "Stage 1: IDENTIFY (RQ1 — Discovery & Routing)",
        "RQ1 (Part 2): Cross-Corpus Transfer & Why Whole-Dialogue Clustering Failed Early Routing",
        "Figure D3 & Table D4: Diagnosing wizard confounding (V = .45) and outcome leakage (κ = .24) in full-transcript clusters",
        notes="Explain why clustering whole transcripts fails at runtime: at Turn 3, the end of the conversation hasn't happened yet!",
    )
    D.add_figure(
        s, os.path.join(FIG_INT, "fig_rq1_umap.png"),
        0.35, 1.50, 6.20, 5.55,
        caption="Figure D3: UMAP Projection of Frames Golden/Test Archetypes (Panel A) vs. MultiWOZ 2.2 Projection (Panel B)",
    )
    D.add_table(
        s, 6.70, 1.50, 6.28, 2.30,
        headers=["Partition / Corpus", "N", "Centroid Cosine M (SD)", "Direct Trans. (%)", "Constraint Neg. (%)", "Guided Exp. (%)"],
        rows=[
            ["Frames Golden (D_gold)", "933", ".466 (.116)", "42.3%", "37.6%", "20.0%"],
            ["Frames Held-Out (D_test)", "401", ".467 (.116)", "42.6%", "37.7%", "19.7%"],
            ["MultiWOZ 2.2 Sample", "1,499", ".269 (.115)", "71.4%", "28.6%", "0.1%"],
        ],
        col_widths=[1.7, 0.6, 1.3, 0.9, 0.9, 0.9],
        font_size=9.5,
        align_left_cols=(0,),
        highlight_rows=(0, 1),
    )
    D.add_card(
        s, 6.70, 3.92, 6.28, 3.13,
        title="Three Diagnostic Findings That Motivated the Prefix `Blocks` Breakthrough",
        header_bg=CORAL,
        bg_color=RED_BG,
        bullets=[
            "<b>1. Internal Stability vs. Cross-Corpus Specificity (Table D4):</b>",
            (1, "Within Frames, Golden (.466) and Held-Out (.467) centroid similarity matched perfectly (<i>t</i> = −0.10, <i>p</i> = .923). Projecting MultiWOZ dropped similarity to .269 (<i>t</i> = 28.08, <i>p</i> < .001) with 0.1% Guided Explorers—confirming consultative travel archetypes are domain-specific."),
            "<b>2. Wizard Role-Player Confounding (Cramér's V = .45):</b>",
            (1, "Pooling both user and wizard turns caused clusters to reflect <i>which human wizard</i> handled the chat rather than the customer's own persona."),
            "<b>3. Weak Early-Turn Prefix Routing (κ = .24, 39.4% Accuracy):</b>",
            (1, "Predicting a whole-dialogue cluster from the first 5 turns achieved only κ = .24 because whole-dialogue clusters separated sessions by how they <i>ended</i> (Turn 15 booking vs. walk-away), which is unknown during opening turns!"),
        ],
        font_size=9.8,
    )

    # =========================================================================
    # SLIDE 14 (FROM SLIDE 24): STAGE 1 — IDENTIFY (RQ1 PART 3: BLOCKS BREAKTHROUGH)
    # =========================================================================
    s = D.content_slide(
        "Stage 1: IDENTIFY (RQ1 — Discovery & Routing)",
        "RQ1 (Part 3): The Representation × Truncation Breakthrough (`Blocks` at M = 9)",
        "Figure D4 & Tables C2, D5–D6: Combining PCA-20 Gemini user prefixes + 16-field LLM behavioral profile on opening user messages",
        notes="Explain how restricting to user turns only, truncating to the first M=9 user messages, and combining PCA-20 Gemini embeddings with the 16-field behavioral profile solved early routing.",
    )
    D.add_figure(
        s, os.path.join(FIG_INT, "fig_rq1_truncation_2x2.png"),
        0.35, 1.50, 6.30, 5.55,
        caption="Figure D4: Bootstrap Stability (ARI), Core Membership, Early Routing, and Outcome Association Across M",
    )
    D.add_table(
        s, 6.80, 1.50, 6.18, 2.75,
        headers=["Prefix Horizon (m User Msgs / ≈T Turns)", "Dialogues > m", "Bootstrap ARI", "Held-Out Routing p_o (κ)", "p_o (<m / ≥m Msgs)", "Outcome V"],
        rows=[
            ["m = 3 user msgs (≈ 5 total turns)", "96.0%", ".57", "59.4% (κ = .359)", "87.5% / 58.2%", ".14"],
            ["m = 5 user msgs (≈ 9 turns — RQ2 Runtime)", "83.2%", ".84", "70.1% (κ = .535)", "81.8% / 67.8%", ".17"],
            ["m = 7 user msgs (≈ 13 total turns)", "59.9%", ".85", "82.0% (κ = .722)", "93.2% / 74.6%", ".18"],
            ["m = 9 user msgs (Adopted Golden Horizon)", "38.6%", ".89 (.87 abl.)", "97.3% (κ = .958)", "96.0% / 99.3%", ".20"],
            ["Whole conversation (Un-truncated)", "0.0%", ".62", "Confounded by outcome", "—", ".29"],
        ],
        col_widths=[1.85, 0.70, 0.72, 1.20, 1.13, 0.58],
        font_size=8.8,
        align_left_cols=(0,),
        highlight_rows=(1, 3),
    )
    D.add_card(
        s, 6.80, 4.38, 6.18, 2.67,
        title="How the 46-d `Blocks` Representation Unlocks Early Routing",
        header_bg=TEAL,
        bullets=[
            "<b>1. Three-Part Fix (`step2e` & `step2g`):</b> (a) Extract <b>user turns only</b> (eliminates wizard confounding); (b) Truncate at <b>first M = 9 user messages</b> (cuts outcome association from <i>V</i> = .29 to .20); (c) Concatenate <b>PCA-20 Gemini prefix embeddings + 26 encoded columns from the 16-field `UserBehaviour` codebook</b> (Fields 1–13 clustered; Fields 14–16 held out for audit).",
            "<b>2. Codebook Reliability & Validity (Table C2):</b> Test–retest reliability (<i>n</i> = 50) reached <b>κ_w = .87 to .96</b> (mean .91), and ground-truth correlations with Frames acts reached <b>Spearman ρ = .41 to .64 (p < .001)</b>.",
            "<b>3. Ablation Proof (Table D6):</b> Text embeddings alone at <i>M</i>=9 achieve ARI = .39; combining PCA-20 Gemini + behavioral ratings (`Blocks`) jumps stability to <b>ARI = .89 (.87 in ablation)</b> and held-out routing from <b>κ = .24 → .535 (M=5) → .958 (M=9)</b>!",
        ],
        font_size=9.5,
    )

    # =========================================================================
    # SLIDE 15 (FROM SLIDE 25): STAGE 1 — IDENTIFY (RQ1 PART 4: ARCHETYPE PROFILES)
    # =========================================================================
    s = D.content_slide(
        "Stage 1: IDENTIFY (RQ1 — Discovery & Routing)",
        "RQ1 (Part 4): Behavioral Profile of the Three Refined User Archetypes (Table 13)",
        "How the 16 schema fields differentiate Decisive Booker (45.0%), Open Explorer (25.5%), and Rigid-Constraint Seeker (29.5%)",
        notes="Walk through Table 13 showing how the three discovered archetypes differ across flexibility, exploration, decisiveness, revisions, and downstream prompting strategy.",
    )
    D.add_table(
        s, 0.35, 1.48, 12.63, 4.42,
        headers=["Schema Field Group & Behavioral Attribute (All 16 Fields)", "Archetype 1: Decisive Booker", "Archetype 2: Open Explorer", "Archetype 3: Rigid-Constraint Seeker", "Downstream Prompting & Policy Action (RQ2–RQ4)"],
        rows=[
            ["Golden (n=933) / Held-Out (n=401) Share", "420 (45.0%) / 165 (41.1%)", "238 (25.5%) / 140 (34.9%)", "275 (29.5%) / 96 (23.9%)", "Balanced partition (smallest cluster = 25.5% > 20% rule)"],
            ["Total Turns M (SD) / User Turns M", "14.96 (6.08) / 7.90", "17.99 (6.65) / 9.48", "10.64 (5.68) / 5.79", "Explorers converse 69% longer than Rigid-Constraint Seekers"],
            ["Fields 1–2 (ORD): Dest. / Date Flexibility", "2.54 / 2.57 (Moderate)", "3.49 / 2.77 (Open dest./dates)", "2.20 / 2.18 (Fixed city & dates)", "Offer multi-city alternatives only to Open Explorers"],
            ["Fields 3–4 (ORD): Exploration / Decisiveness", "1.97 (Focused) / 3.97 (Decisive)", "2.96 (Broad) / 2.58 (Deliberative)", "1.59 (Narrow) / 3.23 (Firm)", "Present 2–3 side-by-side options to Open Explorers"],
            ["Fields 5–6 (ORD): Detail / Revision Tendency", "2.39 / 2.00 (Low revisions)", "2.87 / 3.03 (Frequent pivots)", "1.46 / 2.40 (Constraint-focused)", "Proactive dual trade-off framing for Rigid-Constraint Seekers"],
            ["Fields 7–8 (ORD): Question Asking / Politeness", "2.05 / 4.26 (Warm, direct)", "2.72 / 3.80 (Inquisitive)", "1.43 / 3.07 (Terse, direct)", "Fast booking confirmation (~13w norm) for Decisive Bookers"],
            ["Fields 9–10 (ORD): Price Sens. / Info Upfront", "3.20 / 2.18 (Stated early)", "3.18 / 1.82 (Gradual disclosure)", "3.12 / 2.16 (Hard ceiling)", "Calibrate budget-ceiling and package-tier emphasis"],
            ["Fields 11–13 (CAT Cluster): Goal / Sec. / Tone", "0.5% Exp, 99.3% Book | 52.4% Pos", "39.1% Exp, 50.8% Book | 69.3% Neut", "2.2% Exp, 89.8% Book | 7.6% Pos", "One-hot / multi-hot encoded into 16 binary cols (10+16 = 26 cols)"],
            ["Fields 14–16 (AUDIT Only): Outcome / Party / Flag", "90.5% Booked | 37.1% Solo/Cpl", "68.1% Booked | 44.5% Solo/Cpl", "28.0% Booked (68.0% None)", "Excluded from clustering to guarantee zero outcome leakage!"],
        ],
        col_widths=[2.85, 2.25, 2.35, 2.35, 2.83],
        font_size=8.8,
        align_left_cols=(0, 4),
        highlight_rows=(0, 2, 3, 7, 8),
    )
    D.add_callout(
        s, 0.35, 5.98, 12.63, 1.05,
        "<b>Stage 1 (IDENTIFY) Handoff to Stage 2 (PERSONALIZE):</b>\n"
        "Unsupervised K-Means integer IDs (`0, 1, 2`) are deterministically mapped via golden centroid maxima (`idxmax(destination_flexibility)` → <i>Open Explorer</i>; `idxmax(decisiveness)` → <i>Decisive Booker</i>; remaining → <i>Rigid-Constraint Seeker</i>). "
        "The frozen `RefinedArchetypeRouter` predicts these personas on held-out test prefixes (`κ = .535` at <i>M</i>=5 for mid-dialogue RQ2 prompting; `κ = .958` at <i>M</i>=9 for RQ4 multi-turn policy selection).",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.8,
    )

