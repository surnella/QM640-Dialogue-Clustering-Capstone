"""
Part 2 of the 15-Minute Executive & Defense Presentation (Slides 16–28):
  - Slides 16–17: Stage 2 — PERSONALIZE (RQ2 Results, Parts 1–2; from Slides 26–27)
  - Slides 18–20: Stage 3 — GOVERN (RQ3 Results, Parts 1–3; from Slides 28–30)
  - Slides 21–23: Stage 4 — OPTIMIZE (RQ4 Results, Parts 1–3; from Slides 31–33)
  - Slide 24: Consolidated Hypothesis Testing Scorecard & Operational Impact (from Slide 34)
  - Slide 25: Enhanced Storyline Flowchart with Key Proof Values: Identify (RQ1) -> Personalize (RQ2) -> Govern (RQ3) -> Optimize (RQ4) (Enhanced Slide 43)
  - Slide 26: Pictorial Roadmap Architecture (Condensing Slides 44, 45 & 47 with Teal Capstone vs. Amber Doctoral Color Coding)
  - Slide 27: Data Flow Diagram — Upgrading Cosine Similarity (RQ2) with an Additional Turn-Economy & USP Database Inside Clusters (Condensing Slide 48 without chess jargon)
  - Slide 28: Concluding Summary & Defense Open Floor
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
from report.final_context import FIG_FIN, FIG_INT, REPO


def build_slides_15min_part2(D, ctx):
    # =========================================================================
    # SLIDE 16 (FROM SLIDE 26): STAGE 2 — PERSONALIZE (RQ2 PART 1)
    # =========================================================================
    s = D.content_slide(
        "Stage 2: PERSONALIZE (RQ2 — Style & Pacing Adaptation)",
        "RQ2 (Part 1): Causal Contrast Between Primary (p = .211) and Refined (p < .001) Archetypes",
        "Figures E2 & 6: Proving that in-context style adaptation succeeds if and only if Stage 1 (Identify) routing is coherent",
        notes="Contrast Figure E2 (interim coarse routing kappa=.24) against Figure 6 (refined Blocks routing kappa=.535). This directly proves the causal link between RQ1 and RQ2.",
    )
    D.add_figure(
        s, os.path.join(FIG_INT, "fig_rq2_results.png"),
        0.35, 1.50, 6.15, 3.85,
        caption="Figure E2 (Coarse Whole-Dialogue Routing, κ = .24): Style Cosine F = 1.61, p = .211 (Null)",
    )
    D.add_figure(
        s, os.path.join(FIG_FIN, "fig_rq2_refined_results.png"),
        6.80, 1.50, 6.18, 3.85,
        caption="Figure 6 (Refined `Blocks` Prefix Routing, κ = .535): Style Cosine F = 9.79, p < .001 (Reject H02!)",
    )
    D.add_card(
        s, 0.35, 5.45, 6.15, 1.60,
        title="Why Primary RQ2 Yielded a Null Style Effect (p = .211)",
        header_bg=CORAL,
        bg_color=RED_BG,
        bullets=[
            "<b>1. Near-Chance Upstream Routing (39.4%, κ = .24):</b> 60.6% of held-out dialogues were routed to the <i>wrong</i> primary cluster at Turn 3.",
            "<b>2. Conflated Exemplar Pools:</b> Because primary clusters mixed user and wizard turns across whole sessions, retrieving from a cluster's FAISS pool fed mismatched examples into the prompt.",
        ],
        font_size=10.2,
    )
    D.add_card(
        s, 6.80, 5.45, 6.18, 1.60,
        title="Why Refined RQ2 Decisively Rejected H02 (p < .001)",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>1. Accurate `Blocks` Prefix Routing (70.1%, κ = .535 at M = 5):</b> Test dialogues were routed to their true behavioral archetype.",
            "<b>2. Coherent Sub-Indices & Pacing Directives:</b> Retrieving <i>k</i> = 3 slot-masked exemplars from the matched refined archetype boosted style convergence (<b>F = 9.79, p < .001</b>) and cut pacing error to <b>3.87 words</b>.",
        ],
        font_size=10.2,
    )

    # =========================================================================
    # SLIDE 17 (FROM SLIDE 27): STAGE 2 — PERSONALIZE (RQ2 PART 2: TABLE 14)
    # =========================================================================
    s = D.content_slide(
        "Stage 2: PERSONALIZE (RQ2 — Style & Pacing Adaptation)",
        "RQ2 (Part 2): Repeated-Measures Style Convergence & Pacing Calibration (Table 14)",
        "Evaluating Zero-Shot, Static Few-Shot (k = 3), and Cluster-Adaptive Few-Shot (k = 3) across N = 33 dialogues (99 calls)",
        notes="Walk through Table 14. Mention concisely that Greenhouse-Geisser sphericity corrections and non-parametric Friedman rank tests confirmed the exact same outcomes.",
    )
    D.add_table(
        s, 0.35, 1.50, 12.63, 3.25,
        headers=["Experiment & Outcome Metric (N = 33 Dialogues)", "Zero-Shot M (SD)", "Static Few-Shot M (SD)", "Cluster-Adaptive M (SD)", "RM-ANOVA F (GG df)", "p-value", "Partial ηp²"],
        rows=[
            ["Primary Archetypes (κ = .24) — Style Cosine", ".603 (.161)", ".650 (.165)", ".642 (.125)", "1.61 (1.95, 62.45)", ".211", ".048"],
            ["Primary Archetypes — Response Length (words)", "27.58 (5.43)", "16.33 (4.73)", "15.06 (4.35)", "95.32 (1.82, 58.31)", "< .001", ".749"],
            ["Refined Archetypes (κ = .535) — SBERT Style Cosine (Primary DV)", ".530 (.132)", ".453 (.169)", ".597 (.086)", "9.79 (1.88, 60.29)", "< .001", ".234"],
            ["Refined Archetypes — Gemini 3,072-d Topical Cosine", ".787 (.052)", ".775 (.055)", ".796 (.042)", "1.66 (1.94, 62.22)", ".200", ".049"],
            ["Refined Archetypes — Token-Level BERTScore F1", ".849 (.020)", ".844 (.023)", ".852 (.019)", "1.45 (1.92, 61.51)", ".243", ".043"],
            ["Refined Archetypes — Pacing Calibration Error (words)", "10.12 (8.98)", "6.33 (3.55)", "3.87 (3.58)", "7.10 (1.30, 41.70)", ".007", ".182"],
            ["Refined Archetypes — Response Length (words)", "25.45 (9.17)", "14.48 (5.16)", "16.33 (3.52)", "31.92 (1.41, 45.24)", "< .001", ".499"],
        ],
        col_widths=[3.75, 1.45, 1.55, 1.65, 1.85, 1.15, 1.23],
        font_size=9.5,
        align_left_cols=(0,),
        highlight_rows=(2, 5),
    )
    D.add_card(
        s, 0.35, 4.90, 6.15, 2.15,
        title="Pairwise Contrasts & Why SBERT Moves While BERTScore Stays Flat",
        header_bg=NAVY,
        bullets=[
            "<b>Holm Contrasts:</b> `Cluster-Adaptive` beats `Static Few-Shot` by <b>Δ = +.144 (+31.8%, t = 4.26, p<sub>Holm</sub> < .001, d<sub>z</sub> = 0.74)</b> and `Zero-Shot` by <b>Δ = +.067 (t = 2.37, p<sub>Holm</sub> = .049, d<sub>z</sub> = 0.41)</b>.",
            "<b>Metric Specificity:</b> Because all 3 prompts reply to the <b>same travel scenario</b>, broad 3,072-d topical cosine (.775–.796) and token-level `BERTScore F1` (.844–.852) stay invariant, whereas <b>sentence-level discourse style (`SBERT`, F = 9.79) and pacing (F = 7.10)</b> improve significantly.",
        ],
        font_size=9.6,
    )
    D.add_card(
        s, 6.80, 4.90, 6.18, 2.15,
        title="Pacing Calibration & Distributional Robustness Check",
        header_bg=TEAL,
        bullets=[
            "<b>Pacing Error Reduction (10.12w → 3.87w):</b> Human wizards average ~13w for <i>Decisive Bookers</i>, ~19w for <i>Open Explorers</i>, and ~15w for <i>Rigid Seekers</i>. `Cluster-Adaptive` calibrates verbosity to each persona (<i>p</i><sub>Holm</sub> ≤ .008).",
            "<b>Variance & Non-Parametric Robustness:</b> Greenhouse–Geisser sphericity corrections (ε = 0.65–0.94) and non-parametric Friedman rank tests (`χ² = 12.50, p = .002` for style; `χ² = 14.27, p < .001` for pacing) confirmed identical conclusions.",
        ],
        font_size=9.6,
    )

    # =========================================================================
    # SLIDE 18 (FROM SLIDE 28): STAGE 3 — GOVERN (RQ3 PART 1: 2x2 DESIGN & YAML RULES)
    # =========================================================================
    s = D.content_slide(
        "Stage 3: GOVERN (RQ3 — Policy Compliance & Leakage Elimination)",
        "RQ3 (Part 1): 2 × 2 Factorial Design, Declarative Rules & Dual-Judge Validation",
        "Tables 9 & C3: Crossing Rules Mode (Off vs. Active) × Prompting Strategy (Zero-Shot vs. Cluster-Adaptive) across N = 144 units",
        notes="Explain why Stage 2 (Personalize) needs Stage 3 (Govern): unmasked few-shot examples leak entities, and prompt-only rules are ignored 94.4% of the time.",
    )
    D.add_table(
        s, 0.35, 1.50, 7.35, 3.35,
        headers=["Rule ID & Policy Name", "Deterministic Trigger Condition", "Action", "Severity"],
        rows=[
            ["RULE_VISA_LEAD_TIME:\nVisa Processing Lead Time", "departure_lead_days < 15 on international destination", "flag_warning", "high"],
            ["RULE_PASSPORT_VALIDITY:\nPassport 6-Month Validity", "passport_expiry_months < 6 on international trip", "block_booking", "critical"],
            ["RULE_PARTY_SIZE_LIMIT:\nMaximum FIT Adult Capacity", "traveler_count_adults > 4 and package_type == 'FIT'", "escalate_group_desk", "medium"],
            ["RULE_DISCOUNT_CAP:\nPromotional Discount Ceiling", "discount_applied_percentage > 15.0%", "cap_discount", "high"],
            ["RULE_MIN_BUDGET_INTL:\nMinimum International Budget", "budget_amount < $500 per adult on international package", "reject_and_reprompt", "high"],
        ],
        col_widths=[1.8, 2.8, 1.4, 0.9],
        font_size=9.8,
        align_left_cols=(0, 1, 2),
        highlight_rows=(0, 1, 2, 3, 4),
    )
    D.add_card(
        s, 7.85, 1.50, 5.13, 3.35,
        title="Cross-Model Dual-Judge Reliability (Table C3)",
        header_bg=NAVY,
        bullets=[
            "<b>Independent Verification Against Self-Preference Bias:</b>",
            (1, "Responses generated by `gemini-2.5-flash` were audited on a stratified 48-unit subsample by both `gemini-2.5-flash` (Judge 1) and the larger reasoning model <b>`gemini-2.5-pro` (Judge 2)</b>."),
            "<b>Validation Results (n = 48):</b>",
            (1, "<b>Inter-Model Agreement:</b> <b>95.8%</b> (46 / 48 units identical; <b>Cohen's κ = .917</b>)."),
            (1, "<b>Agreement with Deterministic Regex Verifier (N = 144):</b> <b>93.1% raw agreement (κ = .861)</b>."),
        ],
        font_size=10,
    )
    D.add_callout(
        s, 0.35, 5.02, 12.63, 2.03,
        "<b>2 × 2 Experimental Protocol (N = 144, n = 36 per Cell, Seed = 42):</b>\n"
        "• 36 held-out test dialogues (12 per refined archetype) were paired with seeded Tier-2 policy states: <b>50% (18/cell) violated ≥ 1 YAML rule</b> and <b>50% (18/cell) were 100% policy-compliant</b> (verifying that the guardrail does not falsely block valid trips).\n"
        "• In `Rules Off`, policies are stated only as text instructions and few-shot exemplars are unmasked. In `Rules Active`, `RuleEngine` injects deterministic pre-check directives, masks exemplar entities with `[SLOT]`, and runs post-generation entity leakage sanitization.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=10.8,
    )

    # =========================================================================
    # SLIDE 19 (FROM SLIDE 29): STAGE 3 — GOVERN (RQ3 PART 2: FIGURE 7 PROFILES)
    # =========================================================================
    s = D.content_slide(
        "Stage 3: GOVERN (RQ3 — Policy Compliance & Leakage Elimination)",
        "RQ3 (Part 2): 2 × 2 Factorial Interaction Profiles (Figure 7 Walkthrough)",
        "Visualizing orthogonal main effects (Panels A, C, D) versus the protective interaction on Exemplar Leakage (Panel B)",
        notes="Walk through all 4 panels of Figure 7. Highlight Panel B's crossing lines showing how Rules Active eliminates the 35.9% entity leakage of Cluster-Adaptive prompting.",
    )
    D.add_figure(
        s, os.path.join(FIG_FIN, "fig_rq3_factorial_results.png"),
        0.35, 1.50, 7.55, 5.55,
        caption="Figure 7: 2 × 2 Factorial Interaction Profiles Across N = 144 Units (n = 36/cell; 95% CIs)",
    )
    D.add_card(
        s, 8.05, 1.50, 4.93, 5.55,
        title="How to Read the 4 Panels of Figure 7",
        header_bg=TEAL,
        bullets=[
            "<b>Panel A (Rule Adherence Rate):</b>",
            (1, "Lines are parallel: activating `RuleEngine` jumps overall adherence from <b>.500</b> (5.6% violation sensitivity) to <b>.938</b> (98.6% violation sensitivity), <i>F</i> = 43.92, <i>p</i> < .001."),
            (1, "Prompting mode alone has <b>zero effect</b> (<i>F</i> = 0.01, <i>p</i> = .916) → prompt engineering alone cannot enforce numeric policies!"),
            "<b>Panel B (Exemplar Entity Leakage — Protective Interaction):</b>",
            (1, "Sharp non-parallel divergence (<b>Interaction F = 34.82, p < .001</b>)!"),
            (1, "Under `Rules Off`, switching to Cluster-Adaptive spikes entity leakage from .000 to <b>.359 (55.6% incidence)</b>."),
            (1, "Under `Rules Active`, `[SLOT]` masking + post-gen sanitization lock leakage at <b>.000 (0.0%)</b>!"),
            "<b>Panel C (Factual Slot Coverage F1) & Panel D (Style Cosine):</b>",
            (1, "`Rules Active` lifts Slot F1 from .208/.485 to <b>.977/.952</b> (<i>F</i> = 489.52, <i>p</i> < .001), while `Cluster-Adaptive` lifts style alignment in both modes (<i>F</i> = 24.00, <i>p</i> < .001)."),
        ],
        font_size=9.8,
    )

    # =========================================================================
    # SLIDE 20 (FROM SLIDE 30): STAGE 3 — GOVERN (RQ3 PART 3: TABLE 15 & DIALOGUE PROOF)
    # =========================================================================
    s = D.content_slide(
        "Stage 3: GOVERN (RQ3 — Policy Compliance & Leakage Elimination)",
        "RQ3 (Part 3): Table 15 Factorial Results & Side-by-Side Output Proof",
        "Proving that 'Rules Active × Cluster-Adaptive Few-Shot' (Cell 4) is the unique Pareto-optimal configuration (Reject H03, p < .001)",
        notes="Show the streamlined Table 15 and the concrete Dallas-to-Tokyo output comparison. Mention that heteroscedasticity-robust HC3 and non-parametric ART ANOVA yielded the exact same results.",
    )
    D.add_table(
        s, 0.35, 1.50, 12.63, 3.15,
        headers=["Experimental Cell or 2 × 2 ANOVA Effect", "n or df", "Rule Acc. | Viol. Sens. / Comp. Spec.", "Exemplar Leakage M (SD) / Inc. %", "Slot Coverage F1 M (SD)", "Style Alignment M (SD)"],
        rows=[
            ["Cell 1: Rules Off × Zero-Shot", "36", ".500 (.507) | 5.6% / 94.4%", ".000 (.000) / 0.0%", ".208 (.242)", ".414 (.124)"],
            ["Cell 2: Rules Off × Cluster-Adaptive (Unguarded)", "36", ".500 (.507) | 5.6% / 94.4%", ".359 (.348) / 55.6%", ".485 (.269)", ".507 (.095)"],
            ["Cell 3: Rules Active × Zero-Shot", "36", ".944 (.232) | 100.0% / 88.9%", ".000 (.000) / 0.0%", ".977 (.096)", ".428 (.107)"],
            ["Cell 4: Rules Active × Cluster-Adaptive [Pareto Optimal]", "36", ".931 (.244) | 97.2% / 88.9%", ".000 (.000) / 0.0%", ".952 (.124)", ".506 (.086)"],
            ["Main Effect: Rules Mode", "1, 140", "F = 43.92 (p < .001), ηp² = .239", "F = 34.82 (p < .001), ηp² = .199", "F = 489.52 (p < .001), ηp² = .778", "F = 3.68 (p = .057), ηp² = .026"],
            ["Main Effect: Prompting Mode", "1, 140", "F = 0.01 (p = .916), ηp² = .000", "F = 34.82 (p < .001), ηp² = .199", "F = 20.46 (p < .001), ηp² = .128", "F = 24.00 (p < .001), ηp² = .146"],
            ["Interaction: Rules × Prompting", "1, 140", "F = 0.01 (p = .916), ηp² = .000", "F = 34.82 (p < .001), ηp² = .199", "F = 29.32 (p < .001), ηp² = .173", "F = 8.95 (p = .003), ηp² = .060"],
        ],
        col_widths=[3.05, 0.70, 2.40, 2.30, 2.15, 2.03],
        font_size=9.1,
        align_left_cols=(0,),
        highlight_rows=(3, 4, 6),
    )
    D.add_card(
        s, 0.35, 4.78, 6.15, 2.28,
        title="Real Output Example: Rules Off × Cluster-Adaptive (Cell 2)",
        header_bg=CORAL,
        bg_color=RED_BG,
        bullets=[
            "<b>Active User State:</b> Flying Dallas → Tokyo in <b>9 days</b> (violates 15-day visa rule), 2 adults, budget $2,600.",
            "<b>Generated Reply (Unguarded):</b> <i>'I can book you into the <b>Sapphire Bay Resort</b> on <b>SkyBridge Airways</b> for <b>$1,149</b> using code <b>VIP25</b>!'</i>",
            "<b>Failure:</b> Leaked 4 stale exemplar entities (`ELR = .80`) AND missed the 9-day visa violation (`RAR = 0`)!",
        ],
        font_size=9.8,
    )
    D.add_card(
        s, 6.80, 4.78, 6.18, 2.28,
        title="Real Output Example: Rules Active × Cluster-Adaptive (Cell 4)",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>Same User State:</b> Dallas → Tokyo in <b>9 days</b>, 2 adults, budget $2,600.",
            "<b>Generated Reply (Governed):</b> <i>'For your Dallas to Tokyo trip for 2 adults ($2,600 budget), please note that international departures within 15 days (9 days stated) require expedited visa verification before locking in your 9-night package.'</i>",
            "<b>Variance & Non-Parametric Check:</b> Because zero-leakage cells have zero variance, `MacKinnon–White HC3` (`F = 42.71 & 33.85`) and non-parametric `Aligned Rank Transform (ART)` ANOVA (`p < .001`) were also run and confirmed identical outcomes.",
        ],
        font_size=9.5,
    )

    # =========================================================================
    # SLIDE 21 (FROM SLIDE 31): STAGE 4 — OPTIMIZE (RQ4 PART 1: SIMULATION DESIGN)
    # =========================================================================
    s = D.content_slide(
        "Stage 4: OPTIMIZE (RQ4 — Multi-Turn Negotiation Economy)",
        "RQ4 (Part 1): 2 × 3 Multi-Turn Simulation Design & Persona Fidelity Validation",
        "Testing Prompting Strategy (Zero-Shot vs. Cluster-Adaptive) × Refined Archetype across N = 180 closed-loop dialogues (n = 30/cell)",
        notes="Explain how the closed-loop multi-turn simulation works, the 4-option package catalog, and the blind Gemini 2.5 Pro persona audit (95.6% accuracy, kappa = .933).",
    )
    D.add_card(
        s, 0.35, 1.50, 6.15, 3.65,
        title="Closed-Loop Multi-Turn Simulation Protocol (N = 180, n = 30/cell)",
        header_bg=NAVY,
        bullets=[
            "<b>1. Grounded Seed Trips:</b> 60 unique held-out test dialogues per archetype (180 distinct trip goals across 3 archetypes × 2 prompting modes = 180 episodes; <i>n</i> = 30/cell).",
            "<b>2. Realistic 4-Option Travel Inventory per Dialogue:</b>",
            (1, "<b>Option A (4-Star Exact Match):</b> Exact destination & dates, 4-star hotel, priced at <b>88% of budget</b>."),
            (1, "<b>Option B (3.5-Star Saver):</b> Exact dates, boutique hotel, priced at <b>72% of budget</b>."),
            (1, "<b>Option C (5-Star Exact Dates — Over Budget):</b> 5-star luxury hotel on exact dates, priced at <b>118% of budget</b> (creates realistic constraint conflict!)."),
            (1, "<b>Option D (5-Star Shifted Dates — Within Budget):</b> 5-star luxury hotel with dates shifted +3 days, priced at <b>94% of budget</b>."),
            "<b>3. Stopping Criterion:</b> Runs turn-by-turn until the user simulator issues `[ACCEPT_BOOKING]` on a valid package quotation.",
        ],
        font_size=9.8,
    )
    D.add_card(
        s, 6.80, 1.50, 6.18, 3.65,
        title="Blind Persona Fidelity Audit by Gemini 2.5 Pro (Table C3)",
        header_bg=TEAL,
        bullets=[
            "<b>User Simulator Validation Protocol (n = 45 Transcripts):</b>",
            (1, "An independent `gemini-2.5-pro` judge read ONLY the customer utterances from 45 simulated dialogues (15 per archetype, blinded to condition and archetype label) and rated Decisiveness, Exploration Breadth, and Constraint Rigidity (1–5) plus predicted the archetype."),
            "<b>Validation Results (Within-Simulation Fidelity):</b>",
            (1, "<b>Blind Classification Accuracy:</b> <b>95.6% (43 / 45 correct)</b> vs. 33.3% chance (exact binomial <b>p = 1.37 × 10⁻¹⁸ < .001</b>, <b>Cohen's κ = .933</b>)."),
            (1, "<b>Mean Behavioral Ratings (Decisiveness / Exploration / Rigidity):</b>\n"
                "      • <i>Decisive Booker:</i> <b>5.00</b> / 1.00 / 2.27\n"
                "      • <i>Open Explorer:</i> 2.80 / <b>4.27</b> / 1.60\n"
                "      • <i>Rigid-Constraint Seeker:</i> 1.67 / 2.27 / <b>4.33</b>"),
        ],
        font_size=9.8,
    )
    D.add_callout(
        s, 0.35, 5.30, 12.63, 1.75,
        "<b>How Stage 4 (OPTIMIZE) Combines the Informed Slot Ledger with Archetype Package Policies:</b>\n"
        "• <b>Zero-Shot Baseline:</b> Uses a generic sequential policy—asks clarifying questions one by one and offers only Option A first, without a Verified Informed Slot Ledger.\n"
        "• <b>Governed Cluster-Adaptive Few-Shot (Routed via `Blocks` at M = 9, κ = .958):</b> Combines the <b>Verified Informed Slot Ledger</b> (forbidding re-asking any stated slot) with archetype-specific action policies: (1) immediate Option A confirmation for <i>Decisive Bookers</i>; (2) side-by-side Option A vs. Option B/D comparison table for <i>Open Explorers</i>; and (3) proactive single-turn trade-off resolution (Option A [4-star exact date] vs. Option D [5-star flexible date]) for <i>Rigid-Constraint Seekers</i>.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=10.3,
    )

    # =========================================================================
    # SLIDE 22 (FROM SLIDE 32): STAGE 4 — OPTIMIZE (RQ4 PART 2: FIGURE 8 PROFILES)
    # =========================================================================
    s = D.content_slide(
        "Stage 4: OPTIMIZE (RQ4 — Multi-Turn Negotiation Economy)",
        "RQ4 (Part 2): Multi-Turn Turn Economy & Redundant Elicitation Profiles (Figure 8)",
        "Rejecting H04 (p < .001): Massive main effect of prompting (F = 664.43) AND significant Prompt × Archetype interaction (F = 10.89)",
        notes="Walk through Panels A and B of Figure 8. Highlight why the turn reduction is steepest (−42.7%) for Rigid-Constraint Seekers.",
    )
    D.add_figure(
        s, os.path.join(FIG_FIN, "fig_rq4_turn_economy_results.png"),
        0.35, 1.50, 7.55, 5.55,
        caption="Figure 8: Mean Turns to Goal Completion (Panel A) & Redundant Elicitation Rate (Panel B) Across N = 180 Simulations",
    )
    D.add_card(
        s, 8.05, 1.50, 4.93, 5.55,
        title="Visual Walkthrough of Figure 8",
        header_bg=NAVY,
        bullets=[
            "<b>Panel A (Turns to Goal Completion):</b>",
            (1, "Under `Zero-Shot` (coral bars), <i>Rigid-Constraint Seekers</i> take the longest (<b>8.73 turns</b>) because they reject Option A when their 5-star request exceeds budget, triggering multi-turn pushback loops."),
            (1, "Under `Cluster-Adaptive Few-Shot` (teal bars), turns drop dramatically across all three personas—and the drop is <b>steepest for Rigid-Constraint Seekers (−3.73 turns, −42.7%, 8.73 → 5.00 turns)</b>!"),
            (1, "This non-uniform compression produces the highly significant <b>Prompt × Archetype interaction: F(2, 174) = 10.89, p < .001, ηp² = .111</b>."),
            "<b>Panel B (Redundant Elicitation Rate — RER):</b>",
            (1, "Under `Zero-Shot`, the bot re-asks already stated slots in <b>19.4%</b> of turns for Decisive Bookers (who state many slots up front), 6.1% for Open Explorers, and 7.2% for Rigid Seekers."),
            (1, "Under `Cluster-Adaptive Few-Shot` with the Verified Informed Slot Ledger, RER drops to <b>0.000 (0.0%) across all 90 dialogues</b> (<i>F</i> = 63.02, <i>p</i> < .001)!"),
        ],
        font_size=10,
    )

    # =========================================================================
    # SLIDE 23 (FROM SLIDE 33): STAGE 4 — OPTIMIZE (RQ4 PART 3: TABLE 16)
    # =========================================================================
    s = D.content_slide(
        "Stage 4: OPTIMIZE (RQ4 — Multi-Turn Negotiation Economy)",
        "RQ4 (Part 3): Table 16 Turn Economy Breakdown by Archetype & Contrasts",
        "Detailed cell means, log-turn ANOVA statistics, and simple within-archetype contrasts across N = 180 simulations",
        notes="Walk through Table 16. Note concisely that heteroscedasticity-robust HC3, Aligned Rank Transform (ART), Welch t-tests, and Mann-Whitney U tests all confirmed the exact same p < .001 results.",
    )
    D.add_table(
        s, 0.35, 1.50, 12.63, 3.65,
        headers=["Archetype × Prompting Cell or 2 × 3 ANOVA Effect", "Total Turns M (SD)", "Log Turns ln(TGC) M (SD)", "Redundant Elicitation (RER)", "Turn Reduction Δ (%)", "Simple Contrast (t_log / Cohen's d)"],
        rows=[
            ["Decisive Booker — Zero-Shot (n = 30)", "7.60 (0.93)", "2.021 (0.119)", ".194 (.166)", "—", "—"],
            ["Decisive Booker — Cluster-Adaptive (n = 30)", "5.00 (0.00)", "1.609 (0.000)", ".000 (.000)", "−2.60 turns (−34.2%)", "t = −18.92 (p < .001), d = −3.94"],
            ["Open Explorer — Zero-Shot (n = 30)", "7.47 (1.01)", "2.002 (0.130)", ".061 (.115)", "—", "—"],
            ["Open Explorer — Cluster-Adaptive (n = 30)", "5.27 (0.69)", "1.654 (0.115)", ".000 (.000)", "−2.20 turns (−29.5%)", "t = −10.97 (p < .001), d = −2.55"],
            ["Rigid-Constraint Seeker — Zero-Shot (n = 30)", "8.73 (1.55)", "2.152 (0.175)", ".072 (.119)", "—", "—"],
            ["Rigid-Constraint Seeker — Cluster-Adaptive (n = 30)", "5.00 (0.00)", "1.609 (0.000)", ".000 (.000)", "−3.73 turns (−42.7%)", "t = −17.02 (p < .001), d = −3.40"],
            ["Main Effect: Prompting (df = 1, 174)", "F = 457.74 (< .001), ηp² = .725", "F = 664.43 (< .001), ηp² = .793", "F = 63.02 (< .001), ηp² = .266", "Overall: 7.93 → 5.09 (−35.8%)", "Rejects H04 (p < .001)"],
            ["Main Effect: Archetype (df = 2, 174)", "F = 7.77 (< .001), ηp² = .082", "F = 5.55 (.005), ηp² = .060", "F = 7.57 (< .001), ηp² = .080", "Explorers compare 3 options", "Significant persona difference"],
            ["Interaction: Prompting × Archetype (df = 2, 174)", "F = 14.37 (< .001), ηp² = .142", "F = 10.89 (< .001), ηp² = .111", "F = 9.70 (< .001), ηp² = .100", "Steepest gain in Rigid (−42.7%)", "Rejects H04 Interaction (< .001)"],
        ],
        col_widths=[2.95, 1.50, 1.65, 1.65, 2.00, 2.88],
        font_size=9.2,
        align_left_cols=(0, 4, 5),
        highlight_rows=(1, 3, 5, 6, 8),
    )
    D.add_callout(
        s, 0.35, 5.30, 12.63, 1.75,
        "<b>Protocol Floor (`5.00 Turns`) & Variance / Non-Parametric Robustness Check:</b>\n"
        "• Because each seed dialogue opens with 3/5 mandatory slots stated, the minimum trajectory to quotation agreement is <b>5 messages (`U1 → A1 [bundled intake] → U2 [remaining slots] → A2 [archetype-tailored package quote] → U3 [ACCEPT_BOOKING]`)</b>. `Cluster-Adaptive` reaches this 5.00-turn minimum for Decisive Bookers and Rigid-Constraint Seekers while giving Open Explorers a 3-option side-by-side comparison (5.27 turns).\n"
        "• <b>Variance & Non-Parametric Check:</b> Testing unequal variances with `Welch's t` / `MacKinnon–White HC3` (`F_log = 681.53 & 8.58, p < .001`) and rank-based `ART ANOVA` / `Mann–Whitney U` (`p < .001`) confirmed that zero-variance floor cells do not alter any statistical conclusion (full derivations in Backup Deck).",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.7,
    )

    # =========================================================================
    # SLIDE 24 (FROM SLIDE 34): CONSOLIDATED HYPOTHESIS SCORECARD & ROI
    # =========================================================================
    s = D.content_slide(
        "Empirical Synthesis Across RQ1–RQ4",
        "Consolidated Hypothesis Testing Scorecard (Table 11) & Operational ROI",
        "All four null hypotheses (H01–H04) are rejected at p < .001 across Identify → Personalize → Govern → Optimize",
        notes="Present Table 11 as the master executive scorecard across all four stages of the storyline.",
    )
    D.add_table(
        s, 0.35, 1.50, 12.63, 3.55,
        headers=["Storyline Stage & RQ", "Sample & Design", "Baseline vs. Proposed Performance", "Primary Parametric Test & Effect Size", "Variance & Non-Parametric Check", "Decision"],
        rows=[
            [
                "1. IDENTIFY (RQ1):\nAlgorithm Separation &\nPrefix Routing",
                "N = 159 runs\n(D_gold=933,\nD_test=401)",
                "Perm. Sil = −.013 vs. KM = .147, HDB = .211 (39.1% noise);\nBlocks ARI = .89 (.87 abl.); Routing κ = .535 (M=5) to .958 (M=9)",
                "One-way F(2, 156) = 91.33, p < .001, η² = .539\nMatched RM F(1.72, 89.30) = 83.04, ηp² = .615",
                "Welch & Kruskal–Wallis / Friedman\nconfirmed identical outcome (p < .001)",
                "Reject H01\n(p < .001)",
            ],
            [
                "2. PERSONALIZE (RQ2):\nStyle Convergence &\nPacing Calibration",
                "N = 33 dialogues\n× 3 conditions\n(99 calls)",
                "Style Cos: Static = .453, Zero = .530 vs. Adaptive = .597\nPacing Error: Zero = 10.12w, Static = 6.33w vs. Adaptive = 3.87w",
                "Style F(1.88, 60.29) = 9.79, p < .001, ηp² = .234\nPacing F(1.30, 41.70) = 7.10, p = .007, ηp² = .182",
                "GG sphericity & Friedman rank tests\nconfirmed identical outcome (p ≤ .002)",
                "Reject H02\n(p < .001)",
            ],
            [
                "3. GOVERN (RQ3):\nPolicy Adherence,\nLeakage & Slot F1",
                "N = 144 (2 × 2,\nn = 36/cell;\nκ_judge = .917)",
                "Viol. Sens.: 5.6% (Off) → 98.6% (Active); Comp. Spec.: 94.4% vs 88.9%\nFew-Shot Leakage: .359 (55.6%) → .000 (0.0%); Slot F1: .485 → .952",
                "RAR Acc F(1, 140) = 43.92; Sens F = 498.78\nELR Int. F = 34.82, p < .001; Slot F1 F = 489.52",
                "HC3 robust SE & ART rank ANOVA\nconfirmed identical outcome (p < .001)",
                "Reject H03\n(p < .001)",
            ],
            [
                "4. OPTIMIZE (RQ4):\nMulti-Turn Economy\n(Log Turns & RER)",
                "N = 180 (2 × 3,\nn = 30/cell;\nκ_persona = .933)",
                "Turns: −34.2% (DB), −29.5% (OE), −42.7% (RCS)\nOverall Turns: 7.93 → 5.09 (−35.8%); RER: .109 → .000",
                "Prompt F(1, 174) = 664.43, p < .001, ηp² = .793\nPrompt × Arch Int. F(2, 174) = 10.89, p < .001",
                "HC3, Welch t, ART & Mann–Whitney U\nconfirmed identical outcome (p < .001)",
                "Reject H04\n(p < .001)",
            ],
        ],
        col_widths=[1.95, 1.50, 3.25, 2.55, 2.20, 1.18],
        font_size=9.2,
        align_left_cols=(0, 1, 2, 3, 4),
        highlight_rows=(0, 1, 2, 3),
    )
    D.add_card(
        s, 0.35, 5.20, 12.63, 1.85,
        title="Illustrative Operational Scenario (Hypothetical OTA Handling 1,000,000 Monthly Sessions)",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>1. Cloud Inference & Latency Savings (−35.8%):</b> Compressing mean turns from 7.93 (`Zero-Shot`) to 5.09 (`Cluster-Adaptive`) corresponds to <b>2.84 fewer messages per session (≈ 2.84M fewer LLM calls/month)</b> in simulation.",
            "<b>2. Zero Exemplar Leakage & Policy Enforcement:</b> Eliminating exemplar entity leakage (55.6% incidence → <b>0.0%</b>) and raising violation sensitivity from 5.6% to <b>98.6%</b> (`F = 498.78, p < .001`) prevents hallucinated pricing and compliance breaches.",
            "<b>3. Rescuing Rigid-Constraint Shoppers:</b> Proactive single-turn trade-off framing cuts simulated negotiation turns by <b>42.7%</b> for the segment that experienced a 68.0% walk-away rate in historical human logs.",
        ],
        font_size=10.2,
    )

    # =========================================================================
    # SLIDE 25 (ENHANCED SLIDE 43): CUMULATIVE DECISION & CARRY-FORWARD FLOWCHART
    # =========================================================================
    s = D.content_slide(
        "6. Conclusive Storyline Synthesis",
        "Cumulative Decision & Data Flowchart: Identify (RQ1) → Personalize (RQ2) → Govern (RQ3) → Optimize (RQ4)",
        "Showing how each RQ locks in key methodological decisions and carries forward the 46-d Blocks clusters & artifacts into the next stage",
        notes=(
            "Walk through this cumulative decision-and-data flowchart from left to right. "
            "Highlight how Each RQ (1) inherits validated data/models from the previous RQ, "
            "(2) runs a powered ANOVA experiment, (3) locks in key design decisions (dropping inferior alternatives), "
            "and (4) carries forward concrete artifacts—starting with the 46-d Blocks clusters and FAISS sub-indices from RQ1—into RQ2, RQ3, and RQ4."
        ),
    )

    # Helper to draw a 4-tier cumulative stage column:
    # Tier 1: INHERITED FROM PRIOR STAGE(S)
    # Tier 2: EMPIRICAL TEST & KEY PROOF VALUES (Reject H0)
    # Tier 3: KEY DECISIONS LOCKED IN (Selected ✓ vs. Dropped ✗)
    # Tier 4: CONCRETE DATA & ARTIFACTS CARRIED FORWARD TO NEXT RQ ➔
    def _draw_story_column(
        col_idx,
        left,
        width,
        stage_badge,
        stage_title,
        hdr_c,
        bg_c,
        inherited_txt,
        proof_txt,
        decisions_txt,
        carried_forward_txt,
        arrow_label,
    ):
        # Outer column container
        outer = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(1.44), Inches(width), Inches(4.92))
        outer.adjustments[0] = 0.03
        outer.fill.solid()
        outer.fill.fore_color.rgb = bg_c
        outer.line.color.rgb = hdr_c
        outer.line.width = Pt(1.6)

        # Header banner
        hdr = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(1.44), Inches(width), Inches(0.42))
        hdr.adjustments[0] = 0.03
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = hdr_c
        hdr.line.fill.background()
        tf_h = hdr.text_frame
        tf_h.word_wrap = True
        tf_h.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_h1 = tf_h.paragraphs[0]
        p_h1.alignment = PP_ALIGN.CENTER
        _add_formatted_runs(p_h1, f"{stage_badge}: {stage_title}", font_size=9.3, color=WHITE, bold=True)

        # Tier 1: Inherited Inputs from Prior RQs (y = 1.91, h = 0.96)
        b1 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left + 0.06), Inches(1.91), Inches(width - 0.12), Inches(0.96))
        b1.adjustments[0] = 0.05
        b1.fill.solid()
        b1.fill.fore_color.rgb = WHITE
        b1.line.color.rgb = hdr_c
        b1.line.width = Pt(1.0)
        tf1 = b1.text_frame
        tf1.word_wrap = True
        tf1.margin_left = tf1.margin_right = Inches(0.05)
        tf1.margin_top = tf1.margin_bottom = Inches(0.02)
        _add_formatted_runs(tf1.paragraphs[0], inherited_txt, font_size=7.4, color=DARK)

        # Down arrow 1 -> 2
        da1 = s.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(left + width / 2 - 0.09), Inches(2.89), Inches(0.18), Inches(0.11))
        da1.fill.solid()
        da1.fill.fore_color.rgb = hdr_c
        da1.line.fill.background()

        # Tier 2: Empirical Proof & ANOVA Gate (y = 3.02, h = 1.12)
        b2 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left + 0.06), Inches(3.02), Inches(width - 0.12), Inches(1.12))
        b2.adjustments[0] = 0.05
        b2.fill.solid()
        b2.fill.fore_color.rgb = GREEN_BG
        b2.line.color.rgb = GREEN
        b2.line.width = Pt(1.1)
        tf2 = b2.text_frame
        tf2.word_wrap = True
        tf2.margin_left = tf2.margin_right = Inches(0.05)
        tf2.margin_top = tf2.margin_bottom = Inches(0.02)
        _add_formatted_runs(tf2.paragraphs[0], proof_txt, font_size=7.4, color=DARK)

        # Down arrow 2 -> 3
        da2 = s.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(left + width / 2 - 0.09), Inches(4.16), Inches(0.18), Inches(0.11))
        da2.fill.solid()
        da2.fill.fore_color.rgb = hdr_c
        da2.line.fill.background()

        # Tier 3: Key Decisions Locked In (y = 4.29, h = 0.94)
        b3 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left + 0.06), Inches(4.29), Inches(width - 0.12), Inches(0.94))
        b3.adjustments[0] = 0.05
        b3.fill.solid()
        b3.fill.fore_color.rgb = CALLOUT_BG
        b3.line.color.rgb = GOLD
        b3.line.width = Pt(1.2)
        tf3 = b3.text_frame
        tf3.word_wrap = True
        tf3.margin_left = tf3.margin_right = Inches(0.05)
        tf3.margin_top = tf3.margin_bottom = Inches(0.02)
        _add_formatted_runs(tf3.paragraphs[0], decisions_txt, font_size=7.3, color=DARK)

        # Down arrow 3 -> 4
        da3 = s.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(left + width / 2 - 0.09), Inches(5.25), Inches(0.18), Inches(0.11))
        da3.fill.solid()
        da3.fill.fore_color.rgb = hdr_c
        da3.line.fill.background()

        # Tier 4: Concrete Outputs Carried Forward to Next Stage (y = 5.38, h = 0.92)
        b4 = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left + 0.06), Inches(5.38), Inches(width - 0.12), Inches(0.92))
        b4.adjustments[0] = 0.06
        b4.fill.solid()
        b4.fill.fore_color.rgb = hdr_c
        b4.line.color.rgb = GOLD
        b4.line.width = Pt(1.4)
        tf4 = b4.text_frame
        tf4.word_wrap = True
        tf4.margin_left = tf4.margin_right = Inches(0.05)
        tf4.margin_top = tf4.margin_bottom = Inches(0.02)
        _add_formatted_runs(tf4.paragraphs[0], carried_forward_txt, font_size=7.3, color=WHITE)

        # Horizontal carry-forward connector arrow from bottom-right of this stage into next stage
        if col_idx < 3:
            arr_x = left + width + 0.01
            # Upper arrow connecting into Tier 1 (Inherited) of next column
            arr_top = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(arr_x), Inches(2.26), Inches(0.32), Inches(0.26))
            arr_top.fill.solid()
            arr_top.fill.fore_color.rgb = GOLD
            arr_top.line.color.rgb = NAVY
            arr_top.line.width = Pt(0.9)

            # Lower arrow at Tier 4 (Carried Forward)
            arr_bot = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(arr_x), Inches(5.70), Inches(0.32), Inches(0.28))
            arr_bot.fill.solid()
            arr_bot.fill.fore_color.rgb = GOLD
            arr_bot.line.color.rgb = NAVY
            arr_bot.line.width = Pt(0.9)

            # Vertical bridge line showing Tier 4 Output feeds Tier 1 Inherited of next stage
            v_bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(arr_x + 0.13), Inches(2.38), Inches(0.05), Inches(3.46))
            v_bar.fill.solid()
            v_bar.fill.fore_color.rgb = GOLD
            v_bar.line.fill.background()

            # Label badge on the vertical carry-forward bridge
            lbl_box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(arr_x - 0.04), Inches(3.65), Inches(0.42), Inches(0.88))
            lbl_box.adjustments[0] = 0.1
            lbl_box.fill.solid()
            lbl_box.fill.fore_color.rgb = NAVY
            lbl_box.line.color.rgb = GOLD
            lbl_box.line.width = Pt(0.9)
            tf_l = lbl_box.text_frame
            tf_l.word_wrap = True
            tf_l.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf_l.margin_left = tf_l.margin_right = Inches(0.01)
            pl = tf_l.paragraphs[0]
            pl.alignment = PP_ALIGN.CENTER
            _add_formatted_runs(pl, arrow_label, font_size=6.3, color=WHITE, bold=True)

    col_w = 2.90
    gap_w = 0.34
    start_x = 0.35

    _draw_story_column(
        0, start_x + 0 * (col_w + gap_w), col_w,
        "STAGE 1 (RQ1)", "IDENTIFY",
        NAVY, RGBColor(235, 240, 248),
        "<b>1. Foundation Input:</b>\n• 70/30 Split Firewall: <b>D<sub>gold</sub> = 933</b> (fit) & <b>D<sub>test</sub> = 401</b> (eval)\n• <i>N</i> = 159 subsample runs (53 × 3 algs) + Prefix grid <i>M</i> ∈ {3,5,7,9}",
        "<b>2. Empirical Proof (Reject H<sub>01</sub>, p < .001):</b>\n• <b>RQ1A:</b> <i>F</i>(2,156) = 91.33, η² = .539 (KM .147 vs. Ward .118; HDB drops 39.1% noise)\n• <b>RQ1B/C:</b> `46-d Blocks` (`PCA-20 Gemini + 26 LLM cols` at <i>M</i>=9) lifts stability to <b>ARI = .89</b> & routing from <b>κ = .24 → .535 (M=5) → .958 (M=9)</b>",
        "<b>3. Key Decisions Locked In:</b>\n• <b>✓ Select:</b> `K-Means (k=3)` (100% coverage) + `M=9 46-d Blocks` clusters (<i>Decisive 45%, Explorer 25.5%, Rigid 29.5%</i>)\n• <b>✗ Drop:</b> `HDBSCAN` (39.1% noise) & whole-chat vectors (κ=.24 outcome leakage)",
        "<b>4. CARRIED FORWARD TO RQ2–RQ4 ➔</b>\n• <b>`46-d Blocks` Cluster Labels</b> on all 933 D<sub>gold</sub> & 401 D<sub>test</sub> chats\n• Frozen <b>`RefinedArchetypeRouter`</b>\n• <b>3 Partitioned 46-d FAISS Sub-Indices</b>",
        "46-d\nBlocks\n+\nFAISS\nRouter",
    )

    _draw_story_column(
        1, start_x + 1 * (col_w + gap_w), col_w,
        "STAGE 2 (RQ2)", "PERSONALIZE",
        TEAL, RGBColor(228, 244, 243),
        "<b>1. Inherited from RQ1 (`46-d Blocks`):</b>\n• Sampled <b>N = 33 D<sub>test</sub> chats</b> (11 per `46-d Blocks` archetype × 3 prompts = 99 calls)\n• Uses RQ1's <b>`RefinedArchetypeRouter` (M=5)</b> & <b>3 46-d FAISS Sub-Indices</b>",
        "<b>2. Empirical Proof (Reject H<sub>02</sub>, p < .001):</b>\n• Coarse clusters (κ=.24) failed: <b>F = 1.61, p = .211 (Null)</b>\n• <b>`46-d Blocks` clusters (κ=.535) succeeded:</b> SBERT Style Cosine jumps <b>.453 → .597 (+31.8%, F = 9.79, p < .001, ηp² = .234)</b>; Pacing Error drops <b>10.12w → 3.87w (p = .007)</b>",
        "<b>3. Key Decisions Locked In:</b>\n• <b>✓ Select:</b> `Cluster-Adaptive Few-Shot` (<i>k</i>=3 `46-d FAISS` exemplars + Persona Pacing Directives: 13w / 19w / 15w)\n• <b>✗ Drop:</b> `Static Few-Shot` (.453 cos) & coarse primary clusters (<i>p</i>=.211)",
        "<b>4. CARRIED FORWARD TO RQ3–RQ4 ➔</b>\n• All <b>RQ1 `46-d Blocks` Artifacts</b> +\n• Validated <b>`Cluster-Adaptive` Prompting</b> (<i>k</i>=3 46-d FAISS exemplars + `ARCHETYPE_DIRECTIVES`)",
        "RQ1\nBlocks\n+\nRQ2\nAdaptive\nPrompt",
    )

    _draw_story_column(
        2, start_x + 2 * (col_w + gap_w), col_w,
        "STAGE 3 (RQ3)", "GOVERN",
        CORAL, RGBColor(253, 240, 238),
        "<b>1. Inherited from RQ1 + RQ2:</b>\n• Sampled <b>N = 144 D<sub>test</sub> units</b> (12 per `46-d Blocks` archetype × 3 = 36/cell; 2×2)\n• Uses <b>RQ1's `46-d Blocks` Router</b> + <b>RQ2's `Cluster-Adaptive` Prompting</b>",
        "<b>2. Empirical Proof (Reject H<sub>03</sub>, p < .001):</b>\n• Unguarded RQ2 prompt (`Rules Off`) leaks stale entities in <b>55.6% of replies (ELR = .359)</b> & enforces only <b>5.6%</b> of rules\n• `Rules Active` cuts leakage to <b>.000 (0.0%, Int. F = 34.82)</b>, lifts rule enforcement to <b>98.6% (F = 43.92)</b> & Slot F1 to <b>.952 (F = 489.52)</b>",
        "<b>3. Key Decisions Locked In:</b>\n• <b>✓ Select:</b> `Rules Active × Cluster-Adaptive` (Cell 4 Pareto Optimal: `[SLOT]` masking + `5 YAML rules` + post-gen sanitizer)\n• <b>✗ Drop:</b> Unmasked exemplars & prompt-only policy instructions",
        "<b>4. CARRIED FORWARD TO RQ4 ➔</b>\n• All <b>RQ1 (`46-d Blocks`) + RQ2 (`FAISS ICL`)</b> Artifacts +\n• Mandatory <b>`DeclarativeRuleEngine` (`Rules Active`)</b> locked ON for RQ4",
        "RQ1+2\n+\nActive\nYAML\nRule\nEngine",
    )

    _draw_story_column(
        3, start_x + 3 * (col_w + gap_w), col_w,
        "STAGE 4 (RQ4)", "OPTIMIZE",
        GREEN, RGBColor(230, 246, 235),
        "<b>1. Inherited from RQ1 + RQ2 + RQ3:</b>\n• Factor B IS the <b>3 `46-d Blocks` Archetypes</b> (30 D<sub>test</sub> trips/cell × 6 = 180 chats; simulator conditioned on RQ1 Table 13, κ=.933)\n• Uses <b>RQ1 Router (M=9, κ=.958) + RQ2 `[SLOT]` FAISS + RQ3 Active RuleEngine</b>",
        "<b>2. Empirical Proof (Reject H<sub>04</sub>, p < .001):</b>\n• Cuts turns <b>7.93 → 5.09 (−35.8%, F = 664.43, ηp² = .793)</b>\n• Steepest gain in <b>Rigid Seekers (−42.7%, 8.73→5.00t)</b>, Decisive (−34.2%), Explorer (−29.5%, Int. <b>F = 10.89, p < .001</b>)\n• Redundant Asks (`RER`): <b>.109 → .000 (F = 63.02)</b>",
        "<b>3. Key Decisions Locked In:</b>\n• <b>✓ Select:</b> `Verified Informed Slot Ledger` (0% RER) + <b>Persona Package Policies</b> (1-Opt Confirm / 3-Opt Compare / Dual Trade-Off)\n• <b>✗ Drop:</b> Memoryless sequential 1-option policy",
        "<b>4. FINAL VALIDATED ARCHITECTURE ➔</b>\n• Complete <b>4-Stage Neuro-Symbolic Engine (`RQ1 + RQ2 + RQ3 + RQ4`)</b>\n• Seeds <b>Doctoral Pillars 1–6</b> (Context×Behavior, Stages a–f, Turn-Q DB)",
        "",
    )

    D.add_callout(
        s, 0.35, 6.40, 12.63, 0.68,
        "<b>Cumulative Build Summary:</b> Yes—the <b>`46-d Blocks` clusters and `RefinedArchetypeRouter` created in RQ1</b> are the exact backbone carried forward into <b>RQ2, RQ3, and RQ4</b>: RQ1 locks in the 3 `46-d Blocks` clusters & FAISS sub-indices → RQ2 locks in `Cluster-Adaptive` prompting on those sub-indices → RQ3 locks in `[SLOT]` masking & the `YAML RuleEngine` to make that prompting safe → RQ4 deploys the combined `RQ1 + RQ2 + RQ3` stack with the `Slot Ledger` across all 3 `46-d Blocks` personas.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.3,
    )

    # =========================================================================
    # SLIDE 26 (CONDENSED SLIDES 44, 45 & 47): PICTORIAL CAPSTONE-TO-DOCTORAL ARCHITECTURE
    # =========================================================================
    s = D.content_slide(
        "7. Firming Up the Storyline: Capstone to Doctoral Architecture",
        "Pictorial Roadmap: Completed Capstone Blocks (Teal) vs. Doctoral Extensions (Amber)",
        "Condensing Slides 44, 45 & 47: How the 4-stage storyline is firmed up with Context × Behavior, Bayesian Drift, Call Stages (a–f) & 200-Package USP Narrowing",
        notes=(
            "Condenses Slides 44, 45, and 47 into one cohesive pictorial block diagram using the exact color coding from Slide 47: "
            "Teal/Navy for completed and validated Capstone modules (RQ1–RQ4), Amber/Coral for the Doctoral Dissertation extensions "
            "that firm up the storyline for live enterprise scale, and Emerald Green for the target human-like AI outcome."
        ),
    )

    CAP_BG = RGBColor(224, 242, 241)       # Soft Teal/Cyan tint for Capstone (RQ1-RQ4)
    CAP_HDR = TEAL                         # Deep Teal header for Capstone blocks
    CAP_BORDER = NAVY                      # Solid Navy border

    DOC_BG = RGBColor(255, 246, 224)       # Warm Amber/Gold tint for Doctoral Dissertation
    DOC_HDR = RGBColor(184, 51, 42)        # Coral/Crimson header for Doctoral blocks
    DOC_BORDER = GOLD                      # Warm Gold border

    GOAL_BG = RGBColor(225, 245, 232)      # Soft Emerald tint for Common Goal Hub
    GOAL_HDR = GREEN                       # Deep Emerald header
    GOAL_BORDER = GREEN

    # Top Legend Bar (y = 1.43, h = 0.30)
    def _add_legend_pill(left, width, bg_col, hdr_col, bdr_col, tag_txt, desc_txt):
        box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(1.43), Inches(width), Inches(0.30))
        box.adjustments[0] = 0.15
        box.fill.solid()
        box.fill.fore_color.rgb = bg_col
        box.line.color.rgb = bdr_col
        box.line.width = Pt(1.25)
        badge = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left + 0.04), Inches(1.46), Inches(1.60), Inches(0.24))
        badge.adjustments[0] = 0.2
        badge.fill.solid()
        badge.fill.fore_color.rgb = hdr_col
        badge.line.fill.background()
        p_b = badge.text_frame.paragraphs[0]
        p_b.alignment = PP_ALIGN.CENTER
        _add_formatted_runs(p_b, tag_txt, font_size=7.6, color=WHITE, bold=True)
        tb = s.shapes.add_textbox(Inches(left + 1.68), Inches(1.45), Inches(width - 1.72), Inches(0.26))
        tb.text_frame.word_wrap = True
        tb.text_frame.margin_left = tb.text_frame.margin_top = Inches(0)
        p_t = tb.text_frame.paragraphs[0]
        _add_formatted_runs(p_t, desc_txt, font_size=8.0, color=DARK, bold=True)

    _add_legend_pill(
        0.25, 4.15, CAP_BG, CAP_HDR, CAP_BORDER,
        "BUILT IN CAPSTONE (RQ1–RQ4)",
        "Empirically Validated Modules & Parameters (p < .001)",
    )
    _add_legend_pill(
        4.48, 4.55, DOC_BG, DOC_HDR, DOC_BORDER,
        "TO BE DONE (DOCTORAL P1–P6)",
        "Extensions Firming Up Live Enterprise Scale & Precision",
    )
    _add_legend_pill(
        9.11, 3.97, GOAL_BG, GOAL_HDR, GOAL_BORDER,
        "TARGET ENTERPRISE SYSTEM",
        "Human-Like Consultative Travel AI Architecture",
    )

    def _add_analysis_block(left, top, width, height, title, lines, is_capstone=True):
        bg = CAP_BG if is_capstone else DOC_BG
        hdr_c = CAP_HDR if is_capstone else DOC_HDR
        bdr_c = CAP_BORDER if is_capstone else DOC_BORDER

        card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.adjustments[0] = 0.03
        card.fill.solid()
        card.fill.fore_color.rgb = bg
        card.line.color.rgb = bdr_c
        card.line.width = Pt(1.4)

        hdr_h = 0.27
        hdr = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(hdr_h))
        hdr.adjustments[0] = 0.03
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = hdr_c
        hdr.line.fill.background()
        tf_h = hdr.text_frame
        tf_h.word_wrap = True
        tf_h.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf_h.margin_left = Inches(0.08)
        p_h = tf_h.paragraphs[0]
        _add_formatted_runs(p_h, title, font_size=8.5, color=WHITE, bold=True)

        tb = s.shapes.add_textbox(
            Inches(left + 0.06),
            Inches(top + hdr_h + 0.02),
            Inches(width - 0.12),
            Inches(height - hdr_h - 0.04),
        )
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.02)
        tf.margin_top = tf.margin_bottom = Inches(0.01)
        for idx, ln in enumerate(lines):
            p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
            p.space_after = Pt(1.5)
            _add_formatted_runs(p, ln, font_size=7.4, color=DARK)

    def _add_labeled_arrow(left, top, width, height, label_top, label_bottom, is_capstone=True):
        arr_c = CAP_HDR if is_capstone else DOC_HDR
        bdr_c = NAVY if is_capstone else GOLD
        arr = s.shapes.add_shape(
            MSO_SHAPE.RIGHT_ARROW,
            Inches(left + 0.03),
            Inches(top + height * 0.34),
            Inches(width - 0.06),
            Inches(0.24),
        )
        arr.fill.solid()
        arr.fill.fore_color.rgb = arr_c
        arr.line.color.rgb = bdr_c
        arr.line.width = Pt(0.75)

        tb1 = s.shapes.add_textbox(Inches(left - 0.02), Inches(top + 0.02), Inches(width + 0.04), Inches(0.32))
        tf1 = tb1.text_frame
        tf1.word_wrap = True
        tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = Inches(0)
        p1 = tf1.paragraphs[0]
        p1.alignment = PP_ALIGN.CENTER
        _add_formatted_runs(p1, label_top, font_size=6.9, color=NAVY if is_capstone else DOC_HDR, bold=True)

        tb2 = s.shapes.add_textbox(Inches(left - 0.02), Inches(top + height * 0.34 + 0.25), Inches(width + 0.04), Inches(0.45))
        tf2 = tb2.text_frame
        tf2.word_wrap = True
        tf2.margin_left = tf2.margin_right = tf2.margin_top = tf2.margin_bottom = Inches(0)
        p2 = tf2.paragraphs[0]
        p2.alignment = PP_ALIGN.CENTER
        _add_formatted_runs(p2, label_bottom, font_size=6.6, color=DARK)

    def _add_vert_connector(center_x, top_y, label_txt):
        arr = s.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(center_x - 0.11), Inches(top_y), Inches(0.22), Inches(0.14))
        arr.fill.solid()
        arr.fill.fore_color.rgb = GOLD
        arr.line.color.rgb = DOC_HDR
        arr.line.width = Pt(0.6)
        tb = s.shapes.add_textbox(Inches(center_x + 0.13), Inches(top_y - 0.02), Inches(1.65), Inches(0.16))
        tf = tb.text_frame
        tf.margin_left = tf.margin_top = Inches(0)
        p = tf.paragraphs[0]
        _add_formatted_runs(p, label_txt, font_size=6.5, color=DOC_HDR, bold=True)

    R1_Y, R2_Y, R3_Y = 1.80, 3.44, 5.08
    ROW_H = 1.50

    # COLUMN 1: STAGE 1 — IDENTIFY (RQ1 + PILLARS 1 & 2)
    C1_X, C1_W = 0.25, 2.65
    _add_analysis_block(
        C1_X, R1_Y, C1_W, ROW_H,
        "[BUILT: RQ1] Identify 3 User Archetypes",
        [
            "• <b>Method:</b> Opening prefix (`M=9`) `K-Means (k=3)` + `L2 Router` on `46-d Blocks`.",
            "• <b>Addressed Params:</b> `PCA-20` Gemini prefix + `16` LLM behavioral fields (<i>flexibility, decisiveness, exploration</i>).",
            "• <b>Proven Result:</b> `ARI = .89/.87`, `97.3%` prefix routing (`κ = .958`, `p < .001`).",
        ],
        is_capstone=True,
    )
    _add_vert_connector(C1_X + 0.85, R1_Y + ROW_H, "Firms Up: 1D k=3 → 2D Context×Behavior")

    _add_analysis_block(
        C1_X, R2_Y, C1_W, ROW_H,
        "[TO DO: P1] Hierarchical Clustering (C × K)",
        [
            "• <b>Gap Addressed:</b> Situational trip context shapes how personas behave.",
            "• <b>New Params (Tier 1 × Tier 2):</b> `party_type` (solo/family/group), `budget_stakes` (economy/luxury), `lead_window` × `K=3` personas (`24–36` micro-clusters).",
        ],
        is_capstone=False,
    )
    _add_vert_connector(C1_X + 0.85, R2_Y + ROW_H, "Firms Up: Hard k-Means → Soft Drift")

    _add_analysis_block(
        C1_X, R3_Y, C1_W, ROW_H,
        "[TO DO: P2] Soft-Mixture & Bayesian Drift",
        [
            "• <b>Gap Addressed:</b> `25.2%` boundary speakers (`s < .05`) & mid-call persona shifts after price shock.",
            "• <b>New Method:</b> Turn-by-turn posterior `P(z_t | u_1..t)` & soft style blending weights (`w_1..w_K`).",
        ],
        is_capstone=False,
    )

    # ARROWS 1 -> 2
    A1_X, A1_W = 2.91, 0.77
    _add_labeled_arrow(A1_X, R1_Y + 0.15, A1_W, ROW_H - 0.2, "RQ1 → RQ2", "3 Personas + Router (κ=.535→.958)", is_capstone=True)
    _add_labeled_arrow(A1_X, R2_Y + 0.15, A1_W, ROW_H - 0.2, "P1 Output", "C×K Regime + Stakes State", is_capstone=False)
    _add_labeled_arrow(A1_X, R3_Y + 0.15, A1_W, ROW_H - 0.2, "P2 Output", "Live Posterior P(z_t | u_1..t)", is_capstone=False)

    # COLUMN 2: STAGE 2 — PERSONALIZE (RQ2 + PILLARS 3 & 4)
    C2_X, C2_W = 3.70, 2.85
    _add_analysis_block(
        C2_X, R1_Y, C2_W, ROW_H,
        "[BUILT: RQ2] Personalize Style & Pacing",
        [
            "• <b>Method:</b> Archetype-Partitioned FAISS (`k=3`) + `[SLOT]` Masking + Pacing Directive.",
            "• <b>Addressed Params:</b> Persona word norms (`12.9w` / `18.6w` / `14.8w`), discourse style.",
            "• <b>Proven Result:</b> Style `.597` (`+31.8%`, `p < .001`) & `3.87w` pacing error (`p = .007`).",
        ],
        is_capstone=True,
    )
    _add_vert_connector(C2_X + 0.90, R1_Y + ROW_H, "Firms Up: Single-Stage → 6 Call Stages")

    _add_analysis_block(
        C2_X, R2_Y, C2_W, ROW_H,
        "[TO DO: P3] Enterprise Call Stages (a–f)",
        [
            "• <b>Gap Addressed:</b> Real sales calls progress across 6 stages (`3 × 6 = 18` FAISS cells).",
            "• <b>Stage Params:</b> <b>(a)</b> Opening → <b>(b)</b> Mandatory Slots → <b>(c)</b> Positioning → <b>(d)</b> Negotiation → <b>(e)</b> Compliance → <b>(f)</b> Closure (`Hot/Warm/Cold` Lead).",
        ],
        is_capstone=False,
    )
    _add_vert_connector(C2_X + 0.90, R2_Y + ROW_H, "Firms Up: 4 Options → 200-Pkg USP Tree")

    _add_analysis_block(
        C2_X, R3_Y, C2_W, ROW_H,
        "[TO DO: P4] 200-Package USP Catalog Tree",
        [
            "• <b>Gap Addressed:</b> Mandatory slots still match `200+` regional packages.",
            "• <b>Narrowing Params:</b> Info-Gain question tree over `seniors`, `children`, `breakfast`, `sightseeing tempo`, `occasion` matched to <b>Package USPs</b>.",
        ],
        is_capstone=False,
    )

    # ARROWS 2 -> 3
    A2_X, A2_W = 6.57, 0.76
    _add_labeled_arrow(A2_X, R1_Y + 0.15, A2_W, ROW_H - 0.2, "RQ2 → RQ3/4", "Style (.597) + [SLOT] Mask", is_capstone=True)
    _add_labeled_arrow(A2_X, R2_Y + 0.15, A2_W, ROW_H - 0.2, "P3 Output", "Stage (a–f) Gate + Lead Trigger", is_capstone=False)
    _add_labeled_arrow(A2_X, R3_Y + 0.15, A2_W, ROW_H - 0.2, "P4 Output", "Top 1–2 USP Package Match", is_capstone=False)

    # COLUMN 3: STAGES 3 & 4 — GOVERN & OPTIMIZE (RQ3, RQ4 + PILLARS 5 & 6)
    C3_X, C3_W = 7.35, 2.73
    _add_analysis_block(
        C3_X, R1_Y, C3_W, ROW_H,
        "[BUILT: RQ3] Govern Policy & Zero Leakage",
        [
            "• <b>Method:</b> Declarative `YAML` Rule Engine + Post-Gen Entity Sanitizer.",
            "• <b>Addressed Params:</b> `visa ≥ 15d`, `passport ≥ 6m`, `FIT ≤ 4`, `discount ≤ 15%`, `budget ≥ $500`.",
            "• <b>Proven Result:</b> `0.0%` leakage (`F = 34.82`) & `98.6%` rule enforcement (`κ = .917`).",
        ],
        is_capstone=True,
    )
    _add_vert_connector(C3_X + 0.85, R1_Y + ROW_H, "Verified Slots Feed Turn Ledger")

    _add_analysis_block(
        C3_X, R2_Y, C3_W, ROW_H,
        "[BUILT: RQ4] Optimize Turn Economy & Ledger",
        [
            "• <b>Method:</b> Verified Informed Slot Ledger + Persona Package Trade-Off Framing.",
            "• <b>Addressed Params:</b> `Informed` vs. `Missing` slots + `Option A/B/D` trade-off pitch.",
            "• <b>Proven Result:</b> `−29.5%..−42.7%` turns (`F = 664.43`), `RER .109 → .000`.",
        ],
        is_capstone=True,
    )
    _add_vert_connector(C3_X + 0.85, R2_Y + ROW_H, "Firms Up: Cosine → Turn-Q DB & RLHC")

    _add_analysis_block(
        C3_X, R3_Y, C3_W, ROW_H,
        "[TO DO: P5–6] Turn-Q DB, Ablation & RLHC",
        [
            "• <b>Gap Addressed:</b> Backward cosine ignores remaining turns to quote; simulator vs. live humans.",
            "• <b>New Method:</b> Historical <b>Turn-Economy DB (`DTQ`)</b> + `5-Arm (A–E)` prompt ablation + Constrained Offline RL (`CMDP`).",
        ],
        is_capstone=False,
    )

    # ARROWS 3 -> 4
    A3_X, A3_W = 10.10, 0.68
    _add_labeled_arrow(A3_X, R1_Y + 0.15, A3_W, ROW_H - 0.2, "RQ3 Output", "0.0% Leak & 98.6% Guard", is_capstone=True)
    _add_labeled_arrow(A3_X, R2_Y + 0.15, A3_W, ROW_H - 0.2, "RQ4 Output", "−30..43% Turns & .000 RER", is_capstone=True)
    _add_labeled_arrow(A3_X, R3_Y + 0.15, A3_W, ROW_H - 0.2, "P5–6 Output", "Min-DTQ Action + Lead Score", is_capstone=False)

    # COLUMN 4: TARGET ENTERPRISE SYSTEM HUB
    G_X, G_Y, G_W, G_H = 10.80, 1.80, 2.28, 4.78
    goal_card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(G_X), Inches(G_Y), Inches(G_W), Inches(G_H))
    goal_card.adjustments[0] = 0.03
    goal_card.fill.solid()
    goal_card.fill.fore_color.rgb = GOAL_BG
    goal_card.line.color.rgb = GOAL_BORDER
    goal_card.line.width = Pt(2.0)

    goal_hdr = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(G_X), Inches(G_Y), Inches(G_W), Inches(0.54))
    goal_hdr.adjustments[0] = 0.03
    goal_hdr.fill.solid()
    goal_hdr.fill.fore_color.rgb = GOAL_HDR
    goal_hdr.line.fill.background()
    tf_gh = goal_hdr.text_frame
    tf_gh.word_wrap = True
    tf_gh.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_gh = tf_gh.paragraphs[0]
    p_gh.alignment = PP_ALIGN.CENTER
    _add_formatted_runs(p_gh, "FIRMED-UP ENTERPRISE\nCONVERSATIONAL AI", font_size=9.2, color=WHITE, bold=True)

    goal_items = [
        ("1. Identify (RQ1 + P1–P2)", "Tracks `C × K` regimes & live Bayesian persona drift."),
        ("2. Personalize (RQ2 + P3)", "Adapts style & pacing across call stages `a → f`."),
        ("3. Narrow (P4 USP Tree)", "Narrows `200+` packages to `1–2` via USP info-gain."),
        ("4. Govern (RQ3 Guard)", "Enforces `0.0%` entity leakage & `98.6%` policy compliance."),
        ("5. Optimize (RQ4 + P5–P6)", "Combines Slot Ledger + `Turn-Q DB` + `Hot/Warm/Cold` lead."),
    ]
    cur_gy = G_Y + 0.62
    for g_title, g_desc in goal_items:
        sub = s.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(G_X + 0.08), Inches(cur_gy), Inches(G_W - 0.16), Inches(0.76)
        )
        sub.adjustments[0] = 0.06
        sub.fill.solid()
        sub.fill.fore_color.rgb = WHITE
        sub.line.color.rgb = GOAL_BORDER
        sub.line.width = Pt(1.0)
        tf_s = sub.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_right = Inches(0.06)
        tf_s.margin_top = tf_s.margin_bottom = Inches(0.03)
        p_st = tf_s.paragraphs[0]
        _add_formatted_runs(p_st, g_title, font_size=7.8, color=GOAL_HDR, bold=True)
        p_sd = tf_s.add_paragraph()
        p_sd.space_before = Pt(1.5)
        _add_formatted_runs(p_sd, g_desc, font_size=7.1, color=DARK)
        cur_gy += 0.81

    D.add_callout(
        s, 0.25, 6.64, 12.83, 0.52,
        "<b>How the Storyline Is Firmed Up:</b> The <b>Teal Blocks (RQ1–RQ4)</b> establish the proven 4-stage foundation (`Identify → Personalize → Govern → Optimize`, all <i>p</i> < .001), while the <b>Amber Blocks (Pillars 1–6)</b> show the exact architectural additions needed to scale from 4 simulated package options to 200+ live enterprise packages across call stages `a–f`.",
        bg_color=CALLOUT_BG, border_color=NAVY, font_size=8.5,
    )

    # =========================================================================
    # SLIDE 27 (CONDENSED SLIDE 48 — PURE DATA FLOW DIAGRAM WITHOUT CHESS JARGON)
    # =========================================================================
    s = D.content_slide(
        "7. Firming Up the Storyline: Cosine + Turn-Economy Data Flow",
        "Data Flow Diagram: Upgrading Cosine Retrieval (RQ2) with a Turn-Economy & USP Database",
        "Pictorial block and data-flow architecture showing how an additional Turn-Economy Database (Turn-Q DB) & USP Index enhance cosine similarity",
        notes=(
            "Presents the methodology from Slide 48 as a clean engineering Block and Data Flow Diagram (DFD) without chess analogies, "
            "using the same Teal (Built in Capstone) vs. Amber/Coral (New Database & Scorer Addition) vs. Emerald (Target Output) color coding."
        ),
    )

    # Top Legend Strip (y = 1.43, h = 0.28)
    _add_legend_pill(
        0.25, 4.15, CAP_BG, CAP_HDR, CAP_BORDER,
        "BUILT IN CAPSTONE (RQ1–RQ4)",
        "Existing Prefix Router, FAISS Cosine Index, Rule Engine & Slot Ledger",
    )
    _add_legend_pill(
        4.48, 4.55, DOC_BG, DOC_HDR, DOC_BORDER,
        "NEW DATA STORE & SCORER",
        "Historical Turn-Economy DB (Turn-Q DB), 200-Pkg USP Index & Composite Scorer",
    )
    _add_legend_pill(
        9.11, 3.97, GOAL_BG, GOAL_HDR, GOAL_BORDER,
        "OPTIMIZED TURN OUTPUT",
        "Minimum-Turn Package Quotation + Hot/Warm/Cold Lead Score",
    )

    # LEFT PANEL (x = 0.25, w = 3.85, y = 1.80, h = 4.74): Problem & Composite Formula
    D.add_card(
        s, 0.25, 1.80, 3.85, 2.28,
        title="1. Why Pure Cosine Distance (RQ2) Needs an Additional Database",
        header_bg=CAP_HDR,
        bg_color=CAP_BG,
        border_color=CAP_BORDER,
        bullets=[
            "<b>What Capstone RQ2 Cosine Does Well:</b>",
            (1, "FAISS retrieves top-3 exemplars via <b>context cosine similarity `cos(q_t, e_j)`</b>—capturing <i>how to phrase</i> the reply (`.597` style cosine, `3.87w` pacing error)."),
            "<b>The Limitation of Cosine Alone:</b>",
            (1, "Cosine distance only looks <b>backward at text similarity</b>; it is blind to <b>forward turn economy</b>!"),
            (1, "Two past wizard replies may both have `cos = .82`, yet Action A took <b>9 more turns</b> to reach a quote while Action B closed the quote in <b>1 turn</b>."),
        ],
        font_size=8.1,
        title_size=9.0,
        bullet_spacing=2,
    )

    D.add_card(
        s, 0.25, 4.18, 3.85, 2.36,
        title="2. The Upgrade: Composite Cosine + Turn-Economy Scoring",
        header_bg=DOC_HDR,
        bg_color=DOC_BG,
        border_color=DOC_BORDER,
        bullets=[
            "<b>Augmenting FAISS with a Turn-Economy Database (`Turn-Q DB`):</b>",
            (1, "Every historical dialogue turn `(State S_t, Action A_j)` inside Cluster `(C × K)` is indexed with its empirical outcome metrics:"),
            (2, "• <b>`DTQ(S_t, A_j)`:</b> Expected remaining turns to quotation."),
            (2, "• <b>`Q*(S_t, A_j)`:</b> Quotation agreement probability `[0, 1]`."),
            (2, "• <b>`IG_USP(A_j)`:</b> Package catalog reduction (`200 → |P_t|`)."),
            "<b>Composite Retrieval & Action Score:</b>\n"
            "  <b>`Score = α·cos(q_t, e_j) + β·Q*(S_t, A_j) − γ·DTQ(S_t, A_j) + δ·IG_USP`</b>",
        ],
        font_size=8.0,
        title_size=9.0,
        bullet_spacing=2,
    )

    # RIGHT PANEL (x = 4.22, w = 8.86, y = 1.80, h = 4.74): Block & Data Flow Diagram (DFD)
    dfd_bg = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.22), Inches(1.80), Inches(8.86), Inches(4.74))
    dfd_bg.adjustments[0] = 0.02
    dfd_bg.fill.solid()
    dfd_bg.fill.fore_color.rgb = RGBColor(244, 247, 251)
    dfd_bg.line.color.rgb = NAVY
    dfd_bg.line.width = Pt(1.5)

    dfd_hdr = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.22), Inches(1.80), Inches(8.86), Inches(0.32))
    dfd_hdr.adjustments[0] = 0.02
    dfd_hdr.fill.solid()
    dfd_hdr.fill.fore_color.rgb = NAVY
    dfd_hdr.line.fill.background()
    p_dh = dfd_hdr.text_frame.paragraphs[0]
    p_dh.alignment = PP_ALIGN.CENTER
    _add_formatted_runs(
        p_dh,
        "END-TO-END DATA FLOW DIAGRAM (DFD): COSINE FAISS INDEX + HISTORICAL TURN-ECONOMY & USP DATABASES",
        font_size=8.5,
        color=WHITE,
        bold=True,
    )

    # Helper to draw a DFD block on the right canvas
    def _draw_dfd_node(left, top, width, height, badge, title, bullets, bg_c, hdr_c, bdr_c):
        box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        box.adjustments[0] = 0.04
        box.fill.solid()
        box.fill.fore_color.rgb = bg_c
        box.line.color.rgb = bdr_c
        box.line.width = Pt(1.4)

        bh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(0.26))
        bh.adjustments[0] = 0.04
        bh.fill.solid()
        bh.fill.fore_color.rgb = hdr_c
        bh.line.fill.background()
        p_b = bh.text_frame.paragraphs[0]
        p_b.alignment = PP_ALIGN.CENTER
        _add_formatted_runs(p_b, f"{badge} {title}", font_size=7.9, color=WHITE, bold=True)

        tb = s.shapes.add_textbox(Inches(left + 0.06), Inches(top + 0.28), Inches(width - 0.12), Inches(height - 0.30))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0.01)
        for i, b_txt in enumerate(bullets):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.space_after = Pt(1.2)
            _add_formatted_runs(p, b_txt, font_size=7.2, color=DARK)

    # TOP ROW OF DFD: THREE PARALLEL DATA STORES (y = 2.20, h = 1.42)
    # Store 1 (Teal - Built in RQ2): Partitioned FAISS Cosine Vector Index
    _draw_dfd_node(
        4.35, 2.20, 2.72, 1.42,
        "[DATA STORE 1: BUILT RQ2]",
        "Partitioned FAISS Vector DB",
        [
            "• <b>Indexed By:</b> Archetype `(k = 3)` → upgraded to `(C × K × Stage a–f)`.",
            "• <b>Query Signal:</b> Cosine similarity `cos(q_t, e_j)` on prefix embeddings.",
            "• <b>Provides:</b> Top `[SLOT]`-masked style templates (`HOW` to phrase).",
        ],
        CAP_BG, CAP_HDR, CAP_BORDER,
    )

    # Store 2 (Amber - New Addition): Historical Turn-Economy Database (Turn-Q DB)
    _draw_dfd_node(
        7.29, 2.20, 2.72, 1.42,
        "[DATA STORE 2: NEW DB]",
        "Historical Turn-Economy DB",
        [
            "• <b>Indexed By:</b> Symbolic State `S_t = (Cluster, Stage, Slot Bitmask, Conflict)`.",
            "• <b>Stored Metrics per Action `A_j`:</b>\n  ▪ Remaining turns `DTQ = E[T_quote − t]`\n  ▪ Quote win rate `Q*(S_t, A_j)`",
            "• <b>Provides:</b> Shortest path to quote!",
        ],
        DOC_BG, DOC_HDR, DOC_BORDER,
    )

    # Store 3 (Amber - New Addition): 200-Package USP Knowledge Database
    _draw_dfd_node(
        10.23, 2.20, 2.72, 1.42,
        "[DATA STORE 3: NEW DB]",
        "200-Package USP Catalog DB",
        [
            "• <b>Indexed By:</b> Destination, Window, Budget + Micro-Qualifiers (`Senior, Child, Breakfast, Tempo, Occasion`).",
            "• <b>Query Signal:</b> Info-Gain `IG_USP(A_j)` (`Δ|P_t|` packages narrowed).",
            "• <b>Provides:</b> Top 1–2 USP pitches.",
        ],
        DOC_BG, DOC_HDR, DOC_BORDER,
    )

    # Downward Data Flow Arrows from the 3 Data Stores into the Runtime Pipeline (y = 3.65)
    for store_cx, lbl in [
        (5.71, "cos(q_t, e_j)\nStyle Vectors"),
        (8.65, "DTQ & Q*(S_t, A_j)\nTurn Economy"),
        (11.59, "IG_USP & Top Pkgs\nCatalog Fit"),
    ]:
        da = s.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(store_cx - 0.12), Inches(3.65), Inches(0.24), Inches(0.28))
        da.fill.solid()
        da.fill.fore_color.rgb = TEAL if store_cx < 6.5 else DOC_HDR
        da.line.color.rgb = NAVY if store_cx < 6.5 else GOLD
        da.line.width = Pt(0.8)
        tb_l = s.shapes.add_textbox(Inches(store_cx + 0.14), Inches(3.63), Inches(1.25), Inches(0.32))
        tf_l = tb_l.text_frame
        tf_l.word_wrap = True
        tf_l.margin_left = tf_l.margin_top = Inches(0)
        _add_formatted_runs(tf_l.paragraphs[0], lbl, font_size=6.6, color=DARK, bold=True)

    # BOTTOM ROW OF DFD: 4-STAGE RUNTIME PROCESSING FLOW (y = 3.98, h = 2.42)
    # Process 1 (Teal + Amber): Live State & Cluster Router
    _draw_dfd_node(
        4.35, 3.98, 1.98, 2.42,
        "[STEP 1: IDENTIFY]",
        "State & Cluster Router",
        [
            "• <b>Built (`RQ1 + RQ4`):</b>\n  `Blocks` Router (`κ=.958`) + Verified Slot Ledger (`Known: 7/9`, `Missing: {Senior, Breakfast}`).",
            "• <b>Extended (`P1–P3`):</b>\n  Assigns `(Family, Economy, Rigid)` + `Stage d` + `|P_t| = 38 pkgs`.",
        ],
        CAP_BG, CAP_HDR, CAP_BORDER,
    )

    # Arrow Step 1 -> Step 2
    a_12 = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(6.35), Inches(5.05), Inches(0.22), Inches(0.24))
    a_12.fill.solid()
    a_12.fill.fore_color.rgb = NAVY
    a_12.line.fill.background()

    # Process 2 (Amber): Composite Cosine + Turn-Q Action Ranker
    _draw_dfd_node(
        6.59, 3.98, 2.38, 2.42,
        "[STEP 2: SCORE & RANK]",
        "Cosine + Turn-Q Scorer",
        [
            "• <b>Evaluates Candidate Actions:</b>",
            "  ▪ `A1 (Ask Sightseeing)`: `cos=.81`, `|P_t|: 38→31`, <b>`DTQ = 5.4t` (Slow ✗)</b>",
            "  ▪ `A2 (Ask Senior Only)`: `cos=.82`, `|P_t|: 38→14`, <b>`DTQ = 3.1t`</b>",
            "  ▪ <b>`A3* (Bundle Ask Senior+Bkfst + Pitch 4★ vs 5★ +3d)`:</b> `cos=.84`, `|P_t|: 38→2`, `Q*=.94`, <b>`DTQ = 1.0t` (Selected ✓)</b>",
        ],
        DOC_BG, DOC_HDR, DOC_BORDER,
    )

    # Arrow Step 2 -> Step 3
    a_23 = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(8.99), Inches(5.05), Inches(0.22), Inches(0.24))
    a_23.fill.solid()
    a_23.fill.fore_color.rgb = DOC_HDR
    a_23.line.fill.background()

    # Process 3 (Teal): Governed Generator & Symbolic Rule Verifier
    _draw_dfd_node(
        9.23, 3.98, 1.88, 2.42,
        "[STEP 3: GOVERN]",
        "Rule & Style Synthesis",
        [
            "• <b>WHAT to Execute:</b>\n  Winning Action `A3*` (`DTQ = 1.0t`) + Package USPs.",
            "• <b>HOW to Phrase (`RQ2`):</b>\n  Top-3 `[SLOT]`-masked exemplars (`14.8w` norm).",
            "• <b>Policy Guard (`RQ3/4`):</b>\n  `0.0%` leakage, `5 YAML` rules, `0.0%` repeat asks.",
        ],
        CAP_BG, CAP_HDR, CAP_BORDER,
    )

    # Arrow Step 3 -> Step 4
    a_34 = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(11.13), Inches(5.05), Inches(0.22), Inches(0.24))
    a_34.fill.solid()
    a_34.fill.fore_color.rgb = GREEN
    a_34.line.fill.background()

    # Process 4 (Emerald): Terminal Quotation & Lead Output
    _draw_dfd_node(
        11.37, 3.98, 1.58, 2.42,
        "[STEP 4: OPTIMIZE]",
        "Quotation & Lead",
        [
            "• <b>Catalog Narrowed:</b>\n  `200 → Top 2` USP-fit packages in 1 turn.",
            "• <b>Stage (f) Closure:</b>\n  Customer agrees to formal quotation.",
            "• <b>CRM Output:</b>\n  Scored as `Hot / Warm / Cold` Lead.",
        ],
        GOAL_BG, GOAL_HDR, GOAL_BORDER,
    )

    D.add_callout(
        s, 0.25, 6.62, 12.83, 0.54,
        "<b>Data Flow Takeaway:</b> In the firmed-up architecture, <b>FAISS Cosine Similarity (`Data Store 1`, Teal)</b> governs <i>stylistic phrasing</i>, while the <b>Historical Turn-Economy Database (`Data Store 2`, Amber)</b> and <b>200-Package USP Database (`Data Store 3`, Amber)</b> govern <i>next-action selection (`A3*`)</i>—ensuring every agent turn simultaneously matches customer style and minimizes remaining turns to quotation.",
        bg_color=CALLOUT_BG, border_color=NAVY, font_size=8.4,
    )

    # =========================================================================
    # SLIDE 28: CONCLUDING SUMMARY & OPEN FLOOR (WITH POINTER TO BACKUP DECKS)
    # =========================================================================
    s = D.content_slide(
        "8. Conclusion & Defense Open Floor",
        "Concluding Summary, Reproducibility Inventory & Open Floor",
        "A complete, reproducible neuro-symbolic blueprint validated across Identify (RQ1) → Personalize (RQ2) → Govern (RQ3) → Optimize (RQ4)",
        notes="Final summary slide to leave on screen during committee Q&A. Point to the 48-slide Full Defense Deck and 19-slide Methodology Reference Deck if deep mathematical or Q&A backup slides are requested.",
    )
    D.add_card(
        s, 0.35, 1.50, 6.15, 4.30,
        title="Four-Stage Storyline Summary (All H01–H04 Rejected at p < .001)",
        header_bg=NAVY,
        bullets=[
            "<b>1. IDENTIFY (RQ1 — Early Archetype Routing):</b> Truncating to the first `M = 9` user messages and combining Gemini embeddings with 16 LLM behavioral ratings (`Blocks`) yields 3 stable archetypes (<b>ARI = .89 / .87</b>) and raises held-out prefix routing from κ = .24 to <b>κ = .535 (M=5) and κ = .958 (M=9, 97.3%)</b>.",
            "<b>2. PERSONALIZE (RQ2 — Style & Pacing ICL):</b> Contrasting Primary (<i>p</i> = .211) vs. Refined (<b>F = 9.79, p < .001, ηp² = .234</b>) archetypes proves that `[SLOT]`-masked FAISS retrieval + directives boost style convergence (+31.8% over static, <i>d<sub>z</sub></i> = 0.74) and cut pacing error to <b>3.87 words</b>.",
            "<b>3. GOVERN (RQ3 — Symbolic Policy & Leakage Guard):</b> Declarative `YAML` rule verification eliminates the <b>35.9% entity leakage</b> of unguarded few-shot prompting down to <b>0.0% (Interaction F = 34.82, p < .001)</b> while raising violation enforcement from <b>5.6% to 98.6%</b> and Slot F1 to <b>.952</b> (Dual-judge <b>κ = .917</b>).",
            "<b>4. OPTIMIZE (RQ4 — Multi-Turn Turn Economy):</b> Governed cluster-adaptive prompting + Verified Informed Slot Ledger compress multi-turn sessions by <b>29.5% to 42.7%</b> (<i>F</i> = 664.43, Interaction <i>F</i> = 10.89, <i>p</i> < .001) and eliminate redundant slot questions (<b>RER .109 → .000</b>; Persona <b>κ = .933</b>).",
        ],
        font_size=9.8,
    )
    D.add_card(
        s, 6.80, 1.50, 6.18, 4.30,
        title="Reproducibility & Companion Deep-Dive Backup Decks",
        header_bg=TEAL,
        bullets=[
            f"<b>GitHub Repository:</b> {REPO}",
            "<b>Complete Deliverable Suite (`final/`):</b>",
            (1, "<b>1. 15-Minute Executive Defense Deck (This Presentation — 28 Slides):</b> Streamlined storyline (`Identify → Personalize → Govern → Optimize`) & DFD roadmap."),
            (1, "<b>2. Comprehensive Defense Deck (`QM_640_Defense_Presentation_Sandeep_Surnella.pptx` — 48 Slides):</b> Includes full ground-up primers, Welch/HC3/ART triangulation tables, counterfactual parameter proofs, and 11 prepared Defense Q&A slides."),
            (1, "<b>3. Text-to-ANOVA Methodology Reference (`QM_640_RQ_Text_to_ANOVA_Methodology_Reference.pptx` — 19 Slides):</b> Step-by-step mathematical derivations from raw text to F-ratios and noncentral-F power curves."),
            (1, "<b>4. Final Report (`QM_640_Final_Report_Sandeep_Surnella.docx` & `.pdf`):</b> Complete manuscript, 5 executed notebooks, and 100% cached JSONL outputs."),
        ],
        font_size=9.8,
    )
    D.add_callout(
        s, 0.35, 5.95, 12.63, 1.10,
        "<b>Thank You — Open Floor for Defense Committee Questions</b>\n"
        "<i>Surnella Sandeep  |  Department of Data Analytics, Walsh College  |  QM640: Data Analytics Capstone  |  Mentor: Mr. Smitraj Raut</i>",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=13,
    )

