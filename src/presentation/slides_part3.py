"""
Part 3 of the QM640 Capstone Defense Presentation (Slides 49–66):
  - Module 9 (Slides 49–51): Consolidated Scorecard, Operational ROI, Production Microservice Runtime & Limitations Mapped to the 4-Stage Solution Approach
  - Module 10 (Slides 52–57): Doctoral Dissertation Frontiers & Pictorial Architecture Mapped Directly to the 4-Stage Solution Approach:
      * Slide 52: Hierarchical Context × Behavior (C × K) & 3 × 6 = 18 Call-Stage FAISS Retrieval Mechanics
      * Slide 53: Soft-Mixture Archetype Blending (w_1..w_K) & Turn-by-Turn Bayesian Persona Drift P(z_t | u_1..t)
      * Slide 54: Multi-Interaction Opportunity_ID Turn Economy (TTL, TTQ_s, CSET) & Cold/Warm/Hot Lead Carry-Over
      * Slide 55: Six Doctoral Methodological Pillars (P1–P6) Mapped to Identify → Personalize → Govern → Optimize
      * Slide 56: Pictorial Capstone-to-Doctoral Architecture Under the 4-Stage Solution Approach Columns
      * Slide 57: End-to-End Data Flow Diagram (DFD): Cosine FAISS DB + Historical Turn-Economy DB (Turn-Q) + 200-Pkg USP DB
  - Module 11 (Slides 58–66): Anticipated Defense Committee Q&A Bank & Concluding Summary (All Aligned with the 4-Stage Solution Approach)
"""

from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt
from presentation.ppt_styles import (
    BLUE,
    CALLOUT_BG,
    CARD_ALT,
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
from report.final_context import REPO


def build_slides_part3(D, ctx):
    # =========================================================================
    # SLIDE 49: CONSOLIDATED HYPOTHESIS SCORECARD (TABLE 11) & ENTERPRISE ROI
    # =========================================================================
    s = D.content_slide(
        "9. Cumulative Synthesis, ROI & Production Runtime",
        "Consolidated Hypothesis Scorecard (Table 11) & Operational ROI",
        "All four null hypotheses (H01–H04) rejected at p < .001 with large effect sizes and substantial operational savings",
        notes="Present Table 11 as the master executive summary of all empirical findings across RQ1-Identify to RQ4-Optimize, followed by the illustrative 1,000,000-session operational scenario.",
    )
    D.add_table(
        s, 0.35, 1.46, 12.63, 3.10,
        headers=[
            "Solution Stage & Research Question (Table 11)",
            "Sample & Design",
            "Baseline vs. Proposed Performance",
            "Primary Parametric Test & Effect Size",
            "Robust / Non-Parametric Check",
            "Decision",
        ],
        rows=[
            [
                "RQ1-Identify Stage:\nAlgorithm Separation &\nRefined Prefix Routing",
                "N = 159 runs\n(D_gold=933,\nD_test=401)",
                "Perm. Sil = −.013 vs. KM = .147 / .161 (100% cov.);\nBlocks ARI = .89 (.87); Test κ = .535 (M=5) to .958 (M=9)",
                "One-way F(2, 156) = 91.33 / 127.47, η² = .54–.62\nMatched RM F(1.72, 89.30) = 83.04, ηp² = .615",
                "Friedman χ²(2) = 56.30, p < .001;\nWelch F = 66.98; Kruskal H = 86.82",
                "Reject H01\n(p < .001)",
            ],
            [
                "RQ2-Personalize Stage:\nStyle Convergence &\nPacing Error (Refined)",
                "N = 33 chats × 3\nprompts (99 calls)",
                "Style Cos: Static = .453, Zero = .530 vs. Adaptive = .597\nPacing Error: Zero = 10.12w, Static = 6.33w vs. Adaptive = 3.87w",
                "Style F(1.88, 60.29) = 9.79, p < .001, ηp² = .234\nPacing F(1.30, 41.70) = 7.10, p = .007, ηp² = .182",
                "Friedman χ² = 12.50 (p = .002) &\n14.27 (p < .001); Holm p < .001",
                "Reject H02\n(p < .001)",
            ],
            [
                "RQ3-Govern Stage:\nPolicy Rule Adherence,\nLeakage & Slot F1",
                "N = 144 (2 × 2,\nn = 36/cell;\nκ_judge = .917)",
                "Viol. Sens.: 5.6% (Off) → 98.6% (Active); Comp. Spec.: 94.4% vs 88.9%\nFew-Shot Leakage: .359 (55.6%) → .000 (0.0%); Slot F1: .485 → .952",
                "RAR Acc F(1, 140) = 43.92; Sens F(1, 68) = 498.78\nELR Int. F = 34.82, p < .001; Slot F1 F = 489.52",
                "Sum-HC3 F = 42.71 & 33.85 (< .001);\nART F = 39.12 & 2148.81 (< .001)",
                "Reject H03\n(p < .001)",
            ],
            [
                "RQ4-Optimize Stage:\nMulti-Turn Economy\n(Log Turns & RER)",
                "N = 180 (2 × 3,\nn = 30/cell;\nκ_persona = .933)",
                "Turns: −34.2% (DB), −29.5% (OE), −42.7% (RCS)\nOverall Turns: 7.93 → 5.09 (−35.8%); RER: .109 → .000",
                "Prompt F(1, 174) = 664.43, p < .001, ηp² = .793\nPrompt × Arch Int. F(2, 174) = 10.89, p < .001, ηp² = .111",
                "HC3 Int. F = 8.58, p < .001;\nART Int. F = 209.46, p < .001",
                "Reject H04\n(p < .001)",
            ],
        ],
        col_widths=[2.05, 1.50, 3.15, 2.50, 2.20, 1.23],
        font_size=8.6,
        align_left_cols=(0, 1, 2, 3, 4),
        highlight_rows=(0, 1, 2, 3),
    )
    D.add_card(
        s, 0.35, 4.66, 12.63, 1.62,
        title="Illustrative Operational Scenario (Hypothetical Enterprise OTA Handling 1,000,000 Monthly Sessions)",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>1. Cloud Token & Latency Compression (`−35.8%`, RQ4-Optimize):</b> Compressing mean session length from `7.93` (`Zero-Shot`) to `5.09` (`Cluster-Adaptive`) corresponds to <b>`2.84 fewer messages per session` (`≈ 2.84M fewer LLM calls/month`)</b> while adding `< 4 ms` of local CPU overhead per turn (`< 2 ms` router + `< 1 ms` FAISS + `< 1 ms` `RuleEngine`).",
            "<b>2. Zero Exemplar Entity Leakage & Policy Shield (`RQ3-Govern`):</b> Eliminating few-shot entity leakage (`55.6% → 0.0%`) and lifting violation enforcement sensitivity from `5.6% to 98.6%` (`F = 498.78`) prevents unauthorized discounts and invalid international visa/passport bookings.",
            "<b>3. Rescuing High-Friction Shoppers (`RQ1-Identify, RQ2-Personalize & RQ4-Optimize`):</b> Proactive dual trade-off framing cuts negotiation turns by <b>`42.7%` (`8.73 → 5.00 turns`)</b> for <i>Rigid-Constraint Seekers</i> (`68.0%` historical walk-away rate).",
        ],
        font_size=9.1,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Synthesis:</b> "
        "Table 11 demonstrates that business optimization in `RQ4-Optimize (−35.8% turns, .000 RER)` is the cumulative payoff of `RQ1-Identify (Identify: κ=.535/.958)` → `RQ2-Personalize (Personalize: +31.8% style, 3.87w pacing)` → `RQ3-Govern (Govern: 0.0% leakage, 98.6% violation sensitivity)`.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 50: PRODUCTION MICROSERVICE DEPLOYMENT & DALLAS-TO-TOKYO WALKTHROUGH
    # =========================================================================
    s = D.content_slide(
        "9. Cumulative Synthesis, ROI & Production Runtime",
        "Production Microservice Runtime & End-to-End Tokyo Use Case",
        "Tracing a single live customer request through all 4 stages (`Identify → Personalize → Govern → Optimize`) in < 4 ms local overhead",
        notes="Show how the 4 stages execute as a stateless FastAPI/Pydantic microservice on a concrete Dallas-to-Tokyo Rigid-Constraint Seeker session.",
    )
    D.add_card(
        s, 0.35, 1.48, 6.15, 4.78,
        title="Stateless Microservice Pipeline (`src/final_pipeline/`)",
        header_bg=NAVY,
        bullets=[
            "<b>Step 1 — Canonical State Ingestion (`src/canonical_schema.py`):</b>",
            (1, "Parses incoming webhook JSON into a validated `CanonicalDialogue` object (`Tier1CoreSlots` + `Tier2PolicySlots`) and updates the `Verified Informed Slot Ledger`."),
            "<b>Step 2 — RQ1-Identify (`IDENTIFY` — `< 2 ms` CPU):</b>",
            (1, "`RefinedArchetypeRouter` (`routing.py`) projects the opening user prefix (`min(M, 9)`) into `46-d Blocks` and predicts winning archetype `k* ∈ {DB, OE, RCS}`."),
            "<b>Step 3 — RQ2-Personalize (`PERSONALIZE` — `< 1 ms` CPU):</b>",
            (1, "Queries `FAISS_Index[k*]` (`IndexFlatIP(46)`) for the top `k_shot = 3` `[SLOT]`-masked exemplars and loads persona word-pacing target `μ_k` (`12.9w / 18.6w / 14.8w`)."),
            "<b>Step 4 — RQ3-Govern (`GOVERN` — `< 1 ms` CPU):</b>",
            (1, "`DeclarativeRuleEngine` (`rule_engine.py`) evaluates all 5 `YAML` policies pre-generation and sanitizes any residual exemplar entities post-generation."),
            "<b>Step 5 — RQ4-Optimize (`OPTIMIZE` — Turn-Economy Action):</b>",
            (1, "Injects missing-slot bundle + persona package policy (`1-Opt Confirm / 3-Opt Compare / Dual Trade-Off`)."),
        ],
        font_size=9.1,
    )
    D.add_card(
        s, 6.80, 1.48, 6.18, 4.78,
        title="Live Trace: Dallas → Tokyo Rigid-Constraint Seeker",
        header_bg=TEAL,
        bullets=[
            "<b>Incoming User Prefix (`U1–U2`):</b>",
            (1, "<i>'I need a 5-star hotel in Tokyo from Dallas departing in 9 days for 9 nights, 2 adults, strict $2,600 budget—no other stars.'</i>"),
            "<b>1. RQ1-Identify (`IDENTIFY` Output):</b>",
            (1, "Router scores `P(RCS) = .94` (`Rigid-Constraint Seeker`: low date/dest flexibility `2.18`, hard ceiling). Routes to <b>`FAISS_Index[3]` (`n = 275`)</b>."),
            "<b>2. RQ2-Personalize (`PERSONALIZE` Output):</b>",
            (1, "Retrieves 3 `[SLOT]`-masked `RCS` trade-off exemplars + sets target pacing directive to <b>`14.8 words`</b>."),
            "<b>3. RQ3-Govern (`GOVERN` Output):</b>",
            (1, "`RuleEngine` flags `RULE_VISA_LEAD_TIME` (`9 days < 15 days` international lead window) and verifies `0` leaked exemplar tokens."),
            "<b>4. RQ4-Optimize (`OPTIMIZE` Output — Closed in 5.00 Turns, `RER = 0.0%`):</b>",
            (1, "Explains the 9-day visa check AND presents the <b>Dual Trade-Off</b> (`Option A: 4★ exact dates $2,288` vs. `Option D: 5★ +3d shifted dates $2,444`—which also resolves the 15-day visa window!), closing quotation agreement on Turn 5!"),
        ],
        font_size=9.0,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Engineering Takeaway:</b> "
        "Notice how the Tokyo trace integrates all 4 stages in one reply: `RQ1-Identify` detects the rigid persona, `RQ2-Personalize` sets crisp 15-word trade-off phrasing, `RQ3-Govern` catches the 9-day visa violation, and `RQ4-Optimize`'s `+3d` shifted-date `Option D` simultaneously solves both the `$2,600` budget conflict AND the `15-day` visa rule!",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.3,
    )

    # =========================================================================
    # SLIDE 51: STUDY LIMITATIONS & SCOPE BOUNDARIES MAPPED TO THE STORYLINE
    # =========================================================================
    s = D.content_slide(
        "9. Cumulative Synthesis, ROI & Production Runtime",
        "Study Limitations & Scope Boundaries Mapped to the 4-Stage Solution Approach",
        "Transparently bounding the master's capstone across RQ1-Identify to RQ4-Optimize and showing how each boundary seeds the Doctoral Roadmap",
        notes="Present the 6 methodological limitations transparently, mapping each to its solution approach stage and corresponding doctoral dissertation extension.",
    )
    D.add_table(
        s, 0.35, 1.46, 12.63, 4.80,
        headers=[
            "Solution Stage",
            "Scope Boundary / Limitation in Master's Capstone",
            "Mitigation Applied in This Study",
            "Doctoral Dissertation Extension Seeded",
        ],
        rows=[
            [
                "RQ1-Identify Stage:\nHard K-Means (k=3) &\nStatic Opening Prefix",
                "1. Hard `k = 3` assignment treats `25.2%` boundary speakers (`s < .05`) as discrete and does not update persona if a user shifts mid-call after price shock.\n2. Clusters behavior in 1D without crossing macro trip stakes (`party_type, budget_stakes`).",
                "Verified `93.1%` bootstrap core stability (`ARI = .89`) and evaluated prefix routing across `m ∈ {3, 5, 7, 9}` (`Table 12`).",
                "<b>Doctoral Pillars 1 & 2:</b>\nTwo-Tier `C × K` (`24–36` micro-clusters) + Soft-Mixture weights (`w_1..w_K`) & Bayesian drift `P(z_t | u_1..t)`.",
            ],
            [
                "RQ2-Personalize Stage:\nSingle-Stage FAISS &\nBackward Cosine",
                "3. Uses 1 FAISS sub-index per persona (`k = 3`) across the whole chat rather than sub-indexing by enterprise call stage (`a–f`).\n4. Cosine similarity `cos(q_t, e_j)` looks backward at phrasing and ignores remaining turns to quote (`DTQ`).",
                "Paired `[SLOT]`-masked FAISS exemplars with persona word-pacing directives (`F = 9.79, p < .001; 3.87w error`).",
                "<b>Doctoral Pillars 3 & 6:</b>\n`3 × 6 = 18` `(Persona × Stage a–f)` FAISS DB + Historical Turn-Economy DB (`Turn-Q DB`, `DTQ`).",
            ],
            [
                "RQ3-Govern Stage:\nSeeded Tier-2 Policy\nInjection",
                "5. Public corpora (`Frames, MultiWOZ`) contain `0.0%` natural Tier-2 visa, passport, or promo cap slots (`Table E4`), requiring seeded experimental injection (`seed=42`).",
                "Preserved authentic `D_test` user prefixes, balanced `50%` violating / `50%` compliant cells (`N=144`), and verified via `gemini-2.5-pro` (`κ = .917`).",
                "<b>Doctoral Pillar 3 (Stage e):</b>\nLive OTA CRM & GDS policy integration across regional visa/passport APIs.",
            ],
            [
                "RQ4-Optimize Stage:\nSingle-Session 4-Pkg\nSimulator vs. Multi-Call",
                "6. Evaluates single-session turn economy across a 4-option package catalog (`Options A–D`) with an LLM user simulator (`N=180`) rather than 200+ packages across 4–5 repeat CRM calls/chats.",
                "Grounded seeds in 180 real `D_test` trips, audited persona fidelity (`95.6%, κ = .933`), and contextualized against human logs (`Table E5`).",
                "<b>Doctoral Pillars 4 & 5:</b>\n`200-Pkg USP Info-Gain Tree` + Multi-Call `Opportunity_ID` (`TTL, TTQ_s, CSET`) & `Cold/Warm/Hot` lead state.",
            ],
        ],
        col_widths=[1.85, 4.15, 3.35, 3.28],
        font_size=8.8,
        align_left_cols=(0, 1, 2, 3),
        highlight_rows=(0, 1, 2, 3),
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Transition to Doctoral Extensions (`Slides 52–57`):</b> "
        "Every limitation of the master's capstone maps cleanly onto a specific stage of `Identify → Personalize → Govern → Optimize`—motivating the architectural deep-dives on the next 6 slides.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 52: DOCTORAL FRONTIER 1 — HIERARCHICAL (C × K) & 3 × 6 = 18 FAISS RETRIEVAL MECHANICS
    # =========================================================================
    s = D.content_slide(
        "10. Doctoral Roadmap Aligned with the 4-Stage Solution Approach",
        "Doctoral Frontier 1 (RQ1-Identify & RQ2-Personalize): When Cluster Count ≠ FAISS Index Count",
        "How retrieval works when K = 3 behavioral clusters are crossed with 6 Call Stages (3 × 6 = 18 FAISS DBs) or Context Regimes (C × K)",
        notes=(
            "Directly explain how FAISS retrieval works when the number of behavioral clusters (K=3) does not match the number of FAISS sub-indices "
            "(such as 3 Personas x 6 Call Stages = 18 FAISS indices, or Context C x Behavior K). Walk through the Two-Coordinate Routing Key, Physical Partitioning with Hierarchical Back-Off, and Metadata-Filtered Retrieval."
        ),
    )
    D.add_card(
        s, 0.35, 1.48, 4.05, 4.78,
        title="1. Current Capstone (`RQ1 → RQ2`):\n1:1 Match (`K = 3` Clusters = `3` FAISS DBs)",
        header_bg=NAVY,
        bullets=[
            "<b>Current 1-to-1 Architecture (`D_gold = 933`):</b>",
            (1, "• `RQ1-Identify` K-Means produces <b>`K = 3` behavioral clusters</b>."),
            (1, "• `RQ2-Personalize` builds <b>`3` `faiss.IndexFlatIP(46)` indices</b> (`n = 420 DB, 238 OE, 275 RCS`)."),
            "<b>Why Enterprise Scale Breaks 1-to-1 Matching:</b>",
            (1, "• <b>Dimension A — Situational Trip Context (`C`):</b> `party_type` (Solo/Couple/Family/Group), `budget_stakes` (Economy/Luxury), and `lead_window` (Last-Minute/Advance) modify how a persona behaves (`C × K = 24–36` cells)."),
            (1, "• <b>Dimension B — 6 Consultative Call Stages (`S ∈ {a..f}`):</b>\n"
                "  `(a)` Opening → `(b)` Mandatory Slots → `(c)` Positioning → `(d)` Negotiation → `(e)` Compliance → `(f)` Closure (`3 × 6 = 18` cells)."),
            (1, "<b>The Mismatch Question:</b> When `K = 3` behavioral clusters map to `18` (or `C × K × 6`) FAISS partitions, how does runtime retrieval work without sample starvation?"),
        ],
        font_size=8.8,
    )
    D.add_card(
        s, 4.60, 1.48, 4.10, 4.78,
        title="2. Solution A: Two-Coordinate Routing Key\n& Hierarchical Back-Off (`3 × 6 = 18` DBs)",
        header_bg=TEAL,
        bullets=[
            "<b>Decoupling <i>WHO</i> (`k*`) from <i>WHERE</i> (`s*` & `c*`):</b>",
            (1, "• <b>Coordinate 1 (`k* ∈ {1,2,3}` — Neural Router):</b> `RefinedArchetypeRouter` predicts behavioral persona `k*` from `46-d Blocks`."),
            (1, "• <b>Coordinate 2 (`s* ∈ {a..f}, c*` — Symbolic FSM):</b> Deterministic state tracker reads the `Verified Slot Ledger` & `RuleEngine` to identify active call stage `s*` and trip regime `c*`."),
            "<b>Composite Lookup `Index_ID = (c*, k*, s*)` with 3-Level Hierarchical Back-Off:</b>",
            (1, "1. <b>Level 3 (Exact Cell `(c*, k*, s*)`):</b> If cell has `n ≥ 15` golden turns, retrieve `k_shot = 3` from `FAISS[c*, k*, s*]`."),
            (1, "2. <b>Level 2 (Persona × Stage `(k*, s*)` Back-Off):</b> If sparse (`n < 15`), fall back to the `3 × 6 = 18` parent index `FAISS[k*, s*]`."),
            (1, "3. <b>Level 1 (Macro Persona `k*` Back-Off):</b> Guaranteed fallback to Capstone's `FAISS[k*]` (`n ≥ 238`)!"),
        ],
        font_size=8.7,
    )
    D.add_card(
        s, 8.90, 1.48, 4.08, 4.78,
        title="3. Solution B: Single Parent FAISS Index\n+ Metadata Filtering / Re-Ranking",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>Alternative Without Splitting Into Tiny Indices:</b>",
            (1, "Keep <b>`3` large parent FAISS indices (`1 per K = 3 persona`)</b>—or `18` `(K × Stage)` indices—and store `party_type`, `budget_stakes`, `lead_window`, and `stage` as <b>vector metadata payloads</b>."),
            "<b>Two-Stage Retrieval Execution (`< 2 ms`):</b>",
            (1, "• <b>Step 1 (Wide Cosine Candidate Fetch):</b> Query parent persona index `FAISS[k*]` for the <b>top `M = 20`</b> nearest vectors by `46-d Blocks` cosine `cos(q_t, e_j)`."),
            (1, "• <b>Step 2 (Symbolic Metadata Filter & Re-Rank):</b> Filter/boost candidates matching active stage `s*` and context `c*`:\n"
                "  <b>`Score(e_j) = α·cos(q_t, e_j) + β·I(stage=s*) + γ·Sim_context(c*, c_j)`</b>"),
            (1, "• <b>Result:</b> Selects top `k_shot = 3` exemplars with zero empty-cell failures!"),
        ],
        font_size=8.7,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`Firms Up RQ1-Identify → RQ2-Personalize`):</b> "
        "Whether implemented via <b>`3 × 6 = 18` physical sub-indices with hierarchical back-off</b> or <b>top-20 parent FAISS retrieval with metadata re-ranking</b>, RQ1-Identify's neural router (`WHO`) and RQ3–RQ4's symbolic slot ledger (`WHERE in call stages a–f`) combine seamlessly without ever starving `RQ2-Personalize` of exemplars.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.2,
    )

    # =========================================================================
    # SLIDE 53: DOCTORAL FRONTIER 2 — SOFT-MIXTURE BLENDING & BAYESIAN PERSONA DRIFT
    # =========================================================================
    s = D.content_slide(
        "10. Doctoral Roadmap Aligned with the 4-Stage Solution Approach",
        "Doctoral Frontier 2 (RQ1-Identify & RQ2-Personalize): Soft-Mixture & Bayesian Persona Drift",
        "Replacing hard early-turn cluster lock-in with continuous softmax blending (w_1..w_K) and turn-by-turn Bayesian updating P(z_t | u_1..t)",
        notes="Explain Soft-Mixture routing and Bayesian Persona Drift clearly, showing how they solve the 25.2% boundary speaker overlap and mid-conversation persona shifts after price shock.",
    )
    D.add_card(
        s, 0.35, 1.48, 6.15, 4.78,
        title="Part 1: What Is 'Soft-Mixture Routing' (`w_1, w_2, w_3`)?\n(Solving the 25.2% Boundary Speaker Overlap in RQ1-Identify)",
        header_bg=NAVY,
        bullets=[
            "<b>The Hard-Clustering Limitation in Capstone RQ1:</b>",
            (1, "As shown in the PCA Biplot (`Figure 3`), traveler behavior forms a continuous manifold where <b>`25.2%` of speakers sit near cluster boundaries (`Silhouette s_i < .05`)</b>—e.g., `55% Open Explorer + 45% Rigid-Constraint Seeker`."),
            (1, "Hard `argmax` routing forces `100%` of the prompt into a single cluster, ignoring the secondary trait."),
            "<b>How Soft-Mixture Routing Works:</b>",
            (1, "• <b>Probability Vector:</b> The L1 logistic router outputs a continuous softmax distribution `w_t = [w_DB, w_OE, w_RCS]` (e.g., `[0.05, 0.60, 0.35]`)."),
            (1, "• <b>Proportional Multi-Index FAISS Retrieval (`k_shot = 3`):</b> Allocates exemplar slots proportionally across the 3 FAISS sub-indices: <b>`round(3 × 0.60) = 2` exemplars from `FAISS[OE]` + `round(3 × 0.35) = 1` exemplar from `FAISS[RCS]`</b>!"),
            (1, "• <b>Interpolated Word Pacing Target:</b> Computes weighted target length `μ_target = Σ w_k μ_k = 0.05(12.9) + 0.60(18.6) + 0.35(14.8) = 16.9 words`."),
        ],
        font_size=8.9,
    )
    D.add_card(
        s, 6.80, 1.48, 6.18, 4.78,
        title="Part 2: What Is 'Bayesian Persona Drift' (`P(z_t | u_1..t)`)?\n(Tracking Mid-Call Shifts & Warm-Starting Repeat Calls)",
        header_bg=TEAL,
        bullets=[
            "<b>Why Personas Drift During a Conversation:</b>",
            (1, "A traveler often starts at Turn 1–3 as an <b>`Open Explorer`</b> (<i>'What beach resorts do you have in August?'</i>). Once quoted `$3,400` at Turn 5, <b>price shock</b> triggers a shift into a <b>`Rigid-Constraint Seeker`</b> (<i>'Strictly under $2,200 with a 4★ hotel!'</i>)."),
            "<b>Recursive Bayesian State Filtering Formula:</b>",
            (1, "Instead of freezing the persona at `M = 5`, treat latent persona `z_t ∈ {1..K}` as a Markov state updated after every user turn `u_t`:"),
            (1, "<b>`P(z_t = k | u_1..t) ∝ P(u_t | z_t = k) · Σ_j T_{j→k} P(z_{t−1} = j | u_1..t−1)`</b>"),
            (2, "• <b>Prior `P(z_{t−1})`:</b> Persona belief from previous turn (or carried over from **Session `s−1`** of the same `Opportunity_ID`!)."),
            (2, "• <b>Transition Matrix `T_{j→k}`:</b> Captures natural drift (e.g., `P(OE → RCS | price_conflict) = .38`)."),
            (2, "• <b>Likelihood `P(u_t | z_t = k)`:</b> Scored from latest turn act (`switch_frame` vs. `reject_budget`) and incremental `46-d Blocks` coordinates."),
        ],
        font_size=8.8,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`Upgrading RQ1-Identify → RQ2-Personalize`):</b> "
        "<b>Soft-Mixture</b> upgrades RQ1-Identify from a hard switch to a <i>continuous style blender</i> for boundary shoppers, while <b>Bayesian Drift</b> makes RQ1-Identify→2 routing <i>closed-loop</i>—instantly shifting FAISS retrieval from `3-Option Comparison` to `Dual Trade-Off Framing` when mid-call price shock occurs!",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.2,
    )

    # =========================================================================
    # SLIDE 54: DOCTORAL FRONTIER 3 — MULTI-CALL OPPORTUNITY_ID TURN ECONOMY & LEAD STATUS
    # =========================================================================
    s = D.content_slide(
        "10. Doctoral Roadmap Aligned with the 4-Stage Solution Approach",
        "Doctoral Frontier 3 (RQ3-Govern & RQ4-Optimize): Multi-Call Opportunity_ID Economy",
        "Why Turns-to-Booking is confounded by exogenous drop-offs, and how Turns-to-Lead (TTL), TTQ_s, CSET & Cold/Warm/Hot status work across 4–5 calls",
        notes=(
            "Explain the multi-interaction Opportunity_ID framework across 4-5 calls/chats: why Turns-to-Booking is unrealistic due to exogenous factors, "
            "and how Turns-to-Lead (TTL), Per-Session Turns-to-Quotation (TTQ_s), Cross-Session Excess Turns (CSET), and Cold/Warm/Hot lead carry-over solve it."
        ),
    )
    D.add_card(
        s, 0.35, 1.48, 4.05, 4.78,
        title="1. Why `Turns-to-Booking` Fails in Live\nMulti-Touch Travel Sales (4–5 Calls/Chats)",
        header_bg=CORAL,
        bg_color=RED_BG,
        bullets=[
            "<b>Reality 1 — Multi-Touch Journeys (`Opportunity_ID`):</b>",
            (1, "Consultative travel buyers rarely book in a single chat. A single `Opportunity_ID` typically spans <b>`S = 4 to 5` interactions (chats + calls)</b> over several days as the traveler consults family, compares quotes, and checks dates."),
            "<b>Reality 2 — Unobservable Exogenous Bail-Out Factors:</b>",
            (1, "Even after a perfect quotation, a customer may abandon final payment due to <b>off-chat exogenous shocks</b>:"),
            (2, "• Employer denies vacation / PTO dates;"),
            (2, "• Competitor credit-card portal offers a flash cashback coupon;"),
            (2, "• Staying with relatives and buying flight-only tickets;"),
            (2, "• Visa delay or medical/family emergency."),
            "<b>Methodological Consequence:</b>",
            (1, "Evaluating an AI agent on raw `Turns-to-Booking` confounds conversational policy quality with external market noise!"),
        ],
        font_size=8.7,
    )
    D.add_card(
        s, 4.60, 1.48, 4.10, 4.78,
        title="2. Controllable Milestone Metrics Across\nthe `Opportunity_ID` (`TTL`, `TTQ_s`, `CSET`)",
        header_bg=NAVY,
        bullets=[
            "<b>Replace Noisy Booking With 4 Controllable Milestones:</b>",
            "<b>1. `Turns-to-Lead` (`TTL`, Session 1 — Cold → Warm):</b>",
            (1, "Turns required in Call/Chat 1 to capture the 5 mandatory Tier-1 slots + contact opt-in to register a qualified CRM Lead."),
            "<b>2. Per-Session `Turns-to-Quotation` (`TTQ_s`, Sessions 2..S):</b>",
            (1, "Turns required in Session `s` to narrow `200 → Top 1–2` USP-fit packages and reach verbal quotation agreement (or revised delta-quote)."),
            "<b>3. Cross-Session Redundant Elicitation (`CS-RER = 0.0%`):</b>",
            (1, "Persistent `Opportunity_ID` Slot Ledger pre-loads `L_{s−1}` at Turn 1 of Session `s` so the agent <b>never re-asks slots stated in prior calls</b>!"),
            "<b>4. Cross-Session Excess Turns (`CSET` — Total Economy):</b>",
            (1, "<b>`CSET_i = Σ_{s=1..S_i} (T_{i,s} − T_{i,s}^min)`</b>"),
            (1, "Measures total wasted turns above the information-theoretic floor across all `S_i` sessions (analyzed via Mixed-Effects `LMM` with random intercept `u_i ~ N(0, σ²_opp)`)."),
        ],
        font_size=8.6,
    )
    D.add_card(
        s, 8.90, 1.48, 4.08, 4.78,
        title="3. Cross-Call `Cold / Warm / Hot` Lead\nProgression & Right-Censored Survival",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>Tailoring Responses by Lead Temperature (`L_{i,s}`):</b>",
            (1, "• <b>`COLD` Lead (Call 1):</b> Low commitment, missing slots. <i>Policy:</i> Low-friction USP hook + bundled intake to minimize `TTL` (` Cold → Warm`)."),
            (1, "• <b>`WARM` Lead (Calls 2–3):</b> Slots known, comparing options or spouse constraints. <i>Policy:</i> Pre-load `L_{s−1}`, skip intake (`CS-RER = 0%`), run `200 → 2` USP Info-Gain tree + persona trade-off to minimize `TTQ_s` (`Warm → Hot`)."),
            (1, "• <b>`HOT` Lead (Calls 4–5):</b> Package selected, resolving visa/passport/discount details. <i>Policy:</i> Stage `(e)` `YAML` compliance verification + `2–3` turn delta-quotation closure!"),
            "<b>Handling Exogenous Drop-Offs Statistically:</b>",
            (1, "Model `Cold → Warm → Hot → Quoted` via a <b>Right-Censored Markov / Cox Proportional-Hazards Model</b>—treating off-chat bail-outs after a valid quote as <i>right-censored observations</i> rather than policy failures!"),
        ],
        font_size=8.6,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`Scaling RQ3-Govern & RQ4-Optimize Across Repeat Calls`):</b> "
        "By persisting RQ1-Identify's Bayesian persona posterior, RQ3-Govern's `YAML` compliance state, and RQ4-Optimize's `Verified Slot Ledger` under a unified CRM `Opportunity_ID`, single-chat turn economy (`−35.8%`) scales into multi-touch opportunity economy (`TTL + Σ TTQ_s + CSET`).",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.2,
    )

    # =========================================================================
    # SLIDE 55: DOCTORAL DISSERTATION ROADMAP TABLE (SIX PILLARS MAPPED TO STAGES 1–4)
    # =========================================================================
    s = D.content_slide(
        "10. Doctoral Roadmap Aligned with the 4-Stage Solution Approach",
        "Doctoral Dissertation Roadmap: Six Pillars Mapped to RQ1-Identify to RQ4-Optimize",
        "Scaling Identify → Personalize → Govern → Optimize to C×K regimes, Call Stages (a–f), 200+ packages, and Opportunity_ID journeys",
        notes="Walk through the 6-pillar doctoral roadmap table, showing how every pillar directly extends one of the 4 solution stages.",
    )
    D.add_table(
        s, 0.35, 1.46, 12.63, 4.80,
        headers=[
            "Solution Stage Extended & Doctoral Pillar",
            "Core Doctoral Research Question",
            "Proposed Methodology, Data Stores & Statistical Models",
            "How Validated Capstone Outputs (RQ1–RQ4) Seed This Pillar",
        ],
        rows=[
            [
                "RQ1-IDENTIFY →\nPillar 1: Hierarchical Context × Behavior (`C × K`)",
                "How do situational trip stakes (`party_type, budget_stakes, lead_window`) interact with behavioral archetypes without fragmenting FAISS?",
                "Formulate a <b>Two-Tier Hierarchical Taxonomy (`C × K = 24–36` micro-clusters)</b> using top-20 parent FAISS retrieval + contextual metadata re-ranking & 3-level hierarchical back-off.",
                "Directly extends the Two-Tier Pydantic Schema (`Tier1 + Tier2` slots) and 16-field `UserBehaviour` profile (`party_type`, `price_sensitivity`).",
            ],
            [
                "RQ1-IDENTIFY →\nPillar 2: Soft-Mixture & Bayesian Persona Drift",
                "How can routing blend boundary personas (`25.2%`) and track persona shifts mid-call and across repeat sessions?",
                "Combine <b>Soft-Mixture weights (`w_1..w_K`, proportional multi-index FAISS quota)</b> with <b>Bayesian filtering `P(z_t | u_1..t)`</b> warm-started across sessions of an `Opportunity_ID`.",
                "Reuses the `46-d Blocks` space, boundary speaker diagnostics (`s < .05`), and prefix horizon curve (`m = 3, 5, 7, 9` in `Table 12`).",
            ],
            [
                "RQ2-PERSONALIZE →\nPillar 3: Call Stages (`a–f`) & Multi-Call Lead Policy",
                "How do prompts adapt across 6 call stages (`a–f`) and leverage `Cold/Warm/Hot` lead status across 4–5 touchpoints?",
                "Build a <b>`3 × 6 = 18` `(Persona × Stage a–f)` FAISS Lookup Matrix</b> + <b>Right-Censored Markov Lead Policy (`Cold → Warm → Hot`)</b> governing openings & delta-quotes.",
                "Integrates RQ2/RQ4 persona policies with RQ3-Govern compliance and upgrades RQ1-Identify audit fields (`Fields 14–16`) into persistent CRM lead states.",
            ],
            [
                "RQ2 & RQ4 (NARROW) →\nPillar 4: 200-Package USP Catalog DB & Info-Gain",
                "When mandatory slots match `200+` packages, what question sequence narrows to `1–2` USP-fit packages in minimum turns?",
                "Index a <b>200-Package USP Catalog DB</b> (<i>seniors, children, breakfast, sightseeing tempo, occasion</i>) queried via <b>Maximum Information Gain (`IG_USP`) × Persona Weight</b>.",
                "Scales the RQ4-Optimize `Verified Informed Slot Ledger` and 4-option trade-off framing (`Options A/B/D`) to full tour operator catalogs.",
            ],
            [
                "RQ4-OPTIMIZE →\nPillar 5: Multi-Call `Opportunity_ID` Economy",
                "How can turn economy be optimized across 4–5 calls/chats when final booking suffers exogenous drop-offs?",
                "Optimize controllable <b>`Turns-to-Lead` (`TTL`), `Turns-to-Quotation` (`TTQ_s`), & `Cross-Session Excess Turns` (`CSET = Σ(T_s − T_s^min)`)</b> via Mixed-Effects `LMM` + `5-Arm (A–E)` prompt ablation.",
                "Extends RQ4-Optimize single-session turn economy (`−29.5%..−42.7%`, `.000` RER) to cross-session `CS-RER = 0%` and isolates RQ2-Personalize directive vs. exemplar gains.",
            ],
            [
                "RQ3 & RQ4 (GOVERN/OPT) →\nPillar 6: `Turn-Q DB` Composite Scorer & RLHC",
                "How can retrieval jointly optimize stylistic phrasing (`cos`) and remaining turns to quotation (`DTQ`) under hard safety rules?",
                "Pair FAISS with a <b>Historical Turn-Economy DB (`Turn-Q DB`)</b> via `Score = α·cos + β·Q* − γ·DTQ + δ·IG_USP` and train <b>Constrained Offline RL (`CMDP / RLHC`)</b>.",
                "Uses RQ2-Personalize FAISS cosine (`.597`) for phrasing, RQ3-Govern `RuleEngine` (`0.0%` leak, `98.6%` sens.) as safety shield, and RQ4-Optimize simulator for warm-start.",
            ],
        ],
        col_widths=[2.35, 2.55, 4.30, 3.43],
        font_size=7.8,
        align_left_cols=(0, 1, 2, 3),
        highlight_rows=(0, 1, 2, 3, 4, 5),
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Continuity from Master's Capstone to Doctoral Dissertation:</b> "
        "Notice in Column 1 that Pillars 1–6 do not introduce a disconnected topic—they systematically firm up <b>RQ1-Identify (`P1–P2`)</b>, <b>RQ2-Personalize (`P3–P4`)</b>, <b>RQ3-Govern (`P3e & P6 shield`)</b>, and <b>RQ4-Optimize (`P4–P6`)</b> for live multi-call enterprise deployment.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.3,
    )

    # =========================================================================
    # SLIDE 56: PICTORIAL CAPSTONE-TO-DOCTORAL ARCHITECTURE MAPPED TO STAGES 1–4
    # =========================================================================
    s = D.content_slide(
        "10. Doctoral Roadmap Aligned with the 4-Stage Solution Approach",
        "Pictorial Roadmap: Capstone (Teal) vs. Doctoral Extensions (Coral/Amber)",
        "Mapping every completed Capstone module (RQ1–RQ4) and Doctoral extension (P1–P6) directly under the 4-Stage Solution Approach columns",
        notes=(
            "This pictorial blueprint aligns every Teal (Completed Capstone) and Coral/Amber (Doctoral Extension) block "
            "directly beneath the 4-stage solution approach headers: RQ1-Identify Stage, RQ2-Personalize Stage, RQ3-Govern & RQ4-Optimize (Govern & Optimize), and the Target Enterprise System Hub."
        ),
    )

    CAP_BG = RGBColor(224, 242, 241)       # Soft Teal tint for Built in Capstone (RQ1-RQ4)
    CAP_HDR = TEAL                         # Deep Teal header
    CAP_BORDER = NAVY                      # Solid Navy border

    DOC_BG = RGBColor(255, 244, 224)       # Warm Amber tint for Doctoral Extensions (P1-P6)
    DOC_HDR = CORAL                        # Red/Coral header for Doctoral blocks
    DOC_BORDER = GOLD                      # Gold border

    GOAL_BG = RGBColor(225, 245, 232)      # Soft Emerald tint for Target System Hub
    GOAL_HDR = GREEN                       # Deep Emerald header
    GOAL_BORDER = GREEN

    def _add_legend_pill(left, width, bg_col, hdr_col, bdr_col, tag_txt, desc_txt):
        box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(1.42), Inches(width), Inches(0.28))
        box.adjustments[0] = 0.15
        box.fill.solid()
        box.fill.fore_color.rgb = bg_col
        box.line.color.rgb = bdr_col
        box.line.width = Pt(1.2)
        badge = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left + 0.04), Inches(1.45), Inches(1.62), Inches(0.22))
        badge.adjustments[0] = 0.2
        badge.fill.solid()
        badge.fill.fore_color.rgb = hdr_col
        badge.line.fill.background()
        p_b = badge.text_frame.paragraphs[0]
        p_b.alignment = PP_ALIGN.CENTER
        _add_formatted_runs(p_b, tag_txt, font_size=7.2, color=WHITE, bold=True)
        tb = s.shapes.add_textbox(Inches(left + 1.70), Inches(1.44), Inches(width - 1.74), Inches(0.24))
        tb.text_frame.word_wrap = True
        tb.text_frame.margin_left = tb.text_frame.margin_top = Inches(0)
        p_t = tb.text_frame.paragraphs[0]
        _add_formatted_runs(p_t, desc_txt, font_size=7.5, color=DARK, bold=True)

    _add_legend_pill(
        0.25, 4.15, CAP_BG, CAP_HDR, CAP_BORDER,
        "BUILT IN CAPSTONE (RQ1–RQ4)",
        "Validated 4-Stage Solution Approach Core (p < .001)",
    )
    _add_legend_pill(
        4.48, 4.55, DOC_BG, DOC_HDR, DOC_BORDER,
        "DOCTORAL EXTENSIONS (P1–P6)",
        "Red/Amber Blocks Aligned with Solution Approach RQ1-Identify to RQ4-Optimize",
    )
    _add_legend_pill(
        9.11, 3.97, GOAL_BG, GOAL_HDR, GOAL_BORDER,
        "TARGET ENTERPRISE SYSTEM",
        "Multi-Call Consultative Travel AI",
    )

    # 4-Stage Solution Approach Column Banner Headers (y = 1.74, h = 0.26)
    col_banners = [
        (0.25, 2.65, NAVY, "RQ1-IDENTIFY (RQ1 + P1–P2)"),
        (3.70, 2.85, TEAL, "RQ2-PERSONALIZE (RQ2 + P3–P4)"),
        (7.35, 2.73, CORAL, "RQ3-GOVERN & RQ4-OPTIMIZES (RQ3–4 + P5–6)"),
        (10.80, 2.28, GREEN, "INTEGRATED 4-STAGE GOAL"),
    ]
    for bx, bw, bcol, btxt in col_banners:
        cb = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(bx), Inches(1.74), Inches(bw), Inches(0.24))
        cb.fill.solid()
        cb.fill.fore_color.rgb = bcol
        cb.line.fill.background()
        p_cb = cb.text_frame.paragraphs[0]
        p_cb.alignment = PP_ALIGN.CENTER
        _add_formatted_runs(p_cb, btxt, font_size=7.4, color=WHITE, bold=True)

    def _add_analysis_block(left, top, width, height, title, lines, is_capstone=True):
        bg = CAP_BG if is_capstone else DOC_BG
        hdr_c = CAP_HDR if is_capstone else DOC_HDR
        bdr_c = CAP_BORDER if is_capstone else DOC_BORDER

        card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.adjustments[0] = 0.03
        card.fill.solid()
        card.fill.fore_color.rgb = bg
        card.line.color.rgb = bdr_c
        card.line.width = Pt(1.35)

        hdr_h = 0.25
        hdr = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(hdr_h))
        hdr.adjustments[0] = 0.03
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = hdr_c
        hdr.line.fill.background()
        tf_h = hdr.text_frame
        tf_h.word_wrap = True
        tf_h.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf_h.margin_left = Inches(0.06)
        p_h = tf_h.paragraphs[0]
        _add_formatted_runs(p_h, title, font_size=7.9, color=WHITE, bold=True)

        tb = s.shapes.add_textbox(
            Inches(left + 0.05),
            Inches(top + hdr_h + 0.02),
            Inches(width - 0.10),
            Inches(height - hdr_h - 0.03),
        )
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.02)
        tf.margin_top = tf.margin_bottom = Inches(0.01)
        for idx, ln in enumerate(lines):
            p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
            p.space_after = Pt(1.0)
            _add_formatted_runs(p, ln, font_size=6.8, color=DARK)

    def _add_labeled_arrow(left, top, width, height, label_top, label_bottom, is_capstone=True):
        arr_c = CAP_HDR if is_capstone else DOC_HDR
        bdr_c = NAVY if is_capstone else GOLD
        arr = s.shapes.add_shape(
            MSO_SHAPE.RIGHT_ARROW,
            Inches(left + 0.03),
            Inches(top + height * 0.34),
            Inches(width - 0.06),
            Inches(0.22),
        )
        arr.fill.solid()
        arr.fill.fore_color.rgb = arr_c
        arr.line.color.rgb = bdr_c
        arr.line.width = Pt(0.75)

        tb1 = s.shapes.add_textbox(Inches(left - 0.02), Inches(top + 0.02), Inches(width + 0.04), Inches(0.30))
        tf1 = tb1.text_frame
        tf1.word_wrap = True
        tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = Inches(0)
        p1 = tf1.paragraphs[0]
        p1.alignment = PP_ALIGN.CENTER
        _add_formatted_runs(p1, label_top, font_size=6.6, color=NAVY if is_capstone else DOC_HDR, bold=True)

        tb2 = s.shapes.add_textbox(Inches(left - 0.02), Inches(top + height * 0.34 + 0.23), Inches(width + 0.04), Inches(0.42))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        tf2.margin_left = tf2.margin_right = tf2.margin_top = tf2.margin_bottom = Inches(0)
        p2 = tf2.paragraphs[0]
        p2.alignment = PP_ALIGN.CENTER
        _add_formatted_runs(p2, label_bottom, font_size=6.3, color=DARK)

    def _add_vert_connector(center_x, top_y, label_txt):
        arr = s.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(center_x - 0.10), Inches(top_y), Inches(0.20), Inches(0.13))
        arr.fill.solid()
        arr.fill.fore_color.rgb = GOLD
        arr.line.color.rgb = DOC_HDR
        arr.line.width = Pt(0.6)
        tb = s.shapes.add_textbox(Inches(center_x + 0.12), Inches(top_y - 0.02), Inches(1.65), Inches(0.15))
        tf = tb.text_frame
        tf.margin_left = tf.margin_top = Inches(0)
        p = tf.paragraphs[0]
        _add_formatted_runs(p, label_txt, font_size=6.3, color=DOC_HDR, bold=True)

    R1_Y, R2_Y, R3_Y = 2.02, 3.50, 4.98
    ROW_H = 1.34

    # COLUMN 1: RQ1-IDENTIFY — IDENTIFY (RQ1 + PILLARS 1 & 2)
    C1_X, C1_W = 0.25, 2.65
    _add_analysis_block(
        C1_X, R1_Y, C1_W, ROW_H,
        "[BUILT: RQ1-IDENTIFY] Identify 3 Personas",
        [
            "• <b>Method:</b> `M=9` prefix `K-Means (k=3)` + `L1 Router` on `46-d Blocks`.",
            "• <b>Features:</b> `PCA-20` Gemini + `13` LLM scales (`η²=.32–.52`).",
            "• <b>Result:</b> `ARI=.89/.87`, Test `κ=.535 (M=5)` & `.958 (M=9)`.",
        ],
        is_capstone=True,
    )
    _add_vert_connector(C1_X + 0.85, R1_Y + ROW_H, "Solution RQ1-Identify → Context × Behavior")

    _add_analysis_block(
        C1_X, R2_Y, C1_W, ROW_H,
        "[DOCTORAL P1: RQ1-IDENTIFY] Hierarchical (C × K)",
        [
            "• <b>Solution Role:</b> Adds situational trip context to RQ1-Identify `Identify`.",
            "• <b>New Params:</b> `party_type`, `budget_stakes`, `lead_window` × `K=3` (`24–36` cells + hierarchical FAISS back-off).",
        ],
        is_capstone=False,
    )
    _add_vert_connector(C1_X + 0.85, R2_Y + ROW_H, "Solution RQ1-Identify → Soft Drift")

    _add_analysis_block(
        C1_X, R3_Y, C1_W, ROW_H,
        "[DOCTORAL P2: RQ1-IDENTIFY] Soft-Mixture & Drift",
        [
            "• <b>Solution Role:</b> Upgrades hard `k=3` lock-in for `25.2%` boundary users.",
            "• <b>New Method:</b> Softmax weights `w_1..w_K` + turn-by-turn & cross-call Bayesian posterior `P(z_t | u_1..t)`.",
        ],
        is_capstone=False,
    )

    # ARROWS 1 -> 2
    A1_X, A1_W = 2.91, 0.77
    _add_labeled_arrow(A1_X, R1_Y + 0.12, A1_W, ROW_H - 0.2, "RQ1 → RQ2", "3 Personas + Router + 3 FAISS DBs", is_capstone=True)
    _add_labeled_arrow(A1_X, R2_Y + 0.12, A1_W, ROW_H - 0.2, "P1 → RQ2-Personalize", "C×K Regime + Back-Off Key", is_capstone=False)
    _add_labeled_arrow(A1_X, R3_Y + 0.12, A1_W, ROW_H - 0.2, "P2 → RQ2-Personalize", "Live Posterior P(z_t | u_1..t)", is_capstone=False)

    # COLUMN 2: RQ2-PERSONALIZE — PERSONALIZE (RQ2 + PILLARS 3 & 4)
    C2_X, C2_W = 3.70, 2.85
    _add_analysis_block(
        C2_X, R1_Y, C2_W, ROW_H,
        "[BUILT: RQ2-PERSONALIZE] Personalize Style & Pacing",
        [
            "• <b>Method:</b> Partitioned FAISS (`k=3`) + `[SLOT]` Mask + Pacing Directive.",
            "• <b>Norms:</b> `12.9w` (DB) / `18.6w` (OE) / `14.8w` (RCS).",
            "• <b>Result:</b> Style `.597 (+31.8%, p<.001)` & `3.87w` error (`p=.007`).",
        ],
        is_capstone=True,
    )
    _add_vert_connector(C2_X + 0.90, R1_Y + ROW_H, "Solution RQ2-Personalize → 6 Call Stages")

    _add_analysis_block(
        C2_X, R2_Y, C2_W, ROW_H,
        "[DOCTORAL P3: RQ2-PERSONALIZE] Stages (a–f) & Lead Temp",
        [
            "• <b>Solution Role:</b> Sub-indexes RQ2-Personalize FAISS across `3 × 6 = 18` `(Persona × Stage a–f)` cells.",
            "• <b>Cross-Call Policy:</b> Carries `Cold / Warm / Hot` lead status across 4–5 calls per `Opportunity_ID`.",
        ],
        is_capstone=False,
    )
    _add_vert_connector(C2_X + 0.90, R2_Y + ROW_H, "Solution RQ2-Personalize → 200-Pkg USP Tree")

    _add_analysis_block(
        C2_X, R3_Y, C2_W, ROW_H,
        "[DOCTORAL P4: RQ2/RQ4] 200-Pkg USP Tree",
        [
            "• <b>Solution Role:</b> Scales 4 options to `200+` regional packages.",
            "• <b>Narrowing (`IG_USP`):</b> Max Info-Gain tree over `seniors, children, breakfast, tempo, occasion` → `Top 1–2` USPs.",
        ],
        is_capstone=False,
    )

    # ARROWS 2 -> 3
    A2_X, A2_W = 6.57, 0.76
    _add_labeled_arrow(A2_X, R1_Y + 0.12, A2_W, ROW_H - 0.2, "RQ2 → RQ3", "Style (.597) + [SLOT] Mask", is_capstone=True)
    _add_labeled_arrow(A2_X, R2_Y + 0.12, A2_W, ROW_H - 0.2, "P3 → RQ3-Govern/4", "Stage (a–f) + Cold/Warm/Hot", is_capstone=False)
    _add_labeled_arrow(A2_X, R3_Y + 0.12, A2_W, ROW_H - 0.2, "P4 → RQ4-Optimize", "Top 1–2 USP Package Match", is_capstone=False)

    # COLUMN 3: STAGES 3 & 4 — GOVERN & OPTIMIZE (RQ3, RQ4 + PILLARS 5 & 6)
    C3_X, C3_W = 7.35, 2.73
    _add_analysis_block(
        C3_X, R1_Y, C3_W, ROW_H,
        "[BUILT: RQ3-GOVERN] Govern Policy & Leakage",
        [
            "• <b>Method:</b> Declarative `YAML` Rule Engine + Entity Sanitizer.",
            "• <b>Rules:</b> `visa ≥ 15d, passport ≥ 6m, FIT ≤ 4, disc ≤ 15%, ≥ $500`.",
            "• <b>Result:</b> `0.0%` leak (`F=34.82`), `98.6%` sens. (`F=498.78, κ=.917`).",
        ],
        is_capstone=True,
    )
    _add_vert_connector(C3_X + 0.85, R1_Y + ROW_H, "RQ3-Govern Guard Feeds RQ4-Optimize Ledger")

    _add_analysis_block(
        C3_X, R2_Y, C3_W, ROW_H,
        "[BUILT: RQ4-OPTIMIZE] Optimize Turn Economy",
        [
            "• <b>Method:</b> Verified Informed Slot Ledger + Persona Package Policies.",
            "• <b>Result:</b> `−29.5%..−42.7%` turns (`F=664.43, Int. F=10.89`), `RER .109 → .000` (`κ=.933`).",
        ],
        is_capstone=True,
    )
    _add_vert_connector(C3_X + 0.85, R2_Y + ROW_H, "Solution RQ4-Optimize → Opp_ID & Turn-Q DB")

    _add_analysis_block(
        C3_X, R3_Y, C3_W, ROW_H,
        "[DOCTORAL P5–6: RQ4-OPTIMIZE] Opp_ID & Turn-Q DB",
        [
            "• <b>Solution Role:</b> Extends RQ4-Optimize economy across 4–5 calls (`Opportunity_ID`): `TTL`, `TTQ_s`, & `CSET`.",
            "• <b>Optimization:</b> Historical <b>`Turn-Q DB` (`DTQ`)</b> + `5-Arm (A–E)` ablation + Constrained RL (`CMDP`).",
        ],
        is_capstone=False,
    )

    # ARROWS 3 -> 4
    A3_X, A3_W = 10.10, 0.68
    _add_labeled_arrow(A3_X, R1_Y + 0.12, A3_W, ROW_H - 0.2, "RQ3-Govern Out", "0.0% Leak & 98.6% Guard", is_capstone=True)
    _add_labeled_arrow(A3_X, R2_Y + 0.12, A3_W, ROW_H - 0.2, "RQ4-Optimize Out", "−30..43% Turns & .000 RER", is_capstone=True)
    _add_labeled_arrow(A3_X, R3_Y + 0.12, A3_W, ROW_H - 0.2, "P5–6 Out", "Min TTL/TTQ/CSET + Lead", is_capstone=False)

    # COLUMN 4: TARGET ENTERPRISE SYSTEM HUB
    G_X, G_Y, G_W, G_H = 10.80, 2.02, 2.28, 4.30
    goal_card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(G_X), Inches(G_Y), Inches(G_W), Inches(G_H))
    goal_card.adjustments[0] = 0.03
    goal_card.fill.solid()
    goal_card.fill.fore_color.rgb = GOAL_BG
    goal_card.line.color.rgb = GOAL_BORDER
    goal_card.line.width = Pt(2.0)

    goal_hdr = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(G_X), Inches(G_Y), Inches(G_W), Inches(0.46))
    goal_hdr.adjustments[0] = 0.03
    goal_hdr.fill.solid()
    goal_hdr.fill.fore_color.rgb = GOAL_HDR
    goal_hdr.line.fill.background()
    tf_gh = goal_hdr.text_frame
    tf_gh.word_wrap = True
    tf_gh.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_gh = tf_gh.paragraphs[0]
    p_gh.alignment = PP_ALIGN.CENTER
    _add_formatted_runs(p_gh, "FIRMED-UP 4-STAGE\nENTERPRISE AI", font_size=8.6, color=WHITE, bold=True)

    goal_items = [
        ("1. Identify (RQ1 + P1–P2)", "`C × K` regimes + soft Bayesian drift."),
        ("2. Personalize (RQ2 + P3)", "Style across stages `a → f` & `Cold/Warm/Hot`."),
        ("3. Narrow (P4 USP Tree)", "`200 → 1–2` packages via `IG_USP` tree."),
        ("4. Govern (RQ3 Guard)", "`0.0%` entity leak & `98.6%` rule compliance."),
        ("5. Optimize (RQ4 + P5–P6)", "Min `TTL, TTQ_s, CSET` via `Turn-Q DB`."),
    ]
    cur_gy = G_Y + 0.52
    for g_title, g_desc in goal_items:
        sub = s.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(G_X + 0.07), Inches(cur_gy), Inches(G_W - 0.14), Inches(0.70)
        )
        sub.adjustments[0] = 0.06
        sub.fill.solid()
        sub.fill.fore_color.rgb = WHITE
        sub.line.color.rgb = GOAL_BORDER
        sub.line.width = Pt(1.0)
        tf_s = sub.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_right = Inches(0.05)
        tf_s.margin_top = tf_s.margin_bottom = Inches(0.02)
        p_st = tf_s.paragraphs[0]
        _add_formatted_runs(p_st, g_title, font_size=7.4, color=GOAL_HDR, bold=True)
        p_sd = tf_s.add_paragraph()
        p_sd.space_before = Pt(1.0)
        _add_formatted_runs(p_sd, g_desc, font_size=6.7, color=DARK)
        cur_gy += 0.74

    D.add_callout(
        s, 0.25, 6.40, 12.83, 0.72,
        "<b>Solution Approach Alignment (`How Red/Amber Doctoral Blocks Firm Up the Teal Capstone Core`):</b> "
        "Every Coral/Amber doctoral block sits directly inside its parent solution stage column—extending <b>RQ1-Identify (`P1–P2`)</b>, <b>RQ2-Personalize (`P3–P4`)</b>, and <b>RQ3-Govern & RQ4-Optimize (`P5–P6`)</b> without altering the validated neuro-symbolic core.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.0,
    )

    # =========================================================================
    # SLIDE 57: DOCTORAL DATA FLOW DIAGRAM — COSINE + TURN-Q DB + 200-PKG USP DB
    # =========================================================================
    s = D.content_slide(
        "10. Doctoral Roadmap Aligned with the 4-Stage Solution Approach",
        "Doctoral Deep-Dive: Opportunity_ID Turn Economy & Cosine + Turn-Q DFD",
        "Upgrading backward-looking Cosine Retrieval (RQ2-Personalize) with a Turn-Economy DB (Turn-Q DB), 200-Pkg USP Index & Cross-Call Lead State",
        notes=(
            "Presents the firmed-up enterprise data-flow architecture, "
            "aligning the 3 parallel data stores and 4 runtime steps directly to Identify -> Personalize -> Govern -> Optimize."
        ),
    )

    _add_legend_pill(
        0.25, 4.15, CAP_BG, CAP_HDR, CAP_BORDER,
        "BUILT IN CAPSTONE (RQ1–RQ4)",
        "Router, FAISS Style DB, YAML Rules & Slot Ledger",
    )
    _add_legend_pill(
        4.48, 4.55, DOC_BG, DOC_HDR, DOC_BORDER,
        "NEW DOCTORAL STORES & SCORER",
        "Opp_ID Ledger, Turn-Q DB (DTQ), USP DB & Composite Scorer",
    )
    _add_legend_pill(
        9.11, 3.97, GOAL_BG, GOAL_HDR, GOAL_BORDER,
        "MULTI-CALL CRM OUTPUT",
        "Min TTL / TTQ_s / CSET + Cold→Warm→Hot Progression",
    )

    # LEFT TOP: 5-Row Structural State-Space & Opportunity_ID Mapping Table
    D.add_table(
        s, 0.25, 1.76, 5.30, 3.12,
        headers=["Solution Approach & CRM Pillar", "Multi-Call Consultative Formulation", "Metrics & Solution Approach Alignment"],
        rows=[
            [
                "1. Controllable Goal\n(RQ4-Optimize Scope)",
                "Users take <b>4–5 calls/chats</b> & drop off for exogenous reasons (PTO, visa). Target controllable per-call milestones.",
                "<b>Call 1:</b> `Turns-to-Lead (TTL)`\n<b>Calls 2–5:</b> `TTQ_s` (Quote)",
            ],
            [
                "2. Persistent State\n(`RQ1-Identify + RQ4-Optimize`)",
                "Tuple `S_{i,s,t} = (Opp_ID, C×K Post., Cold/Warm/Hot, Stage a–f, Ledger L_{s−1}, |P_t|, Conflict)`.",
                "Pre-loads prior slots → <b>Cross-Call `CS-RER = 0.0%`</b>",
            ],
            [
                "3. Lead-Temp Policy\n(`RQ2-Personalize Personalize`)",
                "<b>Cold:</b> USP hook (`TTL`). <b>Warm:</b> `200→2` narrowing (`TTQ_s`). <b>Hot:</b> Compliance + delta-quote (`2–3t`).",
                "Right-censored Markov `Cold → Warm → Hot`",
            ],
            [
                "4. Action Guardrail\n(`RQ3-Govern Govern`)",
                "`RQ3-Govern YAML` Rule Engine + `RQ4-Optimize` Slot Ledger prune policy-violating or repeat actions pre-generation.",
                "`0.0%` leak, `98.6%` rule guard, `.000` repeat asks",
            ],
            [
                "5. Lookahead Score\n(`RQ4-Optimize Optimize`)",
                "Combines in-call remaining turns `DTQ(S_t, A_j)` with excess turns above info floor across `S` calls.",
                "<b>`CSET = Σ_s(T_s − T_s^min)`</b>\n(Mixed `LMM` by `Opp_ID`)",
            ],
        ],
        col_widths=[1.25, 2.45, 1.60],
        font_size=6.7,
        header_size=7.4,
        align_left_cols=(0, 1, 2),
        highlight_rows=(0, 4),
    )

    # LEFT BOTTOM: Composite Formula Card
    D.add_card(
        s, 0.25, 4.96, 5.30, 1.36,
        title="Why RQ2-Personalize Cosine Alone Needs Turn-Q & USP DBs (Composite Scorer)",
        header_bg=DOC_HDR,
        bg_color=DOC_BG,
        border_color=DOC_BORDER,
        bullets=[
            "<b>Backward Cosine vs. Forward Economy:</b> `cos(q_t, e_j)` captures <i>phrasing</i> (`.597` style, `3.87w`), but treats a reply needing <b>9 more turns</b> the same as one quoting in <b>1 turn</b>.",
            "<b>Composite Action Score (`Stores 1–3`):</b>  <b>`Score = α·cos(q_t, e_j) + β·Q*(S_t, A_j) − γ·DTQ(S_t, A_j) + δ·IG_USP(A_j)`</b>",
        ],
        font_size=7.2,
        title_size=8.2,
        bullet_spacing=2,
    )

    # RIGHT PANEL: End-to-End Block & Data Flow Diagram (DFD)
    dfd_bg = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.65), Inches(1.76), Inches(7.43), Inches(4.56))
    dfd_bg.adjustments[0] = 0.02
    dfd_bg.fill.solid()
    dfd_bg.fill.fore_color.rgb = RGBColor(244, 247, 251)
    dfd_bg.line.color.rgb = NAVY
    dfd_bg.line.width = Pt(1.5)

    dfd_hdr = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.65), Inches(1.76), Inches(7.43), Inches(0.28))
    dfd_hdr.adjustments[0] = 0.02
    dfd_hdr.fill.solid()
    dfd_hdr.fill.fore_color.rgb = NAVY
    dfd_hdr.line.fill.background()
    p_dh = dfd_hdr.text_frame.paragraphs[0]
    p_dh.alignment = PP_ALIGN.CENTER
    _add_formatted_runs(
        p_dh,
        "4-STAGE RUNTIME DATA FLOW DIAGRAM: COSINE FAISS DB + TURN-ECONOMY (TURN-Q) & 200-PKG USP DBs",
        font_size=7.8,
        color=WHITE,
        bold=True,
    )

    def _draw_dfd_node(left, top, width, height, badge, title, bullets, bg_c, hdr_c, bdr_c):
        box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        box.adjustments[0] = 0.04
        box.fill.solid()
        box.fill.fore_color.rgb = bg_c
        box.line.color.rgb = bdr_c
        box.line.width = Pt(1.3)

        bh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(0.24))
        bh.adjustments[0] = 0.04
        bh.fill.solid()
        bh.fill.fore_color.rgb = hdr_c
        bh.line.fill.background()
        p_b = bh.text_frame.paragraphs[0]
        p_b.alignment = PP_ALIGN.CENTER
        _add_formatted_runs(p_b, f"{badge} {title}", font_size=6.9, color=WHITE, bold=True)

        tb = s.shapes.add_textbox(Inches(left + 0.05), Inches(top + 0.25), Inches(width - 0.10), Inches(height - 0.27))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0.01)
        for idx_b, b_txt in enumerate(bullets):
            p = tf.paragraphs[0] if idx_b == 0 else tf.add_paragraph()
            p.space_after = Pt(1.0)
            _add_formatted_runs(p, b_txt, font_size=6.6, color=DARK)

    # TOP ROW OF DFD: THREE PARALLEL DATA STORES (y = 2.10, h = 1.36)
    _draw_dfd_node(
        5.76, 2.10, 2.32, 1.36,
        "[STORE 1: RQ2-PERSONALIZE]",
        "FAISS Style Vector DB",
        [
            "• <b>Indexed By:</b> `k=3` → `(C × K × Stage a–f)` + metadata back-off.",
            "• <b>Signal:</b> Cosine `cos(q_t, e_j)`.",
            "• <b>Role:</b> `[SLOT]`-masked phrasing (`HOW` to speak).",
        ],
        CAP_BG, CAP_HDR, CAP_BORDER,
    )

    _draw_dfd_node(
        8.20, 2.10, 2.33, 1.36,
        "[STORE 2: RQ4-OPTIMIZE EXT]",
        "Turn-Economy DB (Turn-Q)",
        [
            "• <b>Indexed By:</b> `S_{i,s,t}` (`Cluster, LeadTemp, Stage, Slots, Conflict`).",
            "• <b>Metrics:</b> Remaining turns `DTQ`, quote rate `Q*`, & `CSET`.",
            "• <b>Role:</b> Min-turn action!",
        ],
        DOC_BG, DOC_HDR, DOC_BORDER,
    )

    _draw_dfd_node(
        10.65, 2.10, 2.32, 1.36,
        "[STORE 3: RQ2/RQ4 EXT]",
        "200-Pkg USP Catalog DB",
        [
            "• <b>Indexed By:</b> `Senior, Child, Breakfast, Tempo, Occasion`.",
            "• <b>Signal:</b> Info-Gain `IG_USP` (`Δ|P_t|` narrowed).",
            "• <b>Role:</b> Top 1–2 USP matches.",
        ],
        DOC_BG, DOC_HDR, DOC_BORDER,
    )

    # Downward Data Flow Arrows from the 3 Data Stores (y = 3.49)
    for store_cx, lbl in [
        (6.92, "cos(q_t, e_j)\nStyle Templates"),
        (9.36, "DTQ & Q*(S_t, A_j)\nTurn Economy"),
        (11.81, "IG_USP & USPs\nCatalog Fit"),
    ]:
        da = s.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(store_cx - 0.10), Inches(3.49), Inches(0.20), Inches(0.24))
        da.fill.solid()
        da.fill.fore_color.rgb = TEAL if store_cx < 7.6 else DOC_HDR
        da.line.color.rgb = NAVY if store_cx < 7.6 else GOLD
        da.line.width = Pt(0.75)
        tb_l = s.shapes.add_textbox(Inches(store_cx + 0.11), Inches(3.47), Inches(1.12), Inches(0.28))
        tf_l = tb_l.text_frame
        tf_l.word_wrap = True
        tf_l.margin_left = tf_l.margin_top = Inches(0)
        _add_formatted_runs(tf_l.paragraphs[0], lbl, font_size=6.2, color=DARK, bold=True)

    # BOTTOM ROW OF DFD: 4-STAGE RUNTIME FLOW (y = 3.78, h = 2.44)
    _draw_dfd_node(
        5.76, 3.78, 1.66, 2.44,
        "[RQ1-IDENTIFY]",
        "Identify & Opp_ID",
        [
            "• <b>Load `Opp_ID` (Call 2/4):</b>\n  Prior `Ledger L_1` (`CS-RER=0`) + `WARM` Lead.",
            "• <b>Route (`RQ1+P1–3`):</b>\n  `(Family, Rigid)` + `Stage d` + `|P_t|=38 pkgs`.",
        ],
        CAP_BG, CAP_HDR, CAP_BORDER,
    )

    a_12 = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(7.44), Inches(4.88), Inches(0.18), Inches(0.20))
    a_12.fill.solid()
    a_12.fill.fore_color.rgb = NAVY
    a_12.line.fill.background()

    _draw_dfd_node(
        7.64, 3.78, 2.08, 2.44,
        "[RQ2+RQ4]",
        "Personalize & Score",
        [
            "• <b>Ranks Candidate Actions:</b>",
            "  ▪ `A1 (Ask Tempo)`: `cos=.81`, `38→31`, <b>`DTQ=5.4t` (Slow ✗)</b>",
            "  ▪ `A2 (Ask Senior)`: `cos=.82`, `38→14`, <b>`DTQ=3.1t`</b>",
            "  ▪ <b>`A3* (Bundle Senior+Bkfst + 4★ vs 5★+3d USP)`:</b> `cos=.84`, `38→2`, `Q*=.94`, <b>`DTQ=1.0t` (Best ✓)</b>",
        ],
        DOC_BG, DOC_HDR, DOC_BORDER,
    )

    a_23 = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(9.74), Inches(4.88), Inches(0.18), Inches(0.20))
    a_23.fill.solid()
    a_23.fill.fore_color.rgb = DOC_HDR
    a_23.line.fill.background()

    _draw_dfd_node(
        9.94, 3.78, 1.52, 2.44,
        "[RQ3-GOVERN]",
        "Govern & Phrase",
        [
            "• <b>WHAT Action:</b>\n  Execute `A3*` (`DTQ=1.0t`).",
            "• <b>HOW (`RQ2`):</b>\n  Top-3 `[SLOT]` exemplars (`14.8w`).",
            "• <b>Guard (`RQ3/4`):</b>\n  `0%` leak, `5 YAML` rules, `0%` RER.",
        ],
        CAP_BG, CAP_HDR, CAP_BORDER,
    )

    a_34 = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(11.48), Inches(4.88), Inches(0.18), Inches(0.20))
    a_34.fill.solid()
    a_34.fill.fore_color.rgb = GREEN
    a_34.line.fill.background()

    _draw_dfd_node(
        11.68, 3.78, 1.29, 2.44,
        "[RQ4-OPTIMIZE]",
        "Optimize & Persist",
        [
            "• <b>Milestone:</b>\n  `TTL` (Call 1) or `TTQ_s` Quote (`Top 2` pkgs).",
            "• <b>Save `Opp_ID`:</b>\n  Log `CSET` & upgrade `WARM → HOT` Lead.",
        ],
        GOAL_BG, GOAL_HDR, GOAL_BORDER,
    )

    D.add_callout(
        s, 0.25, 6.38, 12.83, 0.74,
        "<b>Solution Approach Alignment (`Complete Runtime Synthesis`):</b> "
        "Notice how the bottom DFD row executes the exact 4-stage solution approach on every turn: <b>`RQ1-Identify`</b> loads `Opp_ID` & routes `(C × K × Stage)` → <b>`RQ2-Personalize+4`</b> scores style `cos` + forward `DTQ` + `IG_USP` → <b>`RQ3-Govern`</b> enforces `0%` leakage & `YAML` rules → <b>`RQ4-Optimize`</b> delivers the minimum-turn quote and persists `Cold/Warm/Hot` lead state!",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.0,
    )

    # =========================================================================
    # SLIDE 58: DEFENSE Q&A #1 — SAMPLE SIZE ASSUMPTIONS & POST-HOC AUDIT
    # =========================================================================
    s = D.content_slide(
        "11. Anticipated Defense Committee Q&A Bank",
        "Defense Q&A #1: 'What Assumptions Were Taken to Arrive at Sample Sizes?'",
        "Five explicit a priori power assumptions (`step0_sample_size.py`) and post-hoc verification across all 4 solution stages",
        notes="Use this slide when asked Question #1: What are the assumptions taken to arrive at proper sample sizes?",
    )
    D.add_card(
        s, 0.35, 1.48, 6.15, 4.78,
        title="Five Explicit A Priori Assumptions (`step0_sample_size.py`)",
        header_bg=NAVY,
        bullets=[
            "<b>Assumption 1 — Type I Error Control (`α = .05`, two-tailed / omnibus F):</b>",
            (1, "A 5% false-positive ceiling was set across all primary omnibus tests, paired with Tukey HSD (`RQ1-Identify`) and Holm–Bonferroni (`RQ2-Personalize`) familywise error control."),
            "<b>Assumption 2 — Target Statistical Power (`1 − β ≥ .80, β ≤ .20`):</b>",
            (1, "Following Cohen (1988), false-negative risk was capped at `≤ 20%`, requiring noncentrality `λ = 8.00` (`df_1 = 1`) to `λ = 9.88` (`df_1 = 2`)."),
            "<b>Assumption 3 — Medium Minimum Detectable Effect Size (`f = .25`):</b>",
            (1, "Every experiment was powered to detect at least a medium effect (`f = .25`, `η² ≈ .059` or `~6%` variance) so statistical significance aligns with practical business value."),
            "<b>Assumption 4 — Within-Dialogue Correlation (`ρ = .50`) in RQ2-Personalize:</b>",
            (1, "Moderate within-dialogue correlation `ρ = .50` was specified across the `m = 3` prompt conditions."),
            "<b>Assumption 5 — `+10% to +18%` Cell-Balancing Buffer:</b>",
            (1, "`N_min = 158, 28, 128, 158` were buffered to exact cell multiples: <b>`159 (53×3)`, `33 (11×3)`, `144 (36×4)`, and `180 (30×6)`</b> (`a priori power = .804 to .865`)."),
        ],
        font_size=9.1,
    )
    D.add_card(
        s, 6.80, 1.48, 6.18, 4.78,
        title="Post-Hoc Empirical Audit: Did the Data Satisfy Every Assumption?",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>1. Observed Effect Sizes Far Exceeded `f = .25` (`η² = .059`):</b>",
            (1, "• <b>RQ1-Identify Stage:</b> Algorithm `η² = .497 to .620` (`Matched RM ηp² = .615`)."),
            (1, "• <b>RQ2-Personalize Stage:</b> Style `ηp² = .234` (`f = 0.55`) & Pacing `ηp² = .182` (`f = 0.47`)."),
            (1, "• <b>RQ3-Govern Stage:</b> Rules RAR `ηp² = .239`, Leakage Int. `ηp² = .199`, Slot F1 `ηp² = .778`."),
            (1, "• <b>RQ4-Optimize Stage:</b> Log Turns Prompt `ηp² = .793`, Interaction `ηp² = .111` (`f = 0.35`)."),
            (1, "→ Achieved post-hoc power <b>`> .99` on all main effects</b> and <b>`> .95` on all interactions</b>!"),
            "<b>2. Handling Departures from Normality & Equal Variance:</b>",
            (1, "Every omnibus test was verified with <b>`Welch / HC3` sandwich estimators</b> and <b>`Kruskal–Wallis / Friedman / ART` non-parametric tests</b> (`100%` concordance at `p < .001`)."),
            "<b>3. How the `+18%` Buffer Protected RQ2-Personalize Under Sphericity Loss:</b>",
            (1, "In RQ2-Personalize pacing error, Greenhouse–Geisser `ε = 0.65` compressed `df` from `(2, 64)` to `(1.30, 41.70)`. Buffering `N = 28 → 33` preserved `p = .007`!"),
        ],
        font_size=9.1,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`Q&A #1 Takeaway`):</b> "
        "Because every stage of `Identify → Personalize → Govern → Optimize` was powered a priori (`1 − β ≥ .804`) and achieved observed effects `2× to 13×` larger than `η² = .059`, zero solution approach decisions depend on underpowered or borderline `p`-values.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 59: DEFENSE Q&A #2 & #3 — PRIOR RESEARCH USED VS. ORIGINAL CONTRIBUTIONS
    # =========================================================================
    s = D.content_slide(
        "11. Anticipated Defense Committee Q&A Bank",
        "Defense Q&A #2 & #3: 'What Prior Research Was Used, and What Is Original?'",
        "Demarcating inherited building blocks from the original contributions of each stage in the 4-stage solution approach",
        notes="Use this slide to answer Defense Questions #2 and #3 concisely across all 4 stages.",
    )
    D.add_table(
        s, 0.35, 1.46, 12.63, 4.80,
        headers=[
            "Solution Stage",
            "Q2: Prior Research Foundations Applied",
            "Q3: Original Contributions in This Study (Not Present in Prior Literature)",
        ],
        rows=[
            [
                "RQ1-Identify: IDENTIFY\n(Trajectory Clustering &\nEarly Prefix Routing)",
                "Used <b>SBERT</b> (Reimers & Gurevych, 2019), <b>Gemini Embeddings</b> (Lee et al., 2025), <b>K-Means / Ward / HDBSCAN</b> (McInnes et al., 2017), <b>Bootstrap ARI</b> (Hennig, 2007), and <b>zero-temp LLM coding</b> (Gilardi et al., 2023).",
                "<b>Original Contribution 1:</b> Proved whole-dialogue travel clustering is confounded by wizard identity (`V = .45`) and session outcome (`V = .29 → κ = .24`). Designed the <b>prefix-truncated (`M = 9`) `46-d Blocks` representation</b>, 3-tier feature importance (`η², ‖β‖₂, Δκ`), and `RefinedArchetypeRouter` (`ARI = .89`, Test `κ = .535 to .958`, `ROC-AUC = .871 to .999`).",
            ],
            [
                "RQ2-Personalize: PERSONALIZE\n(Archetype-Routed\nFAISS Few-Shot ICL)",
                "Built on <b>few-shot ICL</b> (Brown et al., 2020), <b>KATE k-NN selection</b> (Liu et al., 2022), <b>FAISS indexing</b> (Johnson et al., 2021), and <b>BERTScore</b> (Zhang et al., 2020).",
                "<b>Original Contribution 2:</b> Partitioned FAISS into <b>persona-specific sub-indices (`1 per cluster`) with `[SLOT]` masking + persona pacing directives</b>, and proved a <b>causal routing dependency</b> by contrasting Primary (`p = .211` Null) vs. Refined (`F = 9.79, p < .001, +31.8%` style, `3.87w` pacing error) archetypes.",
            ],
            [
                "RQ3-Govern: GOVERN\n(Neuro-Symbolic Policy\n& Leakage Verification)",
                "Drew motivation from <b>NeMo Guardrails</b> (Rebedea et al., 2023), <b>τ-bench policy failure benchmarks</b> (Yao et al., 2024), and <b>TD-EVAL</b> (Acikgoz et al., 2025).",
                "<b>Original Contribution 3:</b> Executed a <b>`2 × 2` factorial experiment crossing declarative `YAML` rule verification with cluster-adaptive prompting</b>. Quantified the <b>`35.9%` exemplar entity leakage hazard (`55.6%` incidence)</b> of unguarded ICL and proved a protective interaction (`F = 34.82, p < .001`) reducing leakage to `0.0%` while lifting violation sensitivity from `5.6% to 98.6%`.",
            ],
            [
                "RQ4-Optimize: OPTIMIZE\n(Multi-Turn Economy\n& Slot Ledger)",
                "Built on <b>hospitality AI ROI theory</b> (Buhalis & Sinarta, 2019; Ivanov & Webster, 2019; Melián-González et al., 2021) and <b>PARADISE</b> (Walker et al., 1997).",
                "<b>Original Contribution 4:</b> Designed the <b>Verified Informed Slot Ledger + Persona Package Trade-Off Policies</b> and demonstrated a <b>`2 × 3` Prompting × Archetype interaction (`F = 10.89, p < .001`)</b>—cutting turns by `29.5% to 42.7%` (steepest in Rigid Seekers, `d = −3.40`) and eliminating redundant slot questions (`RER .109 → .000`).",
            ],
        ],
        col_widths=[2.05, 4.45, 6.13],
        font_size=8.8,
        align_left_cols=(0, 1, 2),
        highlight_rows=(0, 1, 2, 3),
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`Q&A #2 & #3 Takeaway`):</b> "
        "Beyond the 4 individual stage innovations, the <b>overarching original contribution</b> is demonstrating how they cascade: `RQ1-Identify` makes `RQ2-Personalize` work (`p=.211 → p<.001`), `RQ3-Govern` makes `RQ2-Personalize` safe (`35.9% → 0.0%` leakage), and `RQ1-Identify+2+3` power `RQ4-Optimize` (`−35.8%` turns).",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.3,
    )

    # =========================================================================
    # SLIDE 60: DEFENSE Q&A #4 — DATASET AUTHENTICITY, PURPOSE & RESEARCH FIT
    # =========================================================================
    s = D.content_slide(
        "11. Anticipated Defense Committee Q&A Bank",
        "Defense Q&A #4: 'What Is the Authenticity of the Datasets & How Do They Fit?'",
        "Addressing corpus provenance, original purpose, research fit, and how structural boundaries were resolved across RQ1-Identify to RQ4-Optimize",
        notes="Use this slide when asked Question #4 about dataset authenticity and fit.",
    )
    D.add_card(
        s, 0.35, 1.48, 6.15, 4.78,
        title="1. Authenticity & Original Purpose of the Two Datasets",
        header_bg=NAVY,
        bullets=[
            "<b>Microsoft Frames (El Asri et al., 2017 — Maluuba / Microsoft Research):</b>",
            (1, "• <b>Authenticity:</b> `100%` real human–human dialogues (`1,369` raw, `1,334` analytic; `19,986` turns) collected over 20 days between trained human travel wizards and travelers."),
            (1, "• <b>Original Purpose:</b> Created specifically to move beyond simple slot-filling and capture <b>multi-turn consultative vacation package negotiation, budget ceilings, and non-linear frame-switching</b>."),
            "<b>MultiWOZ 2.2 (Budzianowski et al., 2018; Zang et al., 2020 — Cambridge / Google):</b>",
            (1, "• <b>Authenticity:</b> Peer-reviewed ACL/EMNLP benchmark (`10,438` dialogues; `1,499` analytic subset) with Google-verified slot span annotations."),
            (1, "• <b>Original Purpose:</b> Created to benchmark supervised multi-domain Dialogue State Tracking (hotel, train, taxi, attraction)."),
        ],
        font_size=9.3,
    )
    D.add_card(
        s, 6.80, 1.48, 6.18, 4.78,
        title="2. Fit for the 4-Stage Solution Approach & Resolution of Boundaries",
        header_bg=TEAL,
        bullets=[
            "<b>Why Microsoft Frames Fits RQ1-Identify to RQ4-Optimize Ideally:</b>",
            (1, "Contains natural human shopper diversity—hesitations, price bargaining, city comparisons, and `28.1%` no-suitable-option sessions—enabling authentic discovery of <i>Decisive Bookers</i>, <i>Open Explorers</i>, and <i>Rigid-Constraint Seekers</i>."),
            "<b>Why MultiWOZ 2.2 Fits RQ1-Identify External Validation:</b>",
            (1, "Because MultiWOZ has transactional city bookings without flight+hotel package bargaining, the RQ1-Identify transfer check (`t = 28.08, p < .001`) proves that consultative travel personas are domain-specific."),
            "<b>Transparent Resolution of Two Corpus Boundaries (`RQ3-Govern & RQ4-Optimize`):</b>",
            (1, "• <b>Boundary A (Tier-2 Rules in RQ3-Govern):</b> Public corpora log `0.0%` visa/passport/discount slots (`Table E4`). Authentic `D_test` user prefixes were preserved and paired with seeded Tier-2 states (`N = 144`)."),
            (1, "• <b>Boundary B (Closed-Loop Evaluation in RQ4-Optimize):</b> Static logs cannot reply to new agent policies. Simulators were seeded from `180` real `D_test` trip goals and verified at `95.6%` blind persona fidelity (`κ = .933`)."),
        ],
        font_size=9.2,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`Q&A #4 Takeaway`):</b> "
        "Combining authentic human Wizard-of-Oz discovery (`RQ1–RQ2 on Frames`) with controlled factorial injection (`RQ3-Govern`) and persona-audited closed-loop simulation (`RQ4-Optimize`) achieves both internal causal validity and real-world domain grounding.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 61: DEFENSE Q&A #5, #6 & #7 — JUDGE INDEPENDENCE, COLD-START & ICL VS. FINE-TUNING
    # =========================================================================
    s = D.content_slide(
        "11. Anticipated Defense Committee Q&A Bank",
        "Defense Q&A #5–#7: Judge Independence, Cold-Start (<9 Turns) & Fine-Tuning",
        "Prepared answers for technical questions on circularity, short conversations, and neuro-symbolic ICL vs. weight fine-tuning",
        notes="Cover Q5 (Judge LLM circularity), Q6 (What happens when turns < 9?), and Q7 (Why not fine-tune weights instead of FAISS + YAML rules?).",
    )
    D.add_card(
        s, 0.35, 1.48, 4.05, 4.78,
        title="Q5: 'Isn't Using an LLM Judge Circular or Biased?'",
        header_bg=NAVY,
        bullets=[
            "<b>Three-Layer Defense Against Judge Circularity:</b>",
            "<b>1. Deterministic Primary Metrics in All 4 Stages:</b>",
            (1, "• <b>RQ1-Identify:</b> Mathematical Silhouette, DB, ARI, and κ."),
            (1, "• <b>RQ2-Personalize:</b> Non-Gemini encoders (`all-MiniLM-L6-v2` cosine & `roberta-large` BERTScore) + exact word count."),
            (1, "• <b>RQ3-Govern & RQ4-Optimize:</b> Deterministic Python regex/set verifiers (`ELR`, `Slot F1`, `Turns`, `RER` in `metrics.py`)."),
            "<b>2. Cross-Model Dual-Judge Audit (`RQ3-Govern`):</b>",
            (1, "`gemini-2.5-flash` was cross-checked against the independent larger model `gemini-2.5-pro` (`n = 48`): <b>`95.8%` agreement (`κ = .917`)</b> and <b>`93.1%` (`κ = .861`)</b> vs. deterministic regex."),
            "<b>3. Blind Persona Audit (`RQ4-Optimize`):</b>",
            (1, "`gemini-2.5-pro` was blinded to labels and classified `43/45` simulated users (`95.6%, κ = .933`)."),
        ],
        font_size=8.9,
    )
    D.add_card(
        s, 4.60, 1.48, 4.10, 4.78,
        title="Q6: 'What Happens When Turns < 9? Are Predictions Wrong?'",
        header_bg=TEAL,
        bullets=[
            "<b>Total Turns (`T`) vs. User Messages (`M`) in Frames:</b>",
            (1, "Total turns average `14.90 (Mdn = 15.0)`: `96.0%` have `≥ 5` total turns (`≥ 3` user msgs) and `83.2%` have `≥ 9` total turns (`≥ 5` user msgs)."),
            "<b>Are Predictions Wrong When `M < 9`? No (`Table 12`):</b>",
            (1, "• <b>`m = 3` user msgs (`≈ 5` turns):</b> `59.4%` overall (`κ = .359`); <b>`87.5%` on short chats (`≤ 3` user msgs)</b>!"),
            (1, "• <b>`m = 5` user msgs (`≈ 9` turns — RQ2-Personalize Runtime):</b> `70.1%` overall (`κ = .535, ROC-AUC = .871`); <b>`81.8%` on `≤ 5`-msg chats</b> & `67.8%` on `> 5`-msg chats—already strong enough to yield `p < .001` in RQ2-Personalize!"),
            (1, "• <b>`m = 7` user msgs (`≈ 13` turns):</b> `82.0%` overall (`κ = .722`); `93.2%` on `≤ 7`-msg chats."),
            (1, "• <b>`m = 9` user msgs (`min(M, 9)` cap):</b> `97.3%` overall (`κ = .958, ROC-AUC = .998`)."),
        ],
        font_size=8.8,
    )
    D.add_card(
        s, 8.90, 1.48, 4.08, 4.78,
        title="Q7: 'Why Not Fine-Tune Weights Instead of FAISS + YAML Rules?'",
        header_bg=BLUE,
        bullets=[
            "<b>Three Enterprise Advantages of Neuro-Symbolic ICL Over Fine-Tuning:</b>",
            "<b>1. Instant Zero-Downtime Policy Updates (`< 1 ms`):</b>",
            (1, "When visa lead windows or promo discount caps change at an OTA, updating `rules_enterprise.yaml` (`RQ3-Govern`) takes 1 second with `98.6%` deterministic enforcement—whereas fine-tuning takes hours and still hallucinates arithmetic thresholds."),
            "<b>2. Zero Catastrophic Forgetting (`RQ2-Personalize`):</b>",
            (1, "Adding new exemplary human dialogues or seasonal packages to the FAISS sub-indices requires zero gradient updates."),
            "<b>3. Complete Compliance Auditability (`RQ1-Identify to RQ4-Optimize`):</b>",
            (1, "Every turn logs the exact predicted persona `k*`, the 3 retrieved FAISS IDs, the triggered `YAML` rule IDs, and the `Verified Informed Slot Ledger` state."),
        ],
        font_size=8.9,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`Q&A #5–#7 Takeaway`):</b> "
        "Each stage of `Identify → Personalize → Govern → Optimize` is modular, non-circularly verified, and hot-swappable in production without expensive LLM weight retraining.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.3,
    )

    # =========================================================================
    # SLIDE 62: DEFENSE Q&A #8 — QUOTATION AGREEMENT VS. REAL-WORLD BOOKING NOISE
    # =========================================================================
    s = D.content_slide(
        "11. Anticipated Defense Committee Q&A Bank",
        "Defense Q&A #8: Quotation Agreement vs. Real-World Paid Booking Noise",
        "Why linking checkout payment directly to chat turns induces exogenous noise, and why RQ4-Optimize measures Turns to Quotation Agreement",
        notes="Address the crucial distinction between reaching an agreed trip quotation inside the chat vs. external checkout conversion.",
    )
    D.add_card(
        s, 0.35, 1.48, 4.05, 4.78,
        title="1. The Real-World Attribution Problem:\nQuotation Agreement vs. Paid Checkout",
        header_bg=CORAL,
        bg_color=RED_BG,
        bullets=[
            "<b>Natural Boundary of a Consultative Chat:</b>",
            (1, "In travel counseling, a conversation concludes when the consultant delivers a <b>feasible, agreed itinerary & package quotation</b>."),
            "<b>Why Final Checkout Payment Carries Massive Exogenous Noise:</b>",
            (1, "Whether the customer pays for that quotation depends on <b>off-chat factors</b> outside the assistant's control:"),
            (2, "• Receiving a last-minute coupon from a competing travel portal;"),
            (2, "• Arranging personal lodging with relatives and buying flight-only tickets;"),
            (2, "• Spouse/employer PTO schedule changes or credit-card limits."),
            (1, "<b>Consequence:</b> Regressing paid checkout on chat turns confounds dialogue quality with external market noise!"),
        ],
        font_size=9.0,
    )
    D.add_card(
        s, 4.60, 1.48, 4.10, 4.78,
        title="2. How Literature & RQ1-Identify Stage\nEliminate Outcome Confounding",
        header_bg=NAVY,
        bullets=[
            "<b>PARADISE Framework (Walker et al., 1997) & TOD Surveys (Deriu et al., 2021):</b>",
            (1, "Explicitly decouple <b>Dialogue-Internal Goal Resolution</b> (reaching an agreed matching quotation) from exogenous commercial checkout."),
            "<b>Microsoft Frames (El Asri et al., 2017) & MultiWOZ 2.2:</b>",
            (1, "Frames has no payment gateway—its `book` act is strictly <b>verbal package quotation agreement</b>."),
            "<b>RQ1-Identify Design (`step2g`):</b>",
            (1, "Whole-dialogue clustering was confounded by session outcome (`V = .29 → κ = .24`, <b>Red path</b>)."),
            (1, "Making <b>Field 14 (`outcome`) AUDIT-ONLY</b> and truncating at `min(M, 9)` ensures RQ1-Identify personas reflect <i>how users shop</i>, not whether they bought!"),
        ],
        font_size=9.0,
    )
    D.add_card(
        s, 8.90, 1.48, 4.08, 4.78,
        title="3. What RQ4-Optimize Stage Measures\n& How Doctoral Pillar 5 Extends It",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>Exact RQ4-Optimize Stopping Criterion (`step4_rq4_simulation.py`):</b>",
            (1, "• <b>Goal Slots (5):</b> `origin, destination, departure_date, duration_nights, budget_amount`."),
            (1, "• <b>Stopping Event (`[ACCEPT_BOOKING]`):</b> Turn counter stops the moment the assistant elicits missing slots (`0% RER`) and presents a policy-compliant package quotation (`Option A, B, or D`) that satisfies the traveler's constraints (`7.93 → 5.09 turns, −35.8%`)."),
            "<b>Doctoral Pillar 5 (`Opportunity_ID` Extension):</b>",
            (1, "Extends this noise-free milestone across 4–5 repeat calls using <b>`Turns-to-Lead` (`TTL`), Per-Call `Turns-to-Quotation` (`TTQ_s`), and `CSET`</b> with right-censored `Cold → Warm → Hot` survival modeling!"),
        ],
        font_size=9.0,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`Q&A #8 Takeaway`):</b> "
        "Excluding outcome from `RQ1-Identify` clustering and measuring `Turns to Agreed Quotation` (plus `RER`) in `RQ4-Optimize` isolates the exact conversational efficiency levers that the AI architecture directly controls.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 63: DEFENSE Q&A #9 — HANDLING FLEXIBLE CUSTOMERS EXPLORING 2–3 OPTIONS
    # =========================================================================
    s = D.content_slide(
        "11. Anticipated Defense Committee Q&A Bank",
        "Defense Q&A #9: Handling Flexible Customers Who Explore 2–3 Options",
        "Separating healthy multi-option comparison (`Open Explorer`) from chatbot inefficiency via side-by-side 3-option quoting",
        notes="Explain how multi-option exploration is isolated in RQ1-Identify (Open Explorer) and served via side-by-side 3-option comparative quoting in RQ4-Optimize.",
    )
    D.add_card(
        s, 0.35, 1.48, 4.05, 3.25,
        title="1. RQ1-Identify Stage: Isolating Healthy\nMulti-Option Exploration (`Open Explorer`)",
        header_bg=NAVY,
        bullets=[
            "<b>Why Flexible Shoppers Compare 2–3 Options:</b>",
            (1, "Deliberative travelers naturally compare 2–3 cities or hotel tiers before choosing a quote."),
            "<b>How RQ1-Identify Isolates Them (`Table 15`):</b>",
            (1, "<b>Archetype 2 (`Open Explorer`, `25.5%` of `D_gold`):</b> Highest destination flexibility (`3.49/5`), highest exploration breadth (`2.96/5`), highest revision tendency (`3.03/5`), and longest human chats (`17.99 turns` vs. `14.96` DB & `10.64` RCS)."),
        ],
        font_size=9.0,
    )
    D.add_card(
        s, 4.60, 1.48, 4.10, 3.25,
        title="2. How `Zero-Shot` Fails Open Explorers\n(Sequential 1-Option Ping-Pong = 7.47 Turns)",
        header_bg=CORAL,
        bg_color=RED_BG,
        bullets=[
            "<b>What Happens in `Zero-Shot` (`Red Path ✗`):</b>",
            (1, "In `step4_rq4_simulation.py`, the `Open Explorer` simulator refuses quotation agreement until it has compared <b>at least 2–3 distinct within-budget package options</b>."),
            (1, "Because `Zero-Shot` presents only <b>1 option per turn (`Option A`)</b> and re-asks slots (`6.1% RER`), the traveler must ask <i>'What other package or hotel tier options do you have?'</i> across multiple turns (`7.47 turns`)."),
        ],
        font_size=9.0,
    )
    D.add_card(
        s, 8.90, 1.48, 4.08, 3.25,
        title="3. How `Cluster-Adaptive` Serves Them\n(Side-by-Side 3-Option Quote = 5.27 Turns)",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>`Open Explorer` Policy (`Green Winner ✓`):</b>",
            (1, "When `RQ1-Identify` routes an `Open Explorer`, `RQ4-Optimize` does <b>not</b> rush them or restrict their choices."),
            (1, "Instead, once budget is known, the agent presents a <b>structured SIDE-BY-SIDE COMPARISON of 3 distinct packages in a SINGLE turn (`Option A 4★`, `Option B 3.5★ Saver`, `Option D 5★ Shifted`)</b>—letting the explorer compare all 3 and choose in `5.27 turns (−29.5%, p < .001)`!"),
        ],
        font_size=9.0,
    )
    D.add_table(
        s, 0.35, 4.82, 12.63, 1.46,
        headers=["Refined Traveler Archetype", "Option Exploration Behavior", "Human Logs Turns M", "RQ4-Optimize Zero-Shot Turns M", "RQ4-Optimize Cluster-Adaptive Turns M", "Turn Savings (Δ%) & Mechanism"],
        rows=[
            ["Decisive Booker (45.0%)", "Fixed route/date; wants 1 matching quote fast", "14.96", "7.60", "5.00 (Floor)", "−34.2% (Direct 1-option confirmation + 0% RER)"],
            ["Open Explorer (25.5%)", "Flexible; compares 2–3 options before quote agreement", "17.99 (Longest)", "7.47", "5.27 (Still longest!)", "−29.5% (3-option side-by-side quote in 1 turn)"],
            ["Rigid-Constraint Seeker (29.5%)", "Strict ceiling conflict; needs feasible trade-off quote", "10.64 (68% walk away)", "8.73 (Longest AI)", "5.00 (Floor)", "−42.7% (Dual 4★ exact vs 5★ shifted-date quote)"],
        ],
        col_widths=[2.25, 3.05, 1.45, 1.55, 1.65, 2.68],
        font_size=8.6,
        align_left_cols=(0, 1, 5),
        highlight_rows=(1,),
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`Q&A #9 Takeaway`):</b> "
        "`Open Explorers` still have the longest conversations under `Cluster-Adaptive` (`5.27` vs. `5.00` turns) because healthy comparison is preserved—what is eliminated is the wasted 1-by-1 ping-pong elicitation (`−29.5% turns, d = −2.55`).",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 64: DEFENSE Q&A #10 — WHY 3 BEHAVIORAL ARCHETYPES VS. 500+ PARAMETER CLUSTERS?
    # =========================================================================
    s = D.content_slide(
        "11. Anticipated Defense Committee Q&A Bank",
        "Defense Q&A #10: Why 3 Behavioral Archetypes vs. 500+ Parameter Clusters?",
        "Why clustering on Origin × Destination × Window × Pax × Budget fails for prompting—and how Doctoral Pillar 1 combines C × K",
        notes="Address the committee question: Why not cluster on mandatory trip parameters (Destination, Window, Pax, Origin, Budget) into 500+ micro-clusters?",
    )
    D.add_card(
        s, 0.35, 1.48, 4.05, 4.78,
        title="1. Same 5 Trip Parameters ≠ Same\nConversational Strategy (`WHAT` vs. `HOW`)",
        header_bg=NAVY,
        bullets=[
            "<b>Parameters Tell SQL <i>WHAT</i> to Query; Archetypes Tell the LLM <i>HOW</i> to Converse:</b>",
            (1, "Suppose 3 shoppers share the <b>exact same 5 parameters</b>: <i>Dallas → Cancun, Aug 12 (5 nights), 2 adults, $2,400</i>. In a 500-cluster parameter taxonomy, all 3 land in the <b>same bucket</b>, yet:"),
            (2, "• <b>Shopper A (`Decisive Booker`):</b> Wants a crisp 13-word confirmation of 1 package."),
            (2, "• <b>Shopper B (`Open Explorer`):</b> Used Cancun only as an initial idea (`3.49/5` flex) and wants a 3-option comparison table."),
            (2, "• <b>Shopper C (`Rigid Seeker`):</b> Insists on a 5★ resort under `$2,400` (costs `$2,688`) and walks away unless given a dual 4★ vs. shifted-date 5★ trade-off!"),
            (1, "<b>RQ3-Govern Proof Against Entity Clustering (`Table 17`):</b>"),
            (2, "Retrieving unmasked exemplars by concrete cities/prices causes <b>`35.9%` Entity Leakage (`55.6%` incidence)</b>!"),
        ],
        font_size=8.8,
    )
    D.add_card(
        s, 4.60, 1.48, 4.10, 4.78,
        title="2. Mathematical & Operational Collapse\nat `k = 500+` Parameter Clusters (`Red ✗`)",
        header_bg=CORAL,
        bg_color=RED_BG,
        bullets=[
            "<b>1. Combinatorial Sparsity & Sample Starvation:</b>",
            (1, "`50 origins × 50 destinations × 12 months × 4 pax × 4 budgets = 480,000 cells`. Even at `k = 500` clusters across `N = 933` golden chats, each cluster averages <b>`933 / 500 = 1.86 dialogues`</b>—insufficient to retrieve `k_shot = 3` exemplars!"),
            "<b>2. Early-Turn Cold-Start Failure:</b>",
            (1, "At Turn 2–3, an `Open Explorer` often hasn't stated a destination or budget yet (<i>'Somewhere warm in September'</i>). A parameter router fails when slots are `None`, whereas the `46-d Blocks` router already achieves `59.4%–70.1%` accuracy!"),
            "<b>3. Statistical Power Collapse (`Eq. 1`):</b>",
            (1, "In RQ1-Identify (`Figure D1`), even `k ≥ 4` violated the `≥ 20%` adequacy floor. Powering `k = 500` at 80% power requires `N > 15,000` dialogues."),
        ],
        font_size=8.8,
    )
    D.add_card(
        s, 8.90, 1.48, 4.08, 4.78,
        title="3. How RQ1-Identify to RQ4-Optimize Separate `HOW` vs. `WHAT`\n+ Doctoral Pillar 1 (`C × K` Hierarchy)",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>How the Current 4-Stage Architecture Handles Parameters Without 500 Brittle Clusters:</b>",
            (1, "• <b>RQ1-Identify (`k = 3` Archetypes):</b> Selects conversational policy (`Decisive` vs. `Explorer` vs. `Rigid`)."),
            (1, "• <b>RQ2-Personalize (Continuous FAISS `k`-NN):</b> Searches inside `FAISS_Index[k*]` (`n ≥ 238`) for the 3 closest structural neighbors without sample starvation."),
            (1, "• <b>RQ3-Govern & RQ4-Optimize (`RuleEngine` + `Slot Ledger`):</b> Injects exact `Origin, Dest, Window, Pax, Budget` deterministically (`Slot F1 = .952`, `0.0%` leakage)."),
            "<b>Doctoral Pillar 1 (`Context C × Behavior K`):</b>",
            (1, "Crosses <b>macro trip regimes (`C = 8–12`: Family vs. Solo, Luxury vs. Economy, Urgent vs. Advance)</b> with <b>`K = 3` behavioral personas (`24–36` micro-clusters)</b> using hierarchical FAISS back-off!"),
        ],
        font_size=8.8,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`Q&A #10 Takeaway`):</b> "
        "Separating <b>behavioral persona routing (`RQ1-Identify & RQ2-Personalize`: HOW to converse)</b> from <b>symbolic slot & policy tracking (`RQ3-Govern & RQ4-Optimize`: WHAT parameters to enforce)</b> avoids sample starvation and prevents the `35.9%` entity leakage trap.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 65: DEFENSE Q&A #11 — CLUSTER NAMING RULES (APPENDIX F) & JUDGE LLM ROLE (APPENDIX G)
    # =========================================================================
    s = D.content_slide(
        "11. Anticipated Defense Committee Q&A Bank",
        "Defense Q&A #11: Who Named the 3 Clusters (App. F) & Judge LLM Role (App. G)?",
        "Deterministic Python centroid-mapping rules (`step2i`) vs. independent cross-verification gatekeeping (`gemini-2.5-pro`)",
        notes="Explain Appendix F (how K-Means integer IDs 0, 1, 2 are mapped to archetype names) and Appendix G (why the Judge LLM is strictly a cross-verification validator).",
    )
    D.add_card(
        s, 0.35, 1.48, 6.15, 4.78,
        title="1. Appendix F (Table F1): Deterministic Centroid Naming Rules\n(K-Means Outputs Integers 0, 1, 2 — Not English Names!)",
        header_bg=NAVY,
        bullets=[
            "<b>Why a Pre-Declared Python Rule Is Required:</b>",
            (1, "Unsupervised `K-Means` (`step2g_rq1_truncation.py`) outputs anonymous integer cluster IDs (`0, 1, 2`) that permute across random seeds (the <i>label-switching problem</i>)."),
            "<b>Deterministic Python Rule on Golden Centroids (`step2i_rq1_refined_archetypes.py`):</b>",
            (1, "• <b>Rule 1 — `idxmax(destination_flexibility)` → <i>Open Explorer</i>:</b>\n"
                "  Cluster with highest mean destination flexibility (<b>`3.49 / 5.0`</b>) & exploration breadth (<b>`2.96 / 5.0`</b>; longest chats = `17.99t`; `n = 238, 25.5%`)."),
            (1, "• <b>Rule 2 — `idxmax(decisiveness)` of remaining 2 → <i>Decisive Booker</i>:</b>\n"
                "  Cluster with highest decisiveness (<b>`3.97 / 5.0`</b>), politeness (<b>`4.26 / 5.0`</b>), and `99.3%` specific booking goal (`n = 420, 45.0%`)."),
            (1, "• <b>Rule 3 — Remaining cluster ID → <i>Rigid-Constraint Seeker</i>:</b>\n"
                "  Lowest destination/date flexibility (<b>`2.20 / 2.18`</b>) and `68.0%` no-suitable-option rate under strict ceilings (`n = 275, 29.5%`)."),
        ],
        font_size=9.0,
    )
    D.add_card(
        s, 6.80, 1.48, 6.18, 4.78,
        title="2. Appendix G (Table G1): Exact Role of the Judge LLM\n(Strictly Cross-Verification Gatekeeping — Zero Invented Metrics!)",
        header_bg=TEAL,
        bullets=[
            "<b>All 4 Primary Hypothesis Tests (`H01–H04`) Use Deterministic Math/Python Metrics:</b>",
            (1, "• <b>RQ1-Identify Stage:</b> Mathematical Silhouette, Davies–Bouldin, Bootstrap ARI (`.89`), and `κ` (`.359–.958`). (`gemini-2.5-flash` at `temp=0` is used <i>before</i> K-Means as the 16-field behavioral annotator, validated at `κ_w = .87–.96` & `ρ = .41–.64`)."),
            (1, "• <b>RQ2-Personalize Stage:</b> Non-Gemini encoders (`all-MiniLM-L6-v2` cosine, `roberta-large` BERTScore, exact word error). Zero Judge LLM used!"),
            (1, "• <b>RQ3-Govern & RQ4-Optimize (`Govern & Optimize`):</b> Deterministic Python string/set verifiers (`ELR`, `Slot F1`, turn counter, and regex slot-ledger `RER`)."),
            "<b>Exact Role of Independent `gemini-2.5-pro` Judge (`Tables C3 & G1`):</b>",
            (1, "• <b>Pilot Gatekeeper:</b> Caught a prompt-ordering issue in RQ3-Govern (`pilot_v1 → pilot_v2`) prior to full run."),
            (1, "• <b>RQ3-Govern Cross-Verifier (`n = 48`):</b> `95.8%` agreement (`κ = .917`) vs. `flash` and `93.1%` (`κ = .861`) vs. regex."),
            (1, "• <b>RQ4-Optimize Blind Persona Auditor (`n = 45`):</b> Verified simulator construct fidelity (`95.6%, κ = .933`)."),
        ],
        font_size=8.9,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`Q&A #11 Takeaway`):</b> "
        "Cluster names in `RQ1-Identify` are 100% deterministic functions of top-`η²` centroid coordinates (`Appendix F`), and the `gemini-2.5-pro` Judge in `RQ3-Govern & RQ4-Optimize` serves strictly as an independent quality-assurance gatekeeper (`Appendix G`).",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.3,
    )

    # =========================================================================
    # SLIDE 66: DEFENSE Q&A #12A (RQ4 BACKUP) — CLOSED-LOOP SIMULATION ORCHESTRATION
    # =========================================================================
    s = D.content_slide(
        "11. Anticipated Defense Committee Q&A Bank",
        "Defense Q&A #12A (RQ4-Optimize Backup): Closed-Loop Simulation Orchestration",
        "Who runs the closed loop (`step4_rq4_simulation.py`), how Agent & Customer LLMs interact, and the post-hoc role of the Judge LLM",
        notes="Explain the exact closed-loop orchestration in step4_rq4_simulation.py: deterministic Python loop controller, two gemini-2.5-flash participants (Agent & Customer Simulator), finite MAX_EXCHANGES=11 bound, and post-hoc-only blind Judge LLM (gemini-2.5-pro).",
    )

    def _add_loop_actor(left, top, width, height, hdr_col, bg_col, bdr_col, title_txt, body_lines):
        card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.adjustments[0] = 0.04
        card.fill.solid()
        card.fill.fore_color.rgb = bg_col
        card.line.color.rgb = bdr_col
        card.line.width = Pt(1.4)

        hdr_h = 0.34
        hdr = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(hdr_h))
        hdr.adjustments[0] = 0.04
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = hdr_col
        hdr.line.fill.background()
        tf_h = hdr.text_frame
        tf_h.word_wrap = True
        tf_h.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf_h.margin_left = tf_h.margin_right = Inches(0.05)
        p_h = tf_h.paragraphs[0]
        p_h.alignment = PP_ALIGN.CENTER
        _add_formatted_runs(p_h, title_txt, font_size=7.6, color=WHITE, bold=True)

        tb = s.shapes.add_textbox(Inches(left + 0.05), Inches(top + hdr_h + 0.03), Inches(width - 0.10), Inches(height - hdr_h - 0.05))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.02)
        tf.margin_top = tf.margin_bottom = Inches(0.01)
        for idx_l, ln in enumerate(body_lines):
            p = tf.paragraphs[0] if idx_l == 0 else tf.add_paragraph()
            p.space_after = Pt(1.5)
            _add_formatted_runs(p, ln, font_size=7.1, color=DARK)

    def _add_loop_arrow(left, top, width, label_top, label_bot, col=NAVY, two_way=False):
        shp_type = MSO_SHAPE.LEFT_RIGHT_ARROW if two_way else MSO_SHAPE.RIGHT_ARROW
        arr = s.shapes.add_shape(shp_type, Inches(left), Inches(top + 0.78), Inches(width), Inches(0.24))
        arr.fill.solid()
        arr.fill.fore_color.rgb = col
        arr.line.fill.background()
        tb1 = s.shapes.add_textbox(Inches(left - 0.08), Inches(top + 0.34), Inches(width + 0.16), Inches(0.42))
        tf1 = tb1.text_frame
        tf1.word_wrap = True
        tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = Inches(0)
        p1 = tf1.paragraphs[0]
        p1.alignment = PP_ALIGN.CENTER
        _add_formatted_runs(p1, label_top, font_size=6.5, color=col, bold=True)

        tb2 = s.shapes.add_textbox(Inches(left - 0.08), Inches(top + 1.05), Inches(width + 0.16), Inches(0.55))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        tf2.margin_left = tf2.margin_right = tf2.margin_top = tf2.margin_bottom = Inches(0)
        p2 = tf2.paragraphs[0]
        p2.alignment = PP_ALIGN.CENTER
        _add_formatted_runs(p2, label_bot, font_size=6.3, color=DARK)

    TOP_Y, BOX_H = 1.46, 2.15
    _add_loop_actor(
        0.35, TOP_Y, 2.20, BOX_H, NAVY, CARD_BG, NAVY,
        "1. Python Loop Harness\n(simulate_single_dialogue)",
        [
            "• <b>Deterministic Controller:</b> Runs `for ex_idx in range(MAX_EXCHANGES = 11)` (max 23 turns, `seed = 42`).",
            "• <b>Slot Tracking:</b> `detect_informed_slots()` updates `informed_slots` after every User turn.",
            "• <b>RER Audit:</b> `detect_redundant_request()` flags any repeat slot question.",
        ],
    )
    _add_loop_arrow(2.57, TOP_Y, 0.36, "Update\nSlots", "Track\nLedger", NAVY, two_way=False)
    _add_loop_actor(
        2.95, TOP_Y, 2.28, BOX_H, TEAL, CARD_ALT, TEAL,
        "2. Upstream Cascade\n(RQ1–RQ3 Artifacts)",
        [
            "• <b>`RQ1-Identify`:</b> `RefinedArchetypeRouter` (`DB / OE / RCS`).",
            "• <b>`RQ2-Personalize`:</b> `[SLOT]`-masked FAISS exemplars (`k = 3`).",
            "• <b>`RQ3-Govern & RQ4`:</b> `Verified Informed Slot Ledger` + `Archetype Turn-Economy Policy`.",
        ],
    )
    _add_loop_arrow(5.25, TOP_Y, 0.36, "Inject\nPolicy", "4-Option\nInventory", TEAL, two_way=False)
    _add_loop_actor(
        5.63, TOP_Y, 2.30, BOX_H, GREEN, GREEN_BG, GREEN,
        "3. Travel Agent LLM\n(gemini-2.5-flash, T=0.2)",
        [
            "• <b>Arm 1 (`Zero-Shot`):</b> Step-by-step intake checklist; presents 1 package at a time (no ledger).",
            "• <b>Arm 2 (`Cluster-Adaptive`):</b> Checks Slot Ledger (`0% RER`) + presents persona-matched quote (`Options A/B/C/D`).",
        ],
    )
    _add_loop_arrow(7.95, TOP_Y, 0.42, "Live Turn\nExchange", "Turn 1..T\n(No Skips!)", CORAL, two_way=True)
    _add_loop_actor(
        8.39, TOP_Y, 2.30, BOX_H, BLUE, CARD_BG, BLUE,
        "4. Customer Simulator LLM\n(gemini-2.5-flash, T=0.2)",
        [
            "• <b>Turn 1 Seed:</b> States `Origin, Dest, Date, Duration, Adults` (`Budget` withheld until asked).",
            "• <b>Persona Rules:</b> Follows `USER_PERSONA_INSTRUCTIONS[arch]`.",
            "• <b>Closure:</b> Outputs `[ACCEPT_BOOKING]` once budget + persona quote criteria are met.",
        ],
    )
    _add_loop_arrow(10.71, TOP_Y, 0.36, "After Loop\nEnds Only", "n = 45\nBlind Audit", GOLD, two_way=False)
    _add_loop_actor(
        11.09, TOP_Y, 1.89, BOX_H, CORAL, RED_BG, GOLD,
        "5. Blind Judge LLM\n(gemini-2.5-pro, T=0)",
        [
            "• <b>NOT in the Loop!</b> Never controls or stops the conversation.",
            "• <b>Post-Hoc Audit Only:</b> Blindly classifies `n = 45` finished transcripts (`95.6%` acc., `κ = .933`).",
        ],
    )

    D.add_card(
        s, 0.35, 3.74, 4.05, 2.52,
        title="Q1: Who Runs the Closed Loop?\n(Deterministic Python Harness — NOT Judge LLM)",
        header_bg=NAVY,
        bullets=[
            "<b>Python Harness (`step4_rq4_simulation.py`):</b>",
            (1, "Orchestrates the live alternating loop between the <b>Agent LLM</b> and the <b>Customer Simulator LLM</b> across all `N = 180` held-out test dialogues (`6 cells × 30`)."),
            "<b>Exact Role of Judge LLM (`gemini-2.5-pro`):</b>",
            (1, "The Judge LLM is <b>never</b> inside the loop. It runs <i>only after all 180 simulations finish</i> to verify that simulated customers faithfully enacted their assigned persona (`95.6%` accuracy vs. `33.3%` chance, `κ = .933`, `Table C3`)."),
        ],
        font_size=8.5,
    )
    D.add_card(
        s, 4.60, 3.74, 4.10, 2.52,
        title="Q2: Is the Loop Infinite & How Does It Stop?\n(Bounded at MAX_EXCHANGES = 11 + Dual Gate)",
        header_bg=TEAL,
        bullets=[
            "<b>Hard Upper Cap (`MAX_EXCHANGES = 11`):</b>",
            (1, "The loop is <b>finite</b> (capped at 11 agent–user exchanges = max 23 turns) so no dialogue can run indefinitely."),
            "<b>Early Quotation Termination (`break` at Line 384):</b>",
            (1, "After each customer reply, Python checks two mandatory conditions before terminating:"),
            (2, "1. <b>Slot Gate:</b> `ex_idx >= 1 and 'budget_amount' in informed_slots` (all 6 trip slots, including budget, have been shared)."),
            (2, "2. <b>Quotation Gate:</b> Customer outputs `[ACCEPT_BOOKING]` after receiving a package quotation that satisfies their persona criteria (`100%` of dialogues completed within 5–11 turns)."),
        ],
        font_size=8.5,
    )
    D.add_card(
        s, 8.90, 3.74, 4.08, 2.52,
        title="Q3: Does the Script Skip Customer Turns?\n(No — 100% Genuine Live LLM Interactions)",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>Zero Skipped or Deleted Turns:</b>",
            (1, "The Python script <b>never</b> skips, truncates, or fast-forwards customer turns. Every turn counted in `total_turns` is a real LLM generation."),
            "<b>Why Turn Economy Improves (`7.93 → 5.09 Turns, −35.8%`):</b>",
            (1, "1. <b>`Verified Informed Slot Ledger`</b> prevents the Agent from wasting turns re-asking or re-confirming already-stated slots (`RER: .109 → .000`)."),
            (1, "2. <b>`Archetype Turn-Economy Policy`</b> formats the Agent's Turn 4 package quote to match what that specific persona requires to accept in Turn 5 (`5.00–5.27 turns`)."),
        ],
        font_size=8.5,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`Q&A #12A Takeaway`):</b> "
        "The RQ4-Optimize closed loop is a 100% live, bounded multi-turn negotiation between the Agent LLM and Customer Simulator LLM—turn savings (`−29.5%` to `−42.7%`) emerge naturally from upstream `RQ1-Identify → RQ3-Govern` intelligence, never from skipping turns.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.2,
    )

    # =========================================================================
    # SLIDE 67: DEFENSE Q&A #12B (RQ4 BACKUP) — SLOT FILLING, INVENTORY & QUOTATION ACCEPTANCE RULES
    # =========================================================================
    s = D.content_slide(
        "11. Anticipated Defense Committee Q&A Bank",
        "Defense Q&A #12B (RQ4-Optimize Backup): When Does the Customer Accept a Quote?",
        "How slot completeness (`informed_slots`), the 4-option package inventory (`A/B/C/D`), and persona rules trigger `[ACCEPT_BOOKING]`",
        notes="Walk through how slot filling and archetype-specific decision criteria work together in step4_rq4_simulation.py so the customer only accepts a quotation when both all slots are filled and their persona trade-off rules are satisfied.",
    )
    D.add_card(
        s, 0.35, 1.48, 4.20, 4.78,
        title="1. Slot-Filling Progression & 4-Option Package\nInventory (`build_inventory_for_goal`)",
        header_bg=NAVY,
        bullets=[
            "<b>How Slots Fill Across Opening Turns:</b>",
            (1, "• <b>Turn 1 (`USER` Opening):</b> Customer states 5 of 6 goal slots up front: `origin_city`, `destination_city`, `departure_date`, `duration_nights`, and `traveler_count_adults`. <b>`budget_amount` is withheld</b> until the Agent asks for it."),
            (1, "• <b>Turn 2 (`AGENT`) → Turn 3 (`USER`):</b> When the Agent asks for budget/preferences, the Customer shares `budget_amount` (`$1,500–$2,600`), completing all 6 required slots in `informed_slots`."),
            "<b>The 4 Package Options Available to Both Arms (Relative to Budget `B`):</b>",
            (1, "• <b>`Option A (4★ Value Match — Exact Date)`:</b> `0.88 × B` (<b>Fits Budget ✓</b>)"),
            (1, "• <b>`Option B (3.5★ Boutique w/ Breakfast — Exact Date)`:</b> `0.79 × B` (<b>Fits Budget ✓</b>)"),
            (1, "• <b>`Option C (5★ Luxury Package — Exact Date)`:</b> `1.18 × B` (<b>OVER Budget by +18% ✗</b>)"),
            (1, "• <b>`Option D (5★ Flexible-Date Deal — +2 Days Later)`:</b> `0.94 × B` (<b>Fits Budget ✓</b>)"),
        ],
        font_size=8.6,
    )
    D.add_card(
        s, 4.70, 1.48, 8.28, 1.52,
        title="2. How the `Cluster-Adaptive` Prompt Prevents Wasted Turns Before & During Quoting",
        header_bg=TEAL,
        bg_color=CARD_ALT,
        bullets=[
            (1, "• <b>Mechanism A — `Verified Informed Slot Ledger` (`Lines 328–334`):</b> Passed into every `Cluster-Adaptive` Agent turn: <i>'ALREADY PROVIDED: departure_date, destination_city, duration_nights, origin_city, traveler_count_adults | Remaining Uninformed Slots: budget_amount'</i> (Turn 2) → <i>'Remaining: NONE — present final package offer(s) for immediate booking'</i> (Turn 4). Eliminates redundant confirmation turns (`RER = .000`)."),
            (1, "• <b>Mechanism B — `CLUSTER_ADAPTIVE_TURN_ECONOMY_POLICY` (`Lines 165–189`):</b> Uses the `RQ1-Identify` routed persona label (`DB / OE / RCS`) to structure the Turn 4 package quotation so it immediately satisfies the customer's exact `[ACCEPT_BOOKING]` rule below:"),
        ],
        font_size=8.4,
    )
    D.add_table(
        s, 4.70, 3.08, 8.28, 3.18,
        headers=[
            "Customer Archetype\n(Routed by RQ1-Identify)",
            "Customer Simulator Acceptance Rule\n(`USER_PERSONA_INSTRUCTIONS` → `[ACCEPT_BOOKING]`)",
            "Why `Zero-Shot` Wastes Turns\n(Mean 7.93t | RER = .109)",
            "How `Cluster-Adaptive` Closes Fast\n(Mean 5.09t | RER = .000)",
        ],
        rows=[
            [
                "Decisive Booker\n(n = 30/cell)\nHigh decisiveness (3.97/5)",
                "If Agent asks 1 slot/confirmation question at a time without quoting a full package, answer only what was asked. <b>Accept (`[ACCEPT_BOOKING]`) as soon as budget is shared AND 1 complete within-budget package is quoted.</b>",
                "Asks hotel star preference + re-confirms stated slots (<i>'Just to confirm... is that correct?'</i>, `13.6% RER`) before quoting (`7.60 turns`).",
                "<b>Turn 2:</b> Asks ONLY for budget (`0% RER`).\n<b>Turn 4:</b> Immediately quotes `Option A (4★)` & `Option B (3.5★)` with exact prices → Customer accepts in <b>Turn 5 (`5.00t, −34.2%`)</b>.",
            ],
            [
                "Open Explorer\n(n = 30/cell)\nHigh exploration (2.96/5)",
                "Refuses to commit if shown only 1 package; asks <i>'What other package or hotel tier options are available?'</i> <b>Accept (`[ACCEPT_BOOKING]`) as soon as ≥ 2 distinct within-budget options (`A, B, or D`) have been presented.</b>",
                "Presents only 1 option in Turn 4, forcing customer to ask for another option across Turns 5–7 (`7.47 turns`, `6.1% RER`).",
                "<b>Turn 2:</b> Asks ONLY for budget.\n<b>Turn 4:</b> Presents a <b>side-by-side comparison of 3 options (`Options A, B, & D`) in a SINGLE turn</b> → Customer picks 1 in <b>Turn 5 (`5.27t, −29.5%`)</b>.",
            ],
            [
                "Rigid-Constraint Seeker\n(n = 30/cell)\nLow flexibility (2.20/5)",
                "Insists on <b>exact date + 5★ luxury under strict budget</b> (`Option C` is over budget!). If Agent flags `Option C` as over budget or offers only shifted `Option D` without `Option A`, pushes back. <b>Accepts once feasible `Option A (4★ exact date)` is offered.</b>",
                "Re-confirms slots (`13.0% RER`), quotes over-budget `Option C` alone or `Option D` alone, triggering multi-turn pushback (`8.73 turns`).",
                "<b>Turn 2:</b> Asks ONLY for budget.\n<b>Turn 4:</b> States `Option C (5★ exact)` exceeds budget AND <b>simultaneously quotes `Option A (4★ exact)` + `Option D (5★ +2d)`</b> → Customer accepts `Option A` in <b>Turn 5 (`5.00t, −42.7%`)</b>.",
            ],
        ],
        col_widths=[1.55, 2.45, 2.05, 2.23],
        font_size=7.6,
        align_left_cols=(0, 1, 2, 3),
        highlight_rows=(0, 1, 2),
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`Q&A #12B Takeaway`):</b> "
        "The Agent never sends an unsolicited quote before slots are filled, and the Customer never accepts until both `budget_amount` is shared and their archetype's trade-off criteria are met—proving that persona-aware quoting drives the `29.5%–42.7%` turn reduction.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.2,
    )

    # =========================================================================
    # SLIDE 68: DEFENSE Q&A #12C (RQ4 BACKUP) — CONCRETE TURN-BY-TURN TRANSCRIPT COMPARISON
    # =========================================================================
    s = D.content_slide(
        "11. Anticipated Defense Committee Q&A Bank",
        "Defense Q&A #12C (RQ4-Optimize Backup): Turn-by-Turn Transcript Trace (9 vs. 5 Turns)",
        "Actual cached dialogues from `data/final/rq4_sim_full.jsonl` (`Rigid-Constraint Seeker`) showing where `Zero-Shot` wastes 4 extra turns",
        notes="Walk through this side-by-side transcript from data/final/rq4_sim_full.jsonl turn by turn to show exactly how Turn 4 re-confirmation and Turn 6 single-option failure inflate Zero-Shot to 9 turns vs. 5 turns in Cluster-Adaptive.",
    )
    D.add_table(
        s, 0.35, 1.46, 12.63, 4.82,
        headers=[
            "Turn & Speaker",
            "`Zero-Shot` Baseline Transcript (9 Turns, RER = 0.250)\n[No Slot Ledger | Generic Step-by-Step Checklist Prompt]",
            "`Cluster-Adaptive Few-Shot + Slot Ledger` (5 Turns, RER = 0.000)\n[Routed as `Rigid-Constraint Seeker` | Active Slot Ledger]",
            "Orchestration & Turn-Economy Diagnostic\n(Why the Paths Diverge)",
        ],
        rows=[
            [
                "Turn 1\n[USER]",
                "<i>'Hi, I am looking to book a 7 nights trip from Chicago to Hamburg departing August 18 for 2 adults.'</i>",
                "<i>'Hi, I am looking to book a 7 nights trip from Toronto to Porto departing August 18 for 4 adults.'</i>",
                "<b>5 Slots Informed Up Front:</b> `origin, dest, date, duration, adults` added to `informed_slots`. `budget_amount` is still missing.",
            ],
            [
                "Turn 2\n[AGENT]",
                "<i>'Great! ... could you please tell me your preferred hotel star rating and your budget for the trip?'</i>",
                "<i>'What is your budget for this trip?'</i>",
                "<b>Slot Ledger Precision:</b> `Cluster-Adaptive` sees only `budget_amount` is missing and asks a crisp 7-word question (`0% RER`).",
            ],
            [
                "Turn 3\n[USER]",
                "<i>'I want a 5-star luxury package. My budget is $1500.'</i>",
                "<i>'My budget is $2600. I want a 5-star luxury package.'</i>",
                "<b>All 6 Slots Now Filled:</b> `budget_amount` added to `informed_slots`. Customer states strict `5★ + exact date` constraint.",
            ],
            [
                "Turn 4\n[AGENT]\n(Key Pivot!)",
                "<b>[REDUNDANT RE-ASK ✗]:</b> <i>'Thank you... Just to confirm, you're looking for a 7-night trip from Chicago to Hamburg, departing on August 18th, for 2 adults, with a 5-star hotel preference, and a budget of $1500. Is that all correct?'</i>",
                "<b>[PROACTIVE DUAL TRADE-OFF QUOTE ✓]:</b> <i>'Unfortunately, the Royal Palace Hotel (5-star) for Aug 18 is $3068, which exceeds your $2600 budget by $468. However, I can offer two alternatives within budget: <b>Option A (4-Star Value Match — Exact Date Aug 18): $2288</b>; <b>Option D (5-Star Flexible-Date — Aug 20): $2444</b>. Which would you prefer?'</i>",
                "<b>Why `Cluster-Adaptive` Wins Here:</b>\n• `Zero-Shot` wastes Turn 4 re-confirming 5 known slots (`RER = 1/4 = .250`).\n• `Cluster-Adaptive` sees `Remaining Slots: NONE` and applies the `Rigid-Constraint Seeker` policy to resolve the `5★` budget conflict in one turn!",
            ],
            [
                "Turn 5\n[USER]",
                "<i>'Yes, that is correct.'</i> (Forced to answer redundant confirmation)",
                "<b><i>'I will take Option A. [ACCEPT_BOOKING]'</i> → LOOP TERMINATES (5 Turns Total!)</b>",
                "<b>`Cluster-Adaptive` Closes at Turn 5 (`−44.4%` turns):</b> Both `budget_amount` and feasible `Option A` are satisfied!",
            ],
            [
                "Turn 6\n[AGENT]",
                "<b>[SINGLE-OPTION BOTTLENECK ✗]:</b> <i>'Based on your preference for a 5-star package on Aug 18, I have <b>Option C: Royal Palace Hotel ($1770)</b>. Please note this exceeds your $1500 budget by $270. Would you like to consider this, or explore other options?'</i>",
                "— (Session Already Completed in Turn 5)",
                "<b>2nd Wasted Exchange in `Zero-Shot`:</b> Quotes over-budget `Option C` without offering feasible `Option A ($1320)` in the same turn.",
            ],
            [
                "Turn 7 [USER]\nTurn 8 [AGENT]\nTurn 9 [USER]",
                "<b>Turn 7 [USER]:</b> <i>'Is there a package on August 18 that fits my budget?'</i> (Pushback)\n<b>Turn 8 [AGENT]:</b> <i>'Yes, there are packages on Aug 18 within $1500... Would you consider a 4-star or 3.5-star option?'</i>\n<b>Turn 9 [USER]:</b> <i>'Yes, I will consider a 4-star option on August 18. [ACCEPT_BOOKING]'</i> → <b>LOOP TERMINATES (9 Turns)</b>",
                "— (Session Already Completed in Turn 5)",
                "<b>Net Result Across `N = 180` Dialogues:</b>\n• `Zero-Shot`: `8.73` turns (`RCS`), `7.93` overall, `RER = .109`.\n• `Cluster-Adaptive`: `5.00` turns (`RCS`, `−42.7%`), `5.09` overall (`−35.8%`), `RER = .000` (`p < .001`).",
            ],
        ],
        col_widths=[1.25, 4.15, 4.15, 3.08],
        font_size=7.4,
        align_left_cols=(0, 1, 2, 3),
        highlight_rows=(3, 4),
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`Q&A #12C Takeaway`):</b> "
        "This side-by-side trace demonstrates visually why `RQ4-Optimize` requires every upstream stage: `RQ1-Identify` routes the `Rigid-Constraint Seeker`, `RQ2-Personalize` calibrates concise pacing, `RQ3-Govern` enforces rules without leakage, and `RQ4-Optimize`'s Slot Ledger + Dual Trade-Off Policy eliminates Turns 4–8.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.1,
    )

    # =========================================================================
    # SLIDE 69: DEFENSE Q&A #13 — IS GRADING AGAINST ARCHETYPE CENTROID C_k* FAIR?
    # =========================================================================
    s = D.content_slide(
        "11. Anticipated Defense Committee Q&A Bank",
        "Defense Q&A #13: 'Is Grading Zero-Shot & Static Few-Shot Against Archetype Centroid c_k* Fair?'",
        "Four methodological safeguards proving that RQ2-Personalize style/pacing evaluation is strictly non-circular, plus cluster-free ground-truth metrics",
        notes="Use this backup slide if a committee member asks whether comparing Zero-Shot and Static Few-Shot against the Archetype Agent-Style Centroid c_k* is biased toward Cluster-Adaptive prompting.",
    )
    D.add_card(
        s, 0.35, 1.48, 6.15, 4.78,
        title="Four Safeguards Proving Centroid Evaluation Is 100% Fair & Non-Circular",
        header_bg=NAVY,
        bullets=[
            "<b>Safeguard 1 — RQ1 Clustered `USER` Turns Only; `c_k*` Is Built from Human `AGENT` Turns:</b>",
            (1, "• In `RQ1-Identify`, K-Means (`k = 3`) clustered <b>only the customer's (`USER:`) messages</b> (`step2g_rq1_truncation.py`). Human travel agent (`AGENT:`) replies were <b>100% excluded</b> from clustering!"),
            (1, "• In `RQ2-Personalize`, the target centroid `c_k*` and word target `μ_k*` are computed from <b>real human travel agent (`AGENT:`) replies</b> in successful `D_gold` bookings (`step2_rq2_refined.py`), not from LLM outputs."),
            "<b>Safeguard 2 — `Zero-Shot` & `Static` Receive the Exact Same 9-Turn Live Context (`U1..U5, A1..A4`):</b>",
            (1, "• All 3 conditions read the exact same 5 customer messages (`U1..U5`) and 4 human agent replies (`A1..A4`)."),
            (1, "• If an unguided LLM could infer customer persona and mirror wizard style naturally from context, `Zero-Shot` had `100%` of the chat history needed to match `c_k*` and `μ_k*`—yet it failed (`cos = .536`, `10.12w` error)."),
            "<b>Safeguard 3 — Generation Uses Predicted `M = 5` (`k_hat`); Grading Uses True Held-Out `M = 9` (`k*`):</b>",
            (1, "• At generation time, `Cluster-Adaptive` only sees the router's <b>predicted `M = 5` label `k_hat`</b> on unseen `D_test`, whereas grading scores all 3 prompts against the <b>true `M = 9` reference label `k*`</b>."),
            "<b>Safeguard 4 — Non-Gemini Evaluators (`all-MiniLM-L6-v2` & Exact Word Count):</b>",
            (1, "• Primary `style_cos` uses an independent 384-d SBERT encoder (`all-MiniLM-L6-v2`), and `|W_gen − μ_k*|` is exact deterministic word count."),
        ],
        font_size=8.6,
    )
    D.add_table(
        s, 6.68, 1.48, 6.30, 2.88,
        headers=[
            "Evaluation Metric Across RQs",
            "Uses Cluster Centroid?",
            "What It Compares Against (Ruler)",
            "Empirical Result (Cluster-Adaptive vs. Baselines)",
        ],
        rows=[
            [
                "RQ2 Primary:\nSBERT Style Cosine (`c_k*`)",
                "Yes (`D_gold` Human\nAgent Turns)",
                "Mean vector of human wizard replies to persona `k*` in `D_gold`",
                "<b>`.603`</b> vs. `.459` Static (`+31.8%`) & `.536` Zero-Shot (`F = 9.79, p < .001`)",
            ],
            [
                "RQ2 Primary:\nPacing Error `|W_gen − μ_k*|`",
                "Yes (`D_gold` Human\nWord Mean)",
                "Mean word count of human wizard replies to persona `k*` (`13.8–16.2w`)",
                "<b>`3.87w` error</b> vs. `6.33w` Static & `10.12w` Zero-Shot (`F = 7.10, p = .002`)",
            ],
            [
                "RQ2 Cluster-Free:\nContextual `BERTScore F1`",
                "<b>NO (0% Cluster\nInvolvement)</b>",
                "Exact historical human wizard sentence at Turn 10 (`A5`) of that chat",
                "<b>`.415` (Highest)</b> vs. `.391` Zero-Shot & `.360` Static Few-Shot",
            ],
            [
                "RQ3 Cluster-Free:\nFactual `Slot F1` & `RAR`",
                "<b>NO (0% Cluster\nInvolvement)</b>",
                "Customer's ground-truth trip slots & 5 deterministic `YAML` rules",
                "<b>`Slot F1 = .952`</b> (`p < .001`), <b>`0.0%` leakage</b>, <b>`98.6%` viol. sens.</b>",
            ],
            [
                "RQ4 Cluster-Free:\nTurns to Quote (`TGC`) & `RER`",
                "<b>NO (0% Cluster\nInvolvement)</b>",
                "Total turns until customer outputs `[ACCEPT_BOOKING]` & slot re-asks",
                "<b>`5.09` vs. `7.93` turns (`−35.8%`, `p < .001`)</b>; <b>`RER = .000` vs. `.109`</b>",
            ],
        ],
        col_widths=[1.48, 1.18, 1.74, 1.90],
        font_size=8.0,
        align_left_cols=(0, 1, 2, 3),
        highlight_rows=(2, 3, 4),
    )
    D.add_card(
        s, 6.68, 4.46, 6.30, 1.80,
        title="20-Second Verbatim Defense Response if Asked About Centroid Fairness",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<i>'First, our clusters in RQ1 were formed exclusively on <b>customer (`USER`) messages</b>, whereas the target style centroid `c_k*` in RQ2 is built from <b>real human travel agent (`AGENT`) replies</b> in `D_gold`. Second, `Zero-Shot` and `Static Few-Shot` read the exact same 9-turn conversation prefix—so if they could adapt to the shopper's persona naturally from context, they would match `c_k*`. Third, to guarantee our conclusions never rest on a cluster centroid alone, we also evaluate <b>cluster-free `BERTScore F1`</b> against the exact single human reply in RQ2, <b>factual `Slot F1`</b> in RQ3, and <b>total `Turns to Quotation Agreement` (`−35.8%`)</b> in RQ4.'</i>",
        ],
        font_size=8.5,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`Q&A #13 Takeaway`):</b> "
        "Combining persona-centroid alignment (`style_cos`, `|W_gen − μ_k*|`) with completely cluster-free ground-truth benchmarks (`BERTScore F1`, `Slot F1`, `RAR`, `TGC`, `RER`) ensures that `Cluster-Adaptive` superiority is proven both stylistically and on hard task outcomes.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.1,
    )

    # =========================================================================
    # SLIDE 70: DEFENSE Q&A #14A — RQ1–RQ4 TESTING PROTOCOLS (1-TURN VS. MULTI-TURN & MODEL INDEPENDENCE)
    # =========================================================================
    s = D.content_slide(
        "11. Anticipated Defense Committee Q&A Bank",
        "Defense Q&A #14A: RQ1–RQ4 Testing Protocols (1-Turn Prefix vs. Multi-Turn Loop)",
        "Documented in Appendix H (Table H1): How each RQ defines a dialogue unit, start/end boundaries, and Gemini vs. non-Gemini models",
        notes="Use this slide to explain why RQ2 and RQ3 evaluate a single immediate Agent turn at the end of a frozen conversation prefix, whereas RQ4 runs a full multi-turn closed-loop conversation until [ACCEPT_BOOKING].",
    )
    D.add_table(
        s, 0.35, 1.46, 12.63, 3.12,
        headers=[
            "RQ & Stage",
            "Unit of Analysis & Sample (N)",
            "Turn Horizon (1-Turn vs. Multi-Turn)",
            "Start & End of Conversation in Test Harness",
            "Generator, Encoder & Evaluator Independence\n(Non-Gemini vs. Gemini vs. Deterministic)",
        ],
        rows=[
            [
                "RQ1-Identify\n(`step2_rq1_*.py`,\n`routing.py`)",
                "53 subsamples of `n = 500` on `D_gold` (`N = 159`); router tested on `D_test` (`n = 401`)",
                "<b>Offline Opening User Prefix Only</b>\n(`0` LLM replies generated)",
                "• <b>Start:</b> Customer Turn 1.\n• <b>End:</b> Truncated after first `M ∈ {3, 5, 7, 9}` `USER:` messages (`AGENT:` turns excluded).",
                "• <b>Features:</b> Gemini `PCA-20` + `gemini-2.5-flash` 13-field codebook.\n• <b>Evaluators:</b> <b>100% Deterministic Math</b> (`Silhouette`, `DB`, `ARI`, `κ`, `Softmax OvR ROC-AUC`).",
            ],
            [
                "RQ2-Personalize\n(`step2_rq2_refined.py`)",
                "`N = 33` held-out prefixes from `D_test` (`11/archetype × 3 prompts = 99` runs)",
                "<b>Single-Turn Prefix Completion</b>\n(<b>Exactly 1 immediate Agent turn</b> generated)",
                "• <b>Start:</b> Real archival Turns 1–9 (`U1..U5, A1..A4`).\n• <b>End:</b> Stops immediately after LLM generates <b>Turn 10 (`A5`, 1–3 sentences)</b>.",
                "• <b>Generator:</b> `gemini-2.5-flash`.\n• <b>Primary Evaluators (Non-Gemini):</b> 384-d SBERT (`all-MiniLM-L6-v2`), `roberta-large` BERTScore, & exact word count.\n• <b>Secondary Check:</b> Gemini 3,072-d cosine.",
            ],
            [
                "RQ3-Govern\n(`step3_rq3_experiment.py`)",
                "`N = 144` evaluations (`36` held-out prefixes × `4` cells; `18` viol. + `18` comp./cell)",
                "<b>Single-Turn Prefix Completion</b>\n(<b>Exactly 1 immediate Agent turn</b> generated)",
                "• <b>Start:</b> Real archival Turns `1..k` (`k ∈ {5..9}`, after Tier-1 slots stated) + active Tier-1/Tier-2 state.\n• <b>End:</b> Stops immediately after LLM generates <b>next 1 Agent turn</b>.",
                "• <b>Generator:</b> `gemini-2.5-flash` + Python `YAML` engine (`rules_enterprise.yaml`).\n• <b>Evaluators:</b> <b>Deterministic Python Set/Regex</b> (`ELR`, `Slot F1`, `det_pass`) + Dual Judge (`gemini-2.5-pro` audit, `κ = .917`).",
            ],
            [
                "RQ4-Optimize\n(`step4_rq4_simulation.py`)",
                "`N = 180` distinct seed dialogues (`6` cells × `n = 30` unique seeds/cell; `2 × 3`)",
                "<b>Full Multi-Turn Closed-Loop Simulation</b>\n(`5 to 14` alternating turns)",
                "• <b>Start:</b> Turn 1 customer opening request.\n• <b>End:</b> Multi-turn loop continues until customer simulator outputs <b>`[ACCEPT_BOOKING]`</b> (min 5, cap 14 turns).",
                "• <b>Simulator & Agent:</b> `gemini-2.5-flash` + Python `Slot Ledger` & `Inventory DB`.\n• <b>Evaluators:</b> <b>100% Deterministic Turn Counter (`TGC`, `ln TGC`) & Regex (`RER`)</b>; blind `gemini-2.5-pro` persona audit (`κ = .933`).",
            ],
        ],
        col_widths=[1.50, 1.85, 1.95, 3.45, 3.88],
        font_size=7.6,
        align_left_cols=(0, 1, 2, 3, 4),
        highlight_rows=(1, 2, 3),
    )
    D.add_card(
        s, 0.35, 4.68, 6.18, 1.60,
        title="Why RQ2 & RQ3 Generate Exactly 1 Single Immediate Agent Turn",
        header_bg=NAVY,
        bullets=[
            "<b>1. Matched-Prefix Experimental Control:</b> Slicing a frozen prefix (`Turns 1..k`) guarantees that all prompting/governance arms respond to the <b>exact same conversation history</b>. If allowed to run over multiple incremental turns, histories would diverge and invalidate RM-ANOVA / 2×2 ANOVA.",
            "<b>2. Zero-Tolerance Transactional Gatekeeping (RQ3):</b> When a customer's active booking state triggers a fatal/warning rule (`7-day` international visa window, `11 > 8 FIT adults` capacity, or `25%` discount), an enterprise agent <b>must enforce that rule on the immediate response turn</b>—it cannot stay silent and hope to mention it 3 turns later!",
        ],
        font_size=8.2,
    )
    D.add_card(
        s, 6.68, 4.68, 6.30, 1.60,
        title="Why RQ4 Runs a Full Multi-Turn Closed-Loop Conversation",
        header_bg=TEAL,
        bullets=[
            "<b>1. Cumulative Trajectory Outcomes (`TGC` & `RER`):</b> Conversational turn economy (`Turns to Quotation Agreement`) and `Redundant Elicitation Rate` (`RER`) emerge across multiple turns of slot elicitation and package trade-off negotiation.",
            "<b>2. Identical Governance & Slot Ledger Across Every Turn:</b> In `RQ4-Optimize`, the Python `Verified Informed Slot Ledger` and persona package policies run on <b>every assistant turn</b> from `Turn 2` until the customer simulator verifies all 6 slots + persona trade-off rules and outputs <b>`[ACCEPT_BOOKING]`</b>.",
        ],
        font_size=8.2,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`Appendix H, Table H1`):</b> "
        "Separating <b>Offline User-Prefix Routing (`RQ1`)</b>, <b>Controlled Single-Turn Prefix Completion (`RQ2` & `RQ3`)</b>, and <b>Full Multi-Turn Closed-Loop Simulation (`RQ4`)</b> gives us both surgical single-turn internal validity and end-to-end multi-turn operational realism.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.1,
    )

    # =========================================================================
    # SLIDE 71: DEFENSE Q&A #14B — DVs: CALCULATION METHODOLOGY, PRIMARY VS. SECONDARY & STATISTICAL RATIONALE
    # =========================================================================
    s = D.content_slide(
        "11. Anticipated Defense Committee Q&A Bank",
        "Defense Q&A #14B: DVs — Calculation Methodology & Statistical Rationale",
        "Documented in Appendix H (Table H2): Why each DV is needed (Primary vs. Secondary, ANOVA type, variance & zero-cell guards) and how it is calculated",
        notes="Walk through this master table from Appendix H (Table H2) to explain why each DV is classified as Primary vs. Secondary, why specific parametric/non-parametric/HC3 tests are required, and how each metric is computed.",
    )
    D.add_table(
        s, 0.35, 1.44, 12.63, 4.84,
        headers=[
            "RQ & Dependent Variable (DV)",
            "Test Hierarchy\n(Primary vs. Secondary)",
            "Why This DV & Statistical Test Are Necessary\n(ANOVA Type, Unequal Variance, Skewness, & Zero-Variance Cell Guards)",
            "Exact Calculation Methodology & Evaluator Family\n(Non-Gemini vs. Gemini vs. Deterministic Python/Regex)",
        ],
        rows=[
            [
                "<b>RQ1:</b> Cosine Silhouette `s ∈ [−1, 1]`",
                "<b>Primary DV</b>\n(Tests `H01`)",
                "Measures cohesion vs. separation. Because `HDBSCAN` & `K-Means` have <b>unequal variances (`Levene p < .001`)</b> across 53 shared seeds, One-Way ANOVA is paired with <b>Welch's `F`</b>, <b>RM-ANOVA</b>, & non-parametric <b>Kruskal–Wallis `H` / Friedman `χ²`</b>.",
                "<b>100% Deterministic Math:</b> On each `n = 500` subsample of `D_gold`, compute cosine distance `1 − cos(v_i, v_j)` and average `(b_i − a_i) / max(a_i, b_i)` across assigned points.",
            ],
            [
                "<b>RQ1:</b> `Davies–Bouldin`, `ARI`, `Prefix κ` & `Macro ROC-AUC`",
                "<b>Secondary & Diagnostic DVs</b>",
                "Silhouette alone cannot prove resample stability or early Turn-5 routability. `ARI` checks bootstrap stability (`≥ .87`); `κ` & `OvR ROC-AUC` prove out-of-sample `D_test` generalization.",
                "<b>100% Deterministic Math:</b> `DB` = scatter/separation ratio; `ARI` = 200 × 80% subsample stability; `κ` & `ROC-AUC` from L2 logistic router Softmax probabilities `P(y=c | x_M)` on `D_test`.",
            ],
            [
                "<b>RQ2:</b> De-lexicalized SBERT Style Cosine (`c_k*`)",
                "<b>Primary DV</b>\n(Tests `H02`)",
                "Evaluating 3 prompts on the same 33 prefixes induces <b>within-dialogue correlation (`ρ ≈ .50`)</b> → requires <b>One-Way RM-ANOVA (`Greenhouse–Geisser ε`)</b>, <b>Holm paired `t` (`d_z`)</b>, & <b>Friedman `χ²(2)`</b>. Uses a <b>Non-Gemini encoder</b> for 0% generator bias.",
                "<b>Non-Gemini Neural (`all-MiniLM-L6-v2` 384-d):</b> Mask entities to `[SLOT]` in generated Turn-10 reply and in `D_gold` human `AGENT` turns of persona `k*`; compute `cos(e_gen, c_k*)`.",
            ],
            [
                "<b>RQ2:</b> Pacing Error `|W_gen − μ_k*|` & `BERTScore F1`",
                "<b>Co-Primary & Cluster-Free Secondary</b>",
                "Pacing Error tests verbosity control in exact words. `BERTScore F1` provides a <b>100% cluster-free check</b> against exact archival human turn `A5`. Gemini 3,072-d cosine is a <b>Secondary sensitivity check</b>.",
                "<b>Deterministic Word Count & Non-Gemini `roberta-large`:</b> `|W_gen − μ_k*|` vs. `D_gold` human word norm (`13.8–16.2w`); `BERTScore F1` token alignment vs. exact historical human reply `A5`.",
            ],
            [
                "<b>RQ3:</b> Rule Adherence Rate (`RAR`: Viol. Sens. `n=72` & Spec. `n=72`)",
                "<b>Primary DV 1</b>\n(Tests `H03`)",
                "Tested via <b>2×2 Factorial OLS ANOVA</b> (Type II/III `Sum` contrasts). Overall `RAR` blends 18 violating + 18 compliant chats/cell → <b>Subgroup Split</b> isolates `Violation Sensitivity (5.6% → 98.6%)` from ceiling `Specificity (100%, SD = 0.00)`.",
                "<b>Deterministic Regex + Dual Judge:</b> Checks if active triggered `YAML` rules (`rules_enterprise.yaml`) are enforced on the single turn (`det_pass` regex + `gemini-2.5-flash` audited by `gemini-2.5-pro`, `κ = .917`).",
            ],
            [
                "<b>RQ3:</b> Entity Leakage (`ELR`) & Factual `Slot F1`",
                "<b>Primary DVs 2 & 3</b>\n(Tests `H03`) + Style Check",
                "Governed cells hit an <b>exact zero-variance boundary floor (`ELR = 0.000, SD = 0.000`)</b> while unguarded adaptive leaks at `.359` → violates OLS homoscedasticity, requiring <b>MacKinnon–White `HC3` SEs</b> & non-parametric <b>`ART` Factorial ANOVA</b>.",
                "<b>100% Deterministic Python Set Verifiers (`metrics.py`):</b> `ELR = |E_resp ∩ (E_ex \\ E_diag)| / max(1, |E_resp|)`; `Slot F1` = harmonic mean of precision & recall over active Tier-1 customer slots.",
            ],
            [
                "<b>RQ4:</b> Log Turns `ln(TGC)`, Raw Turns `TGC` & `RER`",
                "<b>Primary Parametric (`ln TGC`), Co-Primary (`TGC`) & Sec. (`RER`)</b>",
                "Tested via <b>2×3 Between-Subjects ANOVA</b> (`N = 180`). Because turn counts are right-skewed and two adaptive cells hit the <b>5.00-turn floor (`SD = 0.00`)</b> and <b>`RER = .000 (SD = .000)`</b>, `ln(TGC)` stabilizes variance while <b>`HC3` SEs</b>, <b>`ART` ANOVA</b> & <b>Mann–Whitney `U`</b> guard zero-variance cells.",
                "<b>100% Deterministic Turn Counter & Regex:</b> Count alternating `USER + AGENT` turns until `[ACCEPT_BOOKING]` (`min = 5`), take `ln(TGC)`, and divide agent turns re-asking known `informed_slots` by total agent turns (`RER`).",
            ],
        ],
        col_widths=[2.05, 1.55, 4.68, 4.35],
        font_size=7.3,
        align_left_cols=(0, 1, 2, 3),
        highlight_rows=(2, 4, 5, 6),
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`Appendix H, Table H2`):</b> "
        "Every RQ pairs a <b>model-independent Primary DV</b> (`Silhouette`, `SBERT Cosine`, `RAR/ELR/Slot F1`, `ln TGC`) with <b>cluster-free/cross-encoder Secondary DVs</b> and <b>zero-variance/skewness statistical guards (`Welch`, `Greenhouse–Geisser`, `HC3`, `ART`)</b>.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.1,
    )

    # =========================================================================
    # SLIDE 72: CONCLUDING SUMMARY, REPRODUCIBILITY INVENTORY & OPEN FLOOR
    # =========================================================================
    s = D.content_slide(
        "11. Concluding Summary & Defense Open Floor",
        "Concluding Summary, Reproducibility Inventory & Open Floor",
        "A complete, reproducible neuro-symbolic blueprint validated across Identify (RQ1) → Personalize (RQ2) → Govern (RQ3) → Optimize (RQ4)",
        notes="Final summary slide to leave on screen during open defense committee questions.",
    )
    D.add_card(
        s, 0.35, 1.48, 6.15, 4.78,
        title="Four-Stage Solution Approach Summary (All H01–H04 Rejected at p < .001)",
        header_bg=NAVY,
        bullets=[
            "<b>1. RQ1-IDENTIFY ( Early Archetype Routing):</b>",
            (1, "Truncating to opening user messages (`M = 9`) and fusing `PCA-20` Gemini embeddings with 13 validated LLM behavioral fields (`46-d Blocks`, `η² = .150–.580`) yields 3 stable personas (<b>`ARI = .89 / .87`</b>), 3 partitioned FAISS sub-indices, and held-out prefix routing of <b>`κ = .535 (M=5, ROC-AUC = .871)` to `κ = .958 (M=9, 97.3%, ROC-AUC = .999)`</b>."),
            "<b>2. RQ2-PERSONALIZE ( Style & Pacing ICL):</b>",
            (1, "Contrasting Primary (`p = .211` Null) vs. Refined (`F = 9.79, p < .001, ηp² = .234`) archetypes proves that `[SLOT]`-masked FAISS retrieval + pacing directives lift style convergence (`+31.8%` over static, `d_z = 0.74`) and cut pacing error to <b>`3.87 words (p = .007)`</b>."),
            "<b>3. RQ3-GOVERN ( Symbolic Policy & Leakage Guard):</b>",
            (1, "Declarative `YAML` verification + `[SLOT]` sanitization eliminates the <b>`35.9%` entity leakage</b> of unguarded ICL down to <b>`0.0%` (`Int. F = 34.82, p < .001`)</b> while raising violation enforcement sensitivity from <b>`5.6% to 98.6%` (`F = 498.78`)</b> and `Slot F1` to <b>`.952`</b> (`Dual-Judge κ = .917`)."),
            "<b>4. RQ4-OPTIMIZE ( Multi-Turn Turn Economy):</b>",
            (1, "Combining RQ1-Identify to RQ3-Govern with the `Verified Informed Slot Ledger` and persona package policies compresses turns by <b>`29.5% to 42.7%`</b> (`F = 664.43, Int. F = 10.89, p < .001`) with <b>`0.0%` redundant questions (`RER .109 → .000`, `Persona κ = .933`)</b>."),
        ],
        font_size=8.8,
    )
    D.add_card(
        s, 6.80, 1.48, 6.18, 4.78,
        title="Complete Reproducibility & Companion Deliverable Suite",
        header_bg=TEAL,
        bullets=[
            f"<b>GitHub Repository:</b> {REPO}",
            "<b>Complete Final Deliverable Suite (`final/`):</b>",
            (1, "<b>1. Comprehensive Defense Deck (`QM_640_Defense_Presentation_Sandeep_Surnella.pptx` — 72 Slides):</b> Full 1+ hour defense presentation aligned to the 4-stage solution approach (`Identify → Personalize → Govern → Optimize`), with 5 progressive solution approach diagrams, complete table/figure walkthroughs, doctoral roadmap, and 17 Q&A/backup deep-dives."),
            (1, "<b>2. 15-Minute Executive Defense Deck (`QM_640_Defense_Presentation_15Min_Sandeep_Surnella.pptx` — 28 Slides):</b> Condensed executive narrative."),
            (1, "<b>3. Text-to-ANOVA Methodology Reference (`QM_640_RQ_Text_to_ANOVA_Methodology_Reference.pptx` — 19 Slides):</b> Step-by-step mathematical derivations from raw text to noncentral-<i>F</i> power curves."),
            (1, "<b>4. Final Report (`QM_640_Final_Report_Sandeep_Surnella.docx` & `.pdf`):</b> Complete APA 7 manuscript, 5 executed notebooks, and 100% cached JSONL outputs (`seed = 42`)."),
        ],
        font_size=9.0,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Thank You — Open Floor for Defense Committee Questions</b>  |  "
        "<i>Surnella Sandeep  |  Department of Data Analytics, Walsh College  |  QM640: Data Analytics Capstone  |  Mentor: Mr. Smitraj Raut</i>",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=11.0,
    )
