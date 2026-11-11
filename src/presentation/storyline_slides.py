"""
Reusable 4-Stage Solution Approach (`Identify -> Personalize -> Govern -> Optimize`) Progression Slides
and Pictorial Methodology Blueprint Slide using native Microsoft PowerPoint Shapes (`MSO_SHAPE`).

Implements:
  1. `add_storyline_discovery_slide(D, stage_step)`:
     Renders the 5 progressive appearances of the 4-Stage Solution Approach across the presentation:
       - stage_step = 0 (Appearance 1, immediately after Problem Statement): Conceptual thought process (no empirical findings yet)
       - stage_step = 1 (Appearance 2, end of RQ1-Identify / RQ1 — Identify)
       - stage_step = 2 (Appearance 3, end of RQ2-Personalize / RQ2 — Personalize)
       - stage_step = 3 (Appearance 4, end of RQ3-Govern / RQ3 — Govern)
       - stage_step = 4 (Appearance 5, end of RQ4-Optimize / RQ4 — Optimize: Complete Validated Solution Cascade)
  2. `add_pictorial_methodology_slide(D)`:
     Renders the purely methodological pictorial diagram of IVs (X), DVs (Y), Parametric Tests,
     Bullet-Proofing Robustness Checks (Welch/HC3 + Non-Parametric ART/Friedman/Kruskal), and
     Expected Findings across all four stages (with zero post-hoc empirical results).
"""

from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt
from presentation.ppt_styles import (
    BLUE,
    BORDER_GRAY,
    CALLOUT_BG,
    CARD_ALT,
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


def add_storyline_discovery_slide(D, stage_step=0):
    """
    Render one of the 5 progressive appearances of the 4-stage solution approach diagram.
    """
    # =========================================================================
    # APPEARANCE 1 (stage_step == 0): CONCEPTUAL THOUGHT PROCESS (NO EMPIRICAL NUMBERS)
    # =========================================================================
    if stage_step == 0:
        return D.add_storyline_state_slide(
            module_label="1. Conceptual 4-Stage Solution Approach (Appearance 1 of 5)",
            title="Four-Stage Solution Approach: Identify → Personalize → Govern → Optimize",
            subtitle="Conceptual thought process: How clustering, in-context style adaptation, symbolic rules, and slot ledgers cascade into one architecture",
            stages_data=[
                {
                    "stage_title": "RQ1-IDENTIFY",
                    "stage_subtitle": "Clustering Methodology & Early Routing",
                    "header_color": NAVY,
                    "border_color": NAVY,
                    "bg_color": WHITE,
                    "input_text": "<b>Conceptual Goal:</b> Discover how travelers shop from opening turns without leaking end-of-chat outcomes.",
                    "circles": [
                        {
                            "status": "blue",
                            "title": "1a. Evaluate Clustering Algorithms",
                            "body": "Test centroid (`K-Means`), hierarchical (`Ward`), and density (`HDBSCAN`) clustering for 100% customer coverage.",
                        },
                        {
                            "status": "orange",
                            "title": "1b. Audit Whole-Chat vs. Prefix",
                            "body": "Whole-chat vectors risk outcome & agent confounding; test opening user prefixes + behavioral ratings (`Blocks`).",
                        },
                        {
                            "status": "green",
                            "title": "1c. Target RQ1-Identify Output",
                            "body": "Isolate stable traveler personas, train an early prefix router, and build 1 FAISS index per persona.",
                        },
                    ],
                    "connectors": [
                        "Check coverage, stability & confounding",
                        "Fit early prefix router & FAISS pools",
                    ],
                    "handoff_status": "green",
                    "handoff_text": "<b>PASS TO RQ2-PERSONALIZE ➔</b>\nValidated Traveler Personas + Live Prefix Router + Persona-Partitioned FAISS Indices.",
                },
                {
                    "stage_title": "RQ2-PERSONALIZE",
                    "stage_subtitle": "Cluster-Adaptive Style & Pacing ICL",
                    "header_color": TEAL,
                    "border_color": TEAL,
                    "bg_color": WHITE,
                    "input_text": "<b>Conceptual Goal:</b> Use RQ1-Identify clusters in the LLM to prove clustering improves style & pacing.",
                    "circles": [
                        {
                            "status": "red",
                            "title": "2a. Unrouted Static / Zero-Shot",
                            "body": "One-size-fits-all prompts and unrouted examples mismatch user verbosity and decision style.",
                        },
                        {
                            "status": "green",
                            "title": "2b. Cluster-Adaptive Few-Shot",
                            "body": "Route user prefix to matched FAISS pool + persona pacing directive to improve style & word calibration.",
                        },
                        {
                            "status": "orange",
                            "title": "2c. Gap: Lacks Rule Capability!",
                            "body": "Style adaptation alone cannot enforce numeric booking rules and risks leaking stale exemplar entities!",
                        },
                    ],
                    "connectors": [
                        "Route via RQ1-Identify into persona FAISS",
                        "Audit replies for policy & entity safety",
                    ],
                    "handoff_status": "orange",
                    "handoff_text": "<b>PASS TO RQ3-GOVERN ➔</b>\nProven Cluster-Adaptive Style Engine (<b>Green</b>) + Unresolved Policy/Leakage Risk (<b>Orange</b>).",
                },
                {
                    "stage_title": "RQ3-GOVERN",
                    "stage_subtitle": "Mixing Symbolic Rules + Adaptive Style",
                    "header_color": CORAL,
                    "border_color": CORAL,
                    "bg_color": WHITE,
                    "input_text": "<b>Conceptual Goal:</b> Prove rules bring accuracy while lacking style, then mix both for rules + style.",
                    "circles": [
                        {
                            "status": "red",
                            "title": "3a. Style Only (Rules Off)",
                            "body": "Unguarded few-shot copies stale hotel/price terms from examples and misses arithmetic policy thresholds.",
                        },
                        {
                            "status": "orange",
                            "title": "3b. Rules Only (Zero-Shot + Rules)",
                            "body": "Deterministic `YAML` rules bring high policy accuracy & zero leakage, but lack persona-adapted style.",
                        },
                        {
                            "status": "green",
                            "title": "3c. Mix Both: Rules + Style!",
                            "body": "Combine `[SLOT]` masking + `YAML` Rule Engine + Cluster-Adaptive ICL for best of rules AND style.",
                        },
                    ],
                    "connectors": [
                        "Contrast Rules Off vs. Rules Active",
                        "Synthesize Neuro-Symbolic Cell 4",
                    ],
                    "handoff_status": "green",
                    "handoff_text": "<b>PASS TO RQ4-OPTIMIZE ➔</b>\nGoverned Neuro-Symbolic Stack (`Rules Active × Cluster-Adaptive` + `[SLOT]` Masking).",
                },
                {
                    "stage_title": "RQ4-OPTIMIZE",
                    "stage_subtitle": "Multi-Turn Economy & Zero RER",
                    "header_color": GREEN,
                    "border_color": GREEN,
                    "bg_color": WHITE,
                    "input_text": "<b>Conceptual Goal:</b> Put RQ1-Identify to RQ3-Govern together with a Slot Ledger to compress turns to quotation.",
                    "circles": [
                        {
                            "status": "red",
                            "title": "4a. Memoryless Sequential Policy",
                            "body": "Re-asks already stated slots (high `RER`) and offers 1 option at a time, causing multi-turn deadlocks.",
                        },
                        {
                            "status": "green",
                            "title": "4b. Verified Informed Slot Ledger",
                            "body": "Track known vs. missing slots deterministically so the agent never re-asks stated user constraints (`RER = 0`).",
                        },
                        {
                            "status": "green",
                            "title": "4c. Persona Package Policies",
                            "body": "Pair 1-Option Confirm, 3-Option Compare, and Dual Trade-Off framing to compress total turns to quote.",
                        },
                    ],
                    "connectors": [
                        "Lock stated slots across turns",
                        "Match package framing to persona",
                    ],
                    "handoff_status": "green",
                    "handoff_text": "<b>TARGET OUTCOME ➔</b>\nPareto-Optimal Turn Economy & Zero Redundant Elicitation Across All Personas.",
                },
            ],
            handoff_arrows=[
                {"active": True, "top_label": "RQ1 → RQ2", "bottom_label": "3 Personas +\nRouter +\n3 FAISS DBs"},
                {"active": True, "top_label": "RQ2 → RQ3", "bottom_label": "Adaptive Style\n(Green) +\nRule Gap (Orange)"},
                {"active": True, "top_label": "RQ3 → RQ4", "bottom_label": "Governed Style\n+ [SLOT] Mask\n+ YAML Rules"},
            ],
            bottom_callout=(
                "<b>Solution Approach Blueprint (Appearance 1 of 5 — Conceptual Thought Process):</b> "
                "Rather than treating clustering, prompting, guardrails, and dialogue efficiency as isolated problems, this study links them into a single causal chain: "
                "<b>RQ1-Identify Stage</b> finds a clustering methodology that is routable from opening turns → "
                "<b>RQ2-Personalize Stage</b> proves those clusters improve LLM style (<b>Green</b>) while exposing rule/leakage vulnerability (<b>Orange</b>) → "
                "<b>RQ3-Govern Stage</b> proves symbolic rules bring accuracy and mixes both (`Rules Active × Cluster-Adaptive`) → "
                "<b>RQ4-Optimize Stage</b> puts all layers together to achieve turn economy and zero redundant questions."
            ),
            notes=(
                "Appearance 1 of the recurring 4-stage solution approach diagram. At this stage (immediately after the Problem Statement), "
                "walk the committee through the conceptual thought process without overwhelming them with empirical numbers yet. "
                "Explain how this exact diagram will reappear at the end of every stage as rounded nodes turn Red (dropped), Orange (needs next stage), or Green (winner carried forward)."
            ),
        )

    # =========================================================================
    # RQ1-IDENTIFY EMPIRICAL DATA (USED IN APPEARANCES 2, 3, 4, 5)
    # =========================================================================
    stage1_empirical = {
        "stage_title": "RQ1-IDENTIFY",
        "stage_subtitle": "Reject H01 (p < .001) — Locked In ✓",
        "header_color": NAVY,
        "border_color": GREEN,
        "bg_color": RGBColor(244, 250, 246),
        "input_text": "<b>Tested on D<sub>gold</sub> (n = 933) & D<sub>test</sub> (n = 401):</b> 159-run algorithm benchmark + Truncation × Modality grid.",
        "circles": [
            {
                "status": "red",
                "title": "CLOSED: HDBSCAN / Ward / Full-Chat",
                "body": "`HDBSCAN` drops `39.1%` noise; `Ward` `.118<.147`; Full-chat confounded by wizard (`V=.45`) & outcome (`κ=.24`).",
            },
            {
                "status": "orange",
                "title": "PARTIAL: Prefix Embeddings Only",
                "body": "Truncated `M=9` Gemini prefix alone gets `ARI = .39` & `κ = .312` (`Δκ = −.223` without LLM scales).",
            },
            {
                "status": "green",
                "title": "WINNER: K-Means (k=3) + 46-d Blocks",
                "body": "`100%` cov. (`F=91.33/127.47`), `ARI=.89/.87`, `η²=.32–.52`, Test Router `κ=.535 (M=5)` & `.958 (97.3%, M=9)`.",
            },
        ],
        "connectors": [
            "ANOVA F=91.33/127.47 (p<.001) + Audit",
            "Join PCA-20 + 13 LLM Fields (DB=2.647)",
        ],
        "handoff_status": "green",
        "handoff_text": "<b>CARRIED TO RQ2-PERSONALIZE ➔</b>\n`3 46-d Blocks Archetypes` + `L1 Router (κ=.535/.958)` + `3 FAISS IndexFlatIP(46) Sub-Indices`.",
    }

    # =========================================================================
    # RQ2-PERSONALIZE EMPIRICAL DATA (USED IN APPEARANCES 3, 4, 5)
    # =========================================================================
    stage2_empirical = {
        "stage_title": "RQ2-PERSONALIZE",
        "stage_subtitle": "Reject H02 (p < .001) — Style Locked ✓",
        "header_color": TEAL,
        "border_color": GREEN,
        "bg_color": RGBColor(244, 250, 246),
        "input_text": "<b>Inherited RQ1-Identify Router & 3 FAISS DBs:</b> Tested on `N = 33` D<sub>test</sub> chats × 3 prompts (`99` evaluations).",
        "circles": [
            {
                "status": "red",
                "title": "CLOSED: Coarse (κ=.24) & Static ICL",
                "body": "Primary clusters failed (`F=1.61, p=.211 Null`); `Static Few-Shot` hurt style (`.453`) & pacing (`6.33w`; Zero `10.12w`).",
            },
            {
                "status": "green",
                "title": "WINNER: Cluster-Adaptive Style",
                "body": "Refined `Blocks` routing lifts style to `.597 (+31.8%, F=9.79, p<.001, ηp²=.234)` & cuts pacing error to `3.87w (p=.007)`.",
            },
            {
                "status": "orange" if stage_step == 2 else "red",
                "title": "GAP: Unguarded Rules & Leakage!" if stage_step == 2 else "PROVEN UNSAFE ALONE IN RQ3-GOVERN",
                "body": (
                    "Solves style, but prompt-only rules & unmasked exemplars risk entity leakage — verify in RQ3-Govern!"
                    if stage_step == 2
                    else "RQ3-Govern proved unguarded `Cluster-Adaptive` leaks entities (`55.6%`) & misses `94.4%` of violations!"
                ),
            },
        ],
        "connectors": [
            "RM-ANOVA F=9.79 (p<.001), d_z=0.74",
            "Check entity leakage & rule compliance",
        ],
        "handoff_status": "orange" if stage_step == 2 else "green",
        "handoff_text": (
            "<b>CARRIED TO RQ3-GOVERN ➔</b>\n`Cluster-Adaptive (k=3 FAISS + Directives)` (<b>Green</b>) + Rule/Leakage Risk (<b>Orange</b>) to verify."
            if stage_step == 2
            else "<b>CARRIED TO RQ3-GOVERN ➔</b>\n`Cluster-Adaptive (k=3 FAISS + Directives)` paired with RQ3-Govern `[SLOT]` Mask & `YAML` Rules."
        ),
    }

    # =========================================================================
    # RQ3-GOVERN EMPIRICAL DATA (USED IN APPEARANCES 4, 5)
    # =========================================================================
    stage3_empirical = {
        "stage_title": "RQ3-GOVERN",
        "stage_subtitle": "Reject H03 (p < .001) — Guard Locked ✓",
        "header_color": CORAL,
        "border_color": GREEN,
        "bg_color": RGBColor(244, 250, 246),
        "input_text": "<b>Inherited RQ1-Identify + RQ2-Personalize Stack:</b> Tested `2 × 2` (`Rules Off/Active × Zero/Adaptive`) on `N = 144` D<sub>test</sub> units (`n=36`/cell).",
        "circles": [
            {
                "status": "red",
                "title": "CLOSED: Rules Off (Unguarded)",
                "body": "RQ2-Personalize Orange path turns <b>RED</b>: `Rules Off × Adaptive` leaks stale entities in `55.6%` (`ELR=.359`) & enforces only `5.6%` of rules!",
            },
            {
                "status": "orange",
                "title": "PARTIAL: Rules Active × Zero-Shot",
                "body": "`YAML RuleEngine` gives `100%` violation sens. & `0.0%` leakage, but lacks persona style (`.428 vs .506, F=24.00`).",
            },
            {
                "status": "green",
                "title": "WINNER: Rules Active × Adaptive",
                "body": "Best of both: `0.0%` leak (`Int. F=34.82`), `98.6%` rule sens. (`F=498.78`), `.952` Slot F1 (`F=489.52`), & `.506` style (`κ=.917`).",
            },
        ],
        "connectors": [
            "Leakage Int. F=34.82, Sens. F=498.78",
            "Mix [SLOT] Mask + 5 YAML Rules + ICL",
        ],
        "handoff_status": "green",
        "handoff_text": "<b>CARRIED TO RQ4-OPTIMIZE ➔</b>\nPareto-Optimal `Rules Active × Cluster-Adaptive` (`[SLOT]` Mask + `5 YAML Rules` + Sanitizer).",
    }

    # =========================================================================
    # RQ4-OPTIMIZE EMPIRICAL DATA (USED IN APPEARANCE 5)
    # =========================================================================
    stage4_empirical = {
        "stage_title": "RQ4-OPTIMIZE",
        "stage_subtitle": "Reject H04 (p < .001) — Full Stack ✓",
        "header_color": GREEN,
        "border_color": GREEN,
        "bg_color": RGBColor(244, 250, 246),
        "input_text": "<b>Inherited RQ1-Identify + RQ2-Personalize + RQ3-Govern Stack:</b> Tested `2 × 3` (`Prompt × 3 Blocks Personas`) on `N = 180` sims (`n=30`/cell, `κ=.933`).",
        "circles": [
            {
                "status": "red",
                "title": "CLOSED: Memoryless Zero-Shot",
                "body": "Sequential 1-option policy without Slot Ledger takes `7.93 turns` (`8.73t` Rigid) & re-asks slots (`RER = .109`; `19.4%` DB).",
            },
            {
                "status": "green",
                "title": "WINNER: Verified Slot Ledger",
                "body": "Locks stated vs. missing constraints across turns, eliminating Redundant Elicitation Rate: `.109 → .000 (0.0%, F=63.02)`.",
            },
            {
                "status": "green",
                "title": "WINNER: Persona Package Policies",
                "body": "Cuts turns `7.93 → 5.09 (−35.8%, F=664.43, ηp²=.793)`: Rigid `−42.7% (8.73→5.00t)`, DB `−34.2%`, OE `−29.5%` (`Int. F=10.89`).",
            },
        ],
        "connectors": [
            "RER ANOVA F=63.02 (p<.001, ηp²=.266)",
            "Log-Turn F=664.43, Int. F=10.89 (p<.001)",
        ],
        "handoff_status": "green",
        "handoff_text": "<b>FINAL VALIDATED SYSTEM ➔</b>\nFull 4-Stage Neuro-Symbolic Engine Deployed + Seeds Doctoral Pillars 1–6 (`Opp_ID`, `Turn-Q DB`).",
    }

    # Pending stage templates for earlier appearances
    stage2_pending = {
        "stage_title": "RQ2-PERSONALIZE",
        "stage_subtitle": "Next Stage to Test (N = 33 × 3 = 99)",
        "header_color": TEAL,
        "border_color": BORDER_GRAY,
        "bg_color": WHITE,
        "input_text": "<b>Receives from RQ1-Identify:</b> `3 46-d Blocks Archetypes`, `L1 Prefix Router (κ=.535)`, & `3 FAISS Sub-Indices`.",
        "circles": [
            {
                "status": "pending",
                "title": "To Test: Coarse vs. Refined Routing",
                "body": "Contrast Primary whole-chat clusters (`κ=.24`) against Refined `46-d Blocks` clusters (`κ=.535`).",
            },
            {
                "status": "pending",
                "title": "To Test: Zero vs. Static vs. Adaptive",
                "body": "Evaluate De-lexicalized SBERT Style Cosine, Gemini 3,072-d Cosine, BERTScore F1, and Pacing Error.",
            },
            {
                "status": "pending",
                "title": "To Audit: Prompt Policy & Leakage",
                "body": "Examine whether style-adapted prompts alone can enforce rules without leaking exemplar entities.",
            },
        ],
        "connectors": ["RM-ANOVA (GG ε) + Friedman χ²", "Holm step-down paired contrasts"],
        "handoff_status": "pending",
        "handoff_text": "<b>AWAITING RQ2-PERSONALIZE TEST ➔</b>\nDetermine if `Cluster-Adaptive` beats `Static` & `Zero-Shot` and check rule/leakage safety.",
    }

    stage3_pending = {
        "stage_title": "RQ3-GOVERN",
        "stage_subtitle": "Upcoming Stage (2 × 2 Factorial, N = 144)",
        "header_color": CORAL,
        "border_color": BORDER_GRAY,
        "bg_color": WHITE,
        "input_text": "<b>Receives from RQ1-Identify & RQ2-Personalize:</b> `46-d Blocks` Router + `Cluster-Adaptive` Prompt + Orange Rule/Leakage Risk.",
        "circles": [
            {
                "status": "pending",
                "title": "To Test: Rules Off vs. Rules Active",
                "body": "Cross `Rules Mode` (`Off` vs. `Active 5 YAML Rules`) with `Prompting` (`Zero-Shot` vs. `Cluster-Adaptive`).",
            },
            {
                "status": "pending",
                "title": "To Test: Violation Sens. & Spec.",
                "body": "Audit 50% violating (`n=18`/cell) & 50% compliant (`n=18`/cell) cases + Dual-Judge `gemini-2.5-pro` (`n=48`).",
            },
            {
                "status": "pending",
                "title": "To Test: Protective Leakage Interaction",
                "body": "Test if `[SLOT]` masking + post-gen sanitization eliminates exemplar entity leakage while keeping style.",
            },
        ],
        "connectors": ["2×2 OLS ANOVA + HC3 + ART", "Orthogonal Sum contrasts"],
        "handoff_status": "pending",
        "handoff_text": "<b>AWAITING RQ3-GOVERN TEST ➔</b>\nVerify whether mixing `Rules Active × Cluster-Adaptive` resolves the RQ2-Personalize safety gap.",
    }

    stage4_pending = {
        "stage_title": "RQ4-OPTIMIZE",
        "stage_subtitle": "Upcoming Stage (2 × 3 Simulation, N = 180)",
        "header_color": GREEN,
        "border_color": BORDER_GRAY,
        "bg_color": WHITE,
        "input_text": "<b>Receives from RQ1-Identify to RQ3-Govern:</b> `3 Blocks Personas` + `[SLOT]` FAISS + Active `YAML RuleEngine`.",
        "circles": [
            {
                "status": "pending",
                "title": "To Test: Zero-Shot vs. Full Stack",
                "body": "Run `N = 180` closed-loop chats (`n=30`/cell) across the 4-option package catalog (`Options A, B, C, D`).",
            },
            {
                "status": "pending",
                "title": "To Test: Verified Slot Ledger (RER)",
                "body": "Measure Redundant Elicitation Rate (`RER`) and validate simulator fidelity via blind `gemini-2.5-pro` (`n=45`).",
            },
            {
                "status": "pending",
                "title": "To Test: Prompt × Persona Interaction",
                "body": "Test Raw & Log Turns (`ln TGC`) across Decisive Booker, Open Explorer, and Rigid-Constraint Seeker.",
            },
        ],
        "connectors": ["2×3 ANOVA on ln(TGC) + HC3 + ART", "Welch t, Mann–Whitney U & Cohen's d"],
        "handoff_status": "pending",
        "handoff_text": "<b>AWAITING RQ4-OPTIMIZE TEST ➔</b>\nQuantify multi-turn compression (`−Δ%` turns) and zero redundant questions (`RER = .000`).",
    }

    # =========================================================================
    # APPEARANCE 2 (stage_step == 1): END OF RQ1-IDENTIFY (IDENTIFY / RQ1)
    # =========================================================================
    if stage_step == 1:
        return D.add_storyline_state_slide(
            module_label="6. RQ1-Identify Synthesis & Solution Handoff (Appearance 2 of 5)",
            title="Four-Stage Solution Update After RQ1-Identify Stage",
            subtitle="RQ1-Identify empirical decisions locked in: What was closed (Red), what was partial (Orange), and what is passed to RQ2-Personalize (Green)",
            stages_data=[stage1_empirical, stage2_pending, stage3_pending, stage4_pending],
            handoff_arrows=[
                {"active": True, "top_label": "RQ1 → RQ2", "bottom_label": "3 Blocks Personas\n+ Router (κ=.535)\n+ 3 FAISS DBs"},
                {"active": False, "top_label": "RQ2 → RQ3", "bottom_label": "Pending\nRQ2-Personalize\nEvaluation"},
                {"active": False, "top_label": "RQ3 → RQ4", "bottom_label": "Pending\nRQ3-Govern\nEvaluation"},
            ],
            bottom_callout=(
                "<b>RQ1-Identify Stage Solution Decision (Appearance 2 of 5):</b> "
                "<b>✗ Closed (Red):</b> `HDBSCAN` (`39.1%` noise loss), `Ward` (`.118 < .147`), whole-dialogue embeddings (`Wizard V = .45, Outcome V = .29, κ = .24`), and audit fields `14–16` are dropped from routing. "
                "<b>! Partial (Orange):</b> Prefix embeddings alone (`ARI = .39, κ = .312`) lack sufficient persona separation. "
                "<b>✓ Carried Forward to RQ2-Personalize (Green):</b> `K-Means (k = 3)` on the `46-d Blocks` prefix space (`M = 9`, `ARI = .89/.87`, `η² = .322–.524`), the `L1 Prefix Router` (`κ = .535` at `M=5`, `κ = .958` at `M=9`), and the `3 Partitioned 46-d FAISS Sub-Indices`."
            ),
            notes=(
                "Appearance 2 of 5 of the recurring 4-stage solution approach diagram, placed at the conclusion of RQ1-Identify. "
                "Point to the Red, Orange, and Green rounded nodes in Column 1 to show exactly what was eliminated and what causal artifacts pass into RQ2-Personalize."
            ),
        )

    # =========================================================================
    # APPEARANCE 3 (stage_step == 2): END OF RQ2-PERSONALIZE (PERSONALIZE / RQ2)
    # =========================================================================
    if stage_step == 2:
        return D.add_storyline_state_slide(
            module_label="7. RQ2-Personalize Synthesis & Solution Handoff (Appearance 3 of 5)",
            title="Four-Stage Solution Update After RQ2-Personalize Stage",
            subtitle="RQ2-Personalize proves clustering improves style & pacing (Green), closes coarse/static prompts (Red), and flags rules/leakage (Orange) for RQ3-Govern",
            stages_data=[stage1_empirical, stage2_empirical, stage3_pending, stage4_pending],
            handoff_arrows=[
                {"active": True, "top_label": "RQ1 → RQ2", "bottom_label": "3 Blocks Personas\n+ Router (κ=.535)\n+ 3 FAISS DBs"},
                {"active": True, "top_label": "RQ2 → RQ3", "bottom_label": "Adaptive Style\n(.597, Green) +\nRule Risk (Orange)"},
                {"active": False, "top_label": "RQ3 → RQ4", "bottom_label": "Pending\nRQ3-Govern\nGovernance"},
            ],
            bottom_callout=(
                "<b>RQ2-Personalize Stage Solution Decision (Appearance 3 of 5):</b> "
                "<b>✗ Closed (Red):</b> Coarse primary clusters (`κ = .24 → F = 1.61, p = .211 Null`), `Static Few-Shot` (`.453` style, `6.33w` error), and `Zero-Shot` (`25.5w`, `10.12w` error) are dropped. "
                "<b>✓ Carried Forward (Green):</b> `Refined Cluster-Adaptive Prompting` (`k = 3` FAISS exemplars from RQ1-Identify's `46-d Blocks` sub-indices + pacing directives) boosts style cosine by `+31.8% (.597, F = 9.79, p < .001)` and cuts pacing error to `3.87 words (p = .007)`. "
                "<b>! Flagged for RQ3-Govern Verification (Orange):</b> Style adaptation alone lacks rule capability and risks copying stale exemplar entities—motivating RQ3-Govern (`GOVERN`)."
            ),
            notes=(
                "Appearance 3 of 5 of the recurring 4-stage solution approach diagram, placed at the conclusion of RQ2-Personalize. "
                "Highlight how Node 2b in RQ2-Personalize is Green (style & pacing proven), while Node 2c is Orange (unguarded prompts lack rule enforcement and leak entities), directly setting up RQ3-Govern."
            ),
        )

    # =========================================================================
    # APPEARANCE 4 (stage_step == 3): END OF RQ3-GOVERN (GOVERN / RQ3)
    # =========================================================================
    if stage_step == 3:
        return D.add_storyline_state_slide(
            module_label="8. RQ3-Govern Synthesis & Solution Handoff (Appearance 4 of 5)",
            title="Four-Stage Solution Update After RQ3-Govern Stage",
            subtitle="RQ3-Govern turns unguarded prompting Red (55.6% leak), proves Rules + Cluster-Adaptive is Pareto-Optimal (Green), and passes to RQ4-Optimize",
            stages_data=[stage1_empirical, stage2_empirical, stage3_empirical, stage4_pending],
            handoff_arrows=[
                {"active": True, "top_label": "RQ1 → RQ2", "bottom_label": "3 Blocks Personas\n+ Router (κ=.535)\n+ 3 FAISS DBs"},
                {"active": True, "top_label": "RQ2 → RQ3", "bottom_label": "Adaptive ICL\nTested in 2×2\nFactorial"},
                {"active": True, "top_label": "RQ3 → RQ4", "bottom_label": "Rules Active ×\nCluster-Adaptive\n([SLOT] + YAML)"},
            ],
            bottom_callout=(
                "<b>RQ3-Govern Stage Solution Decision (Appearance 4 of 5):</b> "
                "<b>✗ Closed (Red):</b> The Orange safety risk from RQ2-Personalize is confirmed lethal when unguarded—`Rules Off × Cluster-Adaptive` leaks stale entities in `55.6%` of replies (`ELR = .359`) and enforces only `5.6%` of rule violations (`Rules Off` is permanently closed). "
                "<b>! Partial (Orange):</b> `Rules Active × Zero-Shot` enforces rules (`100%` sens., `0%` leak) but sacrifices persona style (`.428`). "
                "<b>✓ Carried Forward to RQ4-Optimize (Green):</b> Mixing `Rules Active × Cluster-Adaptive` (`[SLOT]` masking + `5 YAML rules` + sanitizer) achieves `0.0%` leakage (`Int. F = 34.82`), `98.6%` violation sensitivity (`F = 498.78`), `.952` Slot F1, AND `.506` style!"
            ),
            notes=(
                "Appearance 4 of 5 of the recurring 4-stage solution approach diagram, placed at the conclusion of RQ3-Govern. "
                "Point out how the Orange node from RQ2-Personalize turned Red when Rules were Off (35.9% leakage, 5.6% rule sensitivity), while combining Rules Active + Cluster-Adaptive produced the Green Pareto winner carried into RQ4-Optimize."
            ),
        )

    # =========================================================================
    # APPEARANCE 5 (stage_step == 4): END OF RQ4-OPTIMIZE (OPTIMIZE / RQ4 — FULL VALIDATED CASCADE)
    # =========================================================================
    return D.add_storyline_state_slide(
        module_label="9. Complete 4-Stage Solution Synthesis (Appearance 5 of 5)",
        title="Completed Four-Stage Solution Approach: Identify → Personalize → Govern → Optimize",
        subtitle="All four stages empirically validated (H01–H04 rejected at p < .001): Every green winner cascades into multi-turn turn economy",
        stages_data=[stage1_empirical, stage2_empirical, stage3_empirical, stage4_empirical],
        handoff_arrows=[
            {"active": True, "top_label": "RQ1 → RQ2", "bottom_label": "3 Blocks Personas\n+ Router (κ=.535)\n+ 3 FAISS DBs"},
            {"active": True, "top_label": "RQ2 → RQ3", "bottom_label": "Adaptive Style\n(.597, +31.8%)\n& 3.87w Pacing"},
            {"active": True, "top_label": "RQ3 → RQ4", "bottom_label": "0.0% Leakage +\n98.6% Rule Sens.\n+ .952 Slot F1"},
        ],
        bottom_callout=(
            "<b>Complete 4-Stage Solution Cascade Validated (Appearance 5 of 5):</b> "
            "<b>RQ1-Identify Stage</b> locked in `K-Means (k=3)` on `46-d Blocks` (`ARI = .89`, Router `κ = .535/.958`) and 3 FAISS sub-indices → "
            "<b>RQ2-Personalize Stage</b> proved those sub-indices lift style cosine (`+31.8%, p < .001`) and cut pacing error (`3.87w`) → "
            "<b>RQ3-Govern Stage</b> eliminated the `35.9%` entity leakage of unguarded ICL down to `0.0%` (`Int. F = 34.82`) and raised violation enforcement from `5.6% to 98.6%` → "
            "<b>RQ4-Optimize Stage</b> combined the governed stack with the `Verified Informed Slot Ledger` and persona trade-off framing to cut turns by `29.5% to 42.7%` (`F = 664.43, Int. F = 10.89, p < .001`) with `0.0%` redundant questions (`RER`)."
        ),
        notes=(
            "Appearance 5 of 5 of the recurring 4-stage solution approach diagram, completing the empirical arc across RQ1, RQ2, RQ3, and RQ4. "
            "Every Red path has been pruned with statistical proof, every Orange vulnerability has been resolved, and the Green cascade forms the deployed neuro-symbolic architecture."
        ),
    )


def add_pictorial_methodology_slide(D):
    """
    Pictorial representation of all IVs (X), DVs (Y), Primary Parametric Statistical Tests,
    Bullet-Proofing Robustness Checks, and Expected Findings across RQ1-Identify to RQ4-Optimize.
    Strictly METHODOLOGY ONLY (zero post-hoc empirical results).
    """
    s = D.content_slide(
        "4. Experimental Design & Statistical Methodology",
        "Pictorial Methodology Blueprint: IVs (X), DVs (Y), Tests & Bullet-Proofing",
        "End-to-end experimental design across Identify (RQ1) → Personalize (RQ2) → Govern (RQ3) → Optimize (RQ4) (Methodology Only)",
        notes=(
            "Presents the complete experimental methodology pictorially before any empirical results are shown. "
            "Walk through each column from top to bottom: (1) Manipulated Independent Variables (X) & Sample Design, "
            "(2) Primary Parametric Test, (3) Three-Layer Bullet-Proofing Robustness Checks, and (4) Measured Dependent Variables (Y) & Expected Findings."
        ),
    )

    stages = [
        {
            "badge": "RQ1-IDENTIFY",
            "subtitle": "Unsupervised Clustering & Prefix Routing",
            "hdr_col": NAVY,
            "iv_title": "Manipulated IVs (X1) & Design",
            "iv_lines": [
                "• <b>X<sub>1a</sub> (Algorithm):</b> `K-Means (k=3)` vs. `Ward` vs. `HDBSCAN` (`N = 159` runs, `n = 53`/alg on 80% subsamples of `D_gold = 933`).",
                "• <b>X<sub>1b</sub> (Prefix × Modality):</b> Horizon `M ∈ {3, 5, 7, 9, whole}` × (`Embeddings` vs. `16-Field LLM Codebook` vs. `46-d Blocks`).",
            ],
            "test_title": "Primary Parametric Tests",
            "test_lines": [
                "• <b>One-Way ANOVA (`F`)</b> across 159 independent runs + <b>Tukey HSD</b>.",
                "• <b>Matched RM-ANOVA (`F`, GG ε)</b> across the 53 shared random seeds.",
                "• <b>Feature Importance:</b> Unsupervised `η²`, Supervised L1 `‖β_j‖₂`, & Block-Drop `Δκ`.",
            ],
            "robust_title": "Bullet-Proofing & Validation Triad",
            "robust_lines": [
                "• <b>Heteroscedastic:</b> `Welch's ANOVA` + `Games–Howell` post hoc.",
                "• <b>Non-Parametric:</b> `Kruskal–Wallis H` + Paired `Friedman χ²` + Permutation Null.",
                "• <b>Generalization:</b> 5-Fold Stratified CV + Held-Out `D_test (n = 401)` Confusion Matrix & Multiclass OvR `ROC-AUC`.",
            ],
            "dv_title": "Measured DVs (Y1) & Expected Finding",
            "dv_lines": [
                "• <b>DVs (Y<sub>1</sub>):</b> Cosine Silhouette `[-1,1]`, Davies–Bouldin, Bootstrap `ARI ≥ .60`, Held-Out Prefix Routing `κ` & `Macro-F1`.",
                "• <b>Expected (H<sub>a1</sub>):</b> Algorithms differ (`p < .05`); prefix `Blocks` eliminates outcome confounding and enables early routing.",
            ],
        },
        {
            "badge": "RQ2-PERSONALIZE",
            "subtitle": "Within-Subjects Style & Pacing ICL",
            "hdr_col": TEAL,
            "iv_title": "Manipulated IV (X2) & Design",
            "iv_lines": [
                "• <b>X<sub>2</sub> (Prompting Strategy — 3 Levels):</b>\n  1. `Zero-Shot` (generic instruction)\n  2. `Static Few-Shot (k=3)` (unrouted)\n  3. `Cluster-Adaptive (k=3)` (`[SLOT]` FAISS sub-index + pacing directive).",
                "• <b>Design:</b> Repeated-measures (`N = 33` `D_test` chats × 3 = `99` calls; `11`/persona).",
            ],
            "test_title": "Primary Parametric Tests",
            "test_lines": [
                "• <b>One-Way Repeated-Measures ANOVA (`F`)</b> removing baseline dialogue variance (`ρ = .50`).",
                "• <b>Greenhouse–Geisser (`ε`)</b> sphericity correction on degrees of freedom.",
                "• <b>Holm–Bonferroni</b> step-down paired `t`-tests & standardized `d_z`.",
            ],
            "robust_title": "Bullet-Proofing & Validation Triad",
            "robust_lines": [
                "• <b>Non-Parametric Rank Check:</b> Within-dialogue `Friedman χ²(2)` rank test.",
                "• <b>Encoder Independence:</b> Evaluated via non-Gemini encoders (`all-MiniLM-L6-v2` & `roberta-large` BERTScore).",
                "• <b>Causal Routing Check:</b> Contrast Primary (coarse) vs. Refined (`Blocks`) routing.",
            ],
            "dv_title": "Measured DVs (Y2) & Expected Finding",
            "dv_lines": [
                "• <b>DVs (Y<sub>2</sub>):</b> De-lexicalized SBERT Style Cosine (primary), Gemini 3,072-d Cosine, Token `BERTScore F1`, & Pacing Word Error `|W_gen − μ_k|`.",
                "• <b>Expected (H<sub>a2</sub>):</b> `Cluster-Adaptive` increases style cosine & reduces pacing error (`p < .05`) when routing is coherent.",
            ],
        },
        {
            "badge": "RQ3-GOVERN",
            "subtitle": "2 × 2 Factorial Policy & Leakage Guard",
            "hdr_col": CORAL,
            "iv_title": "Manipulated IVs (X3) & Design",
            "iv_lines": [
                "• <b>Factor A (`Rules Mode`):</b> `Rules Off` (prompt-only) vs. `Rules Active` (`5 YAML rules` + `[SLOT]` mask + sanitizer).",
                "• <b>Factor B (`Prompting`):</b> `Zero-Shot` vs. `Cluster-Adaptive`.",
                "• <b>Design:</b> Balanced `2 × 2` (`N = 144` `D_test` units, `n = 36`/cell; 50% violating / 50% compliant).",
            ],
            "test_title": "Primary Parametric Tests",
            "test_lines": [
                "• <b>2 × 2 Factorial OLS ANOVA (`F`, Type II/III Orthogonal `Sum` Contrasts)</b> testing Main Effect A, Main Effect B, and `A × B Interaction`.",
                "• <b>Subgroup Split:</b> Violation Enforcement Sensitivity (`n=72`) vs. Compliant Specificity (`n=72`).",
            ],
            "robust_title": "Bullet-Proofing & Validation Triad",
            "robust_lines": [
                "• <b>Heteroscedastic Zero-Cell Guard:</b> `MacKinnon–White HC3` sandwich SEs.",
                "• <b>Non-Parametric Factorial:</b> `Aligned Rank Transform (ART) ANOVA`.",
                "• <b>Cross-Model Dual Judge:</b> Independent `gemini-2.5-pro` audit (`n = 48`, target `κ ≥ .70`) + deterministic regex check.",
            ],
            "dv_title": "Measured DVs (Y3–Y5) & Expected Finding",
            "dv_lines": [
                "• <b>DVs (Y<sub>3</sub>–Y<sub>5</sub>):</b> Rule Adherence Rate (`RAR`), Exemplar Entity Leakage Rate (`ELR`), Factual `Slot F1`, & Style Cosine.",
                "• <b>Expected (H<sub>a3</sub>):</b> `Rules Active` raises `RAR` & `Slot F1` and interacts with `Prompting` (`p < .05`) to eliminate few-shot entity leakage.",
            ],
        },
        {
            "badge": "RQ4-OPTIMIZE",
            "subtitle": "2 × 3 Multi-Turn Turn Economy",
            "hdr_col": GREEN,
            "iv_title": "Manipulated IVs (X4) & Design",
            "iv_lines": [
                "• <b>Factor A (`Prompting`):</b> `Zero-Shot` (sequential 1-opt, no ledger) vs. `Cluster-Adaptive` (Governed Stack + `Slot Ledger` + Persona Package Policy).",
                "• <b>Factor B (`Refined Archetype`):</b> `Decisive Booker`, `Open Explorer`, `Rigid-Constraint Seeker`.",
                "• <b>Design:</b> Balanced `2 × 3` (`N = 180` closed-loop sims, `n = 30`/cell across 4-option catalog).",
            ],
            "test_title": "Primary Parametric Tests",
            "test_lines": [
                "• <b>2 × 3 Factorial OLS ANOVA (`F`)</b> on natural-log turns `Y = ln(TGC)`, Raw Turns, and `RER` (Main Effects A, B & `A × B Interaction`).",
                "• <b>Within-Archetype Simple Contrasts:</b> Standardized `Cohen's d` per persona.",
            ],
            "robust_title": "Bullet-Proofing & Validation Triad",
            "robust_lines": [
                "• <b>Boundary-Floor Variance Guard:</b> `HC3` robust `F` + `Welch's t`-test.",
                "• <b>Non-Parametric Checks:</b> `ART Factorial ANOVA` + exact `Mann–Whitney U`.",
                "• <b>Simulator Construct Audit:</b> Blind `gemini-2.5-pro` persona classification (`n = 45`, target `κ ≥ .70`) + Human Baseline context.",
            ],
            "dv_title": "Measured DVs (Y6) & Expected Finding",
            "dv_lines": [
                "• <b>DVs (Y<sub>6</sub>):</b> Log Turns to Goal Completion (`ln TGC`), Raw Turns (`TGC`), & Redundant Elicitation Rate (`RER`).",
                "• <b>Expected (H<sub>a4</sub>):</b> `Cluster-Adaptive` cuts `ln(TGC)` & `RER` (`p < .05`) with a significant `Prompting × Archetype` interaction.",
            ],
        },
    ]

    start_x = 0.24
    col_w = 2.94
    gap_w = 0.36
    top_y = 1.48

    row_heights = [0.38, 1.18, 1.04, 1.12, 1.14]  # Header, IVs, Parametric, Bullet-Proofing, DVs/Expected
    row_Colors = [
        None,
        (RGBColor(238, 243, 250), BLUE),
        (WHITE, NAVY),
        (CALLOUT_BG, GOLD),
        (GREEN_BG, GREEN),
    ]

    for idx, st in enumerate(stages):
        x = start_x + idx * (col_w + gap_w)
        cur_y = top_y

        # Stage Header Banner
        hdr = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(cur_y), Inches(col_w), Inches(row_heights[0]))
        hdr.adjustments[0] = 0.04
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = st["hdr_col"]
        hdr.line.fill.background()
        tf_h = hdr.text_frame
        tf_h.word_wrap = True
        tf_h.margin_left = tf_h.margin_right = Inches(0.05)
        tf_h.margin_top = tf_h.margin_bottom = Inches(0.01)
        p1 = tf_h.paragraphs[0]
        p1.alignment = PP_ALIGN.CENTER
        _add_formatted_runs(p1, st["badge"], font_size=8.8, color=WHITE, bold=True)
        p2 = tf_h.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        _add_formatted_runs(p2, st["subtitle"], font_size=6.8, color=RGBColor(225, 238, 255), italic=True)
        cur_y += row_heights[0] + 0.04

        blocks = [
            (st["iv_title"], st["iv_lines"], row_heights[1], row_Colors[1]),
            (st["test_title"], st["test_lines"], row_heights[2], row_Colors[2]),
            (st["robust_title"], st["robust_lines"], row_heights[3], row_Colors[3]),
            (st["dv_title"], st["dv_lines"], row_heights[4], row_Colors[4]),
        ]

        for b_i, (b_title, b_lines, bh, (bg_c, bdr_c)) in enumerate(blocks):
            box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(cur_y), Inches(col_w), Inches(bh))
            box.adjustments[0] = 0.03
            box.fill.solid()
            box.fill.fore_color.rgb = bg_c
            box.line.color.rgb = bdr_c
            box.line.width = Pt(1.2)

            # Mini title strip
            m_hdr = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(cur_y), Inches(col_w), Inches(0.21))
            m_hdr.fill.solid()
            m_hdr.fill.fore_color.rgb = bdr_c
            m_hdr.line.fill.background()
            p_mh = m_hdr.text_frame.paragraphs[0]
            p_mh.alignment = PP_ALIGN.CENTER
            _add_formatted_runs(p_mh, b_title, font_size=7.1, color=WHITE, bold=True)

            tb = s.shapes.add_textbox(Inches(x + 0.05), Inches(cur_y + 0.22), Inches(col_w - 0.10), Inches(bh - 0.24))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0.01)
            for l_i, ln in enumerate(b_lines):
                p = tf.paragraphs[0] if l_i == 0 else tf.add_paragraph()
                p.space_after = Pt(1.2)
                _add_formatted_runs(p, ln, font_size=6.5, color=DARK)

            cur_y += bh
            if b_i < len(blocks) - 1:
                arr = s.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(x + col_w / 2.0 - 0.09), Inches(cur_y + 0.01), Inches(0.18), Inches(0.09))
                arr.fill.solid()
                arr.fill.fore_color.rgb = st["hdr_col"]
                arr.line.fill.background()
                cur_y += 0.11

        # Inter-stage horizontal connector arrow
        if idx < 3:
            hx = x + col_w + 0.04
            hw = gap_w - 0.08
            h_arr = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(hx), Inches(3.85), Inches(hw), Inches(0.28))
            h_arr.fill.solid()
            h_arr.fill.fore_color.rgb = NAVY
            h_arr.line.color.rgb = GOLD
            h_arr.line.width = Pt(0.8)

    D.add_callout(
        s,
        0.24,
        6.40,
        12.85,
        0.72,
        "<b>Solution Approach Methodology Link:</b> Every stage in `Identify → Personalize → Govern → Optimize` pre-declares its manipulated IV (`X`), measured DVs (`Y`), primary parametric ANOVA, and a <b>3-layer bullet-proofing protocol</b> (`Parametric OLS/RM-ANOVA` + `Heteroscedasticity-Robust Welch/HC3` + `Distribution-Free Non-Parametric Kruskal/Friedman/ART` + `Independent Gemini 2.5 Pro Judge Validation`) prior to inspecting any empirical outcomes.",
        bg_color=CALLOUT_BG,
        border_color=GOLD,
        font_size=8.8,
    )
    return s

