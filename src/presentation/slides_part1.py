"""
Part 1 of the QM640 Capstone Defense Presentation (Slides 1–24):
  - Module 1 (Slides 1–6): Problem Statement, Technical Paradox, Conceptual 4-Stage Solution Approach (Appearance 1 of 5), and Core Concepts Primer
  - Module 2 (Slides 7–10): Concise Literature Collection & Operationalization Synthesis Aligned with the 4-Stage Solution Approach
  - Module 3 (Slides 11–16): Dataset Authenticity, Two-Tier Schema, Hygiene Audit, 70/30 Firewall, and Expanded Exploratory Data Analysis
  - Module 4 (Slides 17–24): RQs, Hypotheses, Pictorial Methodology Blueprint, Statistical Test Mechanics, Noncentral-F Sample Size Derivation, Feature Importance Methodology, and System Architecture (Strictly Methodology Only — Zero Empirical Findings)
"""

import os
from presentation.ppt_styles import (
    BLUE,
    CALLOUT_BG,
    CARD_ALT,
    CARD_BG,
    CORAL,
    GOLD,
    GREEN,
    GREEN_BG,
    NAVY,
    RED_BG,
    TEAL,
)
from presentation.storyline_slides import (
    add_pictorial_methodology_slide,
    add_storyline_discovery_slide,
)
from report.final_context import FIG_FIN, FIG_INT, REPO, TITLE


def build_slides_part1(D, ctx):
    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    D.add_title_slide(
        title=TITLE,
        subtitle="A Four-Stage Neuro-Symbolic Framework (Identify → Personalize → Govern → Optimize) Coupling "
                 "Early-Turn Behavioral-Semantic Routing, Slot-Masked FAISS In-Context Learning, and Declarative Policy Verification",
        author_lines=[
            "<b>Author:</b> Surnella Sandeep  |  <b>Course:</b> QM640: Data Analytics Capstone (Department of Data Analytics, Walsh College)",
            "<b>Instructor & Capstone Mentor:</b> Mr. Smitraj Raut  |  <b>Date:</b> 10th Nov 2026",
            f"<b>Reproducible Code & Data Repository:</b> {REPO}",
            "<b>Empirical Scope:</b> 2,833 Analytic Human Dialogues (Microsoft Frames N = 1,334; MultiWOZ 2.2 N = 1,499) + ~8,900 Gemini 2.5 Flash/Pro Evaluations",
        ],
        notes=(
            "Welcome to the comprehensive defense presentation for the QM640 Data Analytics Capstone. "
            "The presentation is organized around a four-stage solution approach—Identify, Personalize, Govern, and Optimize—so "
            "both AI specialists and statistical/business domain reviewers can trace every methodological choice, "
            "empirical test, and causal handoff from raw dialogue logs to multi-turn business optimization."
        ),
    )

    # =========================================================================
    # SLIDE 2: PRESENTATION ROADMAP ALIGNED TO THE 4-STAGE STORYLINE
    # =========================================================================
    s = D.content_slide(
        "1. Problem Statement & 4-Stage Solution Approach",
        "Presentation Roadmap: Integrated Around the Four-Stage Solution Approach",
        "Every section—Literature, EDA, Methodology, Empirical Results, Doctoral Extensions, and Q&A—maps directly to Identify → Personalize → Govern → Optimize",
        notes="Orient the defense committee to the narrative arc of the presentation and how the 4-stage solution approach diagram recurs 5 times as empirical decisions are locked in.",
    )
    D.add_card(
        s, 0.35, 1.48, 3.05, 2.42,
        title="1. Problem & Solution Approach (Slides 1–6)",
        header_bg=NAVY,
        bullets=[
            "Why static travel chatbots fail across diverse shopper personas.",
            "Why naive few-shot AI leaks entities & violates policies.",
            "<b>Solution Approach #1:</b> Conceptual `Identify → Personalize → Govern → Optimize` blueprint.",
        ],
        font_size=10.2,
    )
    D.add_card(
        s, 3.55, 1.48, 3.05, 2.42,
        title="2. Literature Synthesis (Slides 7–10)",
        header_bg=TEAL,
        bullets=[
            "26 peer-reviewed studies across 4 research streams.",
            "6-Column Relevance Matrix mapping every study to the 4 stages.",
            "How literature inspired the neuro-symbolic operationalization.",
        ],
        font_size=10.2,
    )
    D.add_card(
        s, 6.75, 1.48, 3.05, 2.42,
        title="3. Data, Hygiene & EDA (Slides 11–16)",
        header_bg=BLUE,
        bullets=[
            "Microsoft Frames (N=1,334) & MultiWOZ 2.2 (N=1,499) provenance.",
            "Two-Tier Pydantic schema & 70/30 zero-leakage firewall.",
            "Univariate, Outcome-Stratified, Bivariate & PCA Biplot EDA.",
        ],
        font_size=10.2,
    )
    D.add_card(
        s, 9.95, 1.48, 3.03, 2.42,
        title="4. Pure Methodology (Slides 17–24)",
        header_bg=GOLD,
        bullets=[
            "RQs, Hypotheses & Pictorial Blueprint of IVs, DVs & Tests.",
            "Why ANOVA, RM-ANOVA & 2×2 / 2×3 Factorial ANOVA fit.",
            "Noncentral-F sample size (α, β, f, λ), Feature Importance & System Architecture.",
        ],
        font_size=10.2,
    )
    D.add_card(
        s, 0.35, 4.02, 3.05, 2.42,
        title="5. RQ1–RQ2 Results (Slides 25–37)",
        header_bg=NAVY,
        bullets=[
            "<b>RQ1-Identify Stage:</b> 159-run benchmark, 46-d `Blocks`, Feature Importance, Train/CV/Test Router, CM/ROC & <b>Solution Approach #2</b>.",
            "<b>RQ2-Personalize Stage:</b> Primary vs. Refined contrast, Table 16 & <b>Solution Approach #3</b>.",
        ],
        font_size=10.2,
    )
    D.add_card(
        s, 3.55, 4.02, 3.05, 2.42,
        title="6. RQ3–RQ4 Results (Slides 38–48)",
        header_bg=GREEN,
        bullets=[
            "<b>RQ3-Govern Stage:</b> 2×2 Rules × Prompting, Sensitivity/Specificity, Sum-SS proof, Tokyo output & <b>Solution Approach #4</b>.",
            "<b>RQ4-Optimize Stage:</b> 2×3 simulation, Persona audit, Table 18 guide, Human baseline & <b>Solution Approach #5</b>.",
        ],
        font_size=10.2,
    )
    D.add_card(
        s, 6.75, 4.02, 3.05, 2.42,
        title="7. ROI & Doctoral Roadmap (Slides 49–57)",
        header_bg=BLUE,
        bullets=[
            "Consolidated Scorecard, 1M-Session ROI & Microservice Runtime.",
            "Hierarchical `3×6=18` FAISS retrieval & Soft Bayesian Drift.",
            "Multi-Call `Opportunity_ID` Turn Economy (`TTL, TTQ_s, CSET`) & `Turn-Q DB` Data Flow.",
        ],
        font_size=10.2,
    )
    D.add_card(
        s, 9.95, 4.02, 3.03, 2.42,
        title="8. Defense Q&A Bank (Slides 58–66)",
        header_bg=CORAL,
        bullets=[
            "11 evidence-backed Q&A deep-dives linked to the solution approach:",
            "Sample size assumptions, originality, dataset fit, judge independence, cold-start turns < 9, quotation vs. booking noise, 3 vs. 500 clusters, and centroid naming.",
        ],
        font_size=10.2,
    )
    D.add_callout(
        s, 0.35, 6.54, 12.63, 0.58,
        "<b>Core Solution Architecture:</b> The same pictorial <b>4-Stage Solution Approach Diagram (`Identify → Personalize → Govern → Optimize`)</b> is introduced right after the Problem Statement and updated at the conclusion of every stage—color-coding tested paths as <b>Red (Closed/Dropped)</b>, <b>Orange (Needs Next-Stage Verification)</b>, or <b>Green (Winner Carried Forward)</b>.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=10.0,
    )

    # =========================================================================
    # SLIDE 3: THE REAL-WORLD BUSINESS PROBLEM (CONCRETE DIALOGUE EXAMPLES)
    # =========================================================================
    s = D.content_slide(
        "1. Problem Statement & 4-Stage Solution Approach",
        "The Real-World Business Problem: Why Static Travel Chatbots Fail",
        "Travelers exhibit fundamentally different decision-making behaviors—yet commercial chatbots force every shopper through one static script",
        notes="Start with a relatable real-world scenario. Show how three different customers enter an Online Travel Agency (OTA) portal and get frustrated by a one-size-fits-all chatbot.",
    )
    D.add_card(
        s, 0.35, 1.48, 4.05, 4.78,
        title="Customer Type A: The Decisive Booker",
        header_bg=NAVY,
        bullets=[
            "<b>How the traveler speaks (Frames ID e2c09f7a):</b>",
            (1, "<i>'I need a 5-night package from Dallas to Cancun departing Aug 12 for 2 adults under $2,400.'</i>"),
            "<b>What the traveler wants:</b>",
            (1, "Immediate confirmation of the best matching package and direct quotation closure without small talk."),
            "<b>How a Static Chatbot fails this traveler:</b>",
            (1, "Follows a slow multi-step intake script and re-asks constraints already stated in Turn 1."),
            (1, "Generates verbose 30-word paragraphs instead of a crisp confirmation."),
            "<b>Business Consequence:</b> High-intent buyers abandon the session out of impatience.",
        ],
        font_size=10.3,
    )
    D.add_card(
        s, 4.60, 1.48, 4.10, 4.78,
        title="Customer Type B: The Open Explorer",
        header_bg=TEAL,
        bullets=[
            "<b>How the traveler speaks (Frames ID b84f11c2):</b>",
            (1, "<i>'Looking for a week off in September under a $3,000 budget—what beach or European cities can be compared?'</i>"),
            "<b>What the traveler wants:</b>",
            (1, "Side-by-side comparison of 2–3 distinct destination or hotel-tier options to weigh trade-offs."),
            "<b>How a Static Chatbot fails this traveler:</b>",
            (1, "Presents only one option per turn, forcing the traveler to ask <i>'What about another city?'</i> or <i>'What about 4-star vs. 3-star?'</i> across many turns."),
            "<b>Business Consequence:</b> Exhausting, bloated sessions that inflate cloud inference cost and customer fatigue.",
        ],
        font_size=10.3,
    )
    D.add_card(
        s, 8.90, 1.48, 4.08, 4.78,
        title="Customer Type C: Rigid-Constraint Seeker",
        header_bg=CORAL,
        bullets=[
            "<b>How the traveler speaks (Frames ID 91a4d0e5):</b>",
            (1, "<i>'I only want a 5-star hotel in Tokyo on Oct 5 for 10 nights under $2,200—no other dates or stars.'</i>"),
            "<b>What the traveler wants:</b>",
            (1, "When exact inventory exceeds budget, the shopper needs immediate, transparent trade-off options (e.g., 4-star on exact dates vs. 5-star on shifted dates)."),
            "<b>How a Static Chatbot fails this traveler:</b>",
            (1, "Outputs a dead-end <i>'No package found'</i> or argues across multiple turns without offering structured compromise alternatives."),
            "<b>Business Consequence:</b> Multi-turn negotiation deadlocks and high walk-away rates.",
        ],
        font_size=10.3,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`RQ1-Identify` & `RQ4-Optimize`):</b> "
        "Online travel agencies (Buhalis & Sinarta, 2019; Ivanov & Webster, 2019; Melián-González et al., 2021) cannot achieve turn economy (`RQ4-Optimize`) with a single static prompt because these three customer types require fundamentally different pacing (`RQ2-Personalize`) and package trade-off policies—requiring early behavioral identification (`RQ1-Identify`).",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 4: THE TECHNICAL PARADOX — WHY NAIVE AI ADAPTATION FAILS
    # =========================================================================
    s = D.content_slide(
        "1. Problem Statement & 4-Stage Solution Approach",
        "The Technical Paradox: Why Naive Few-Shot AI Adaptation Fails",
        "Simply pasting retrieved historical dialogues into an LLM prompt introduces two severe production hazards",
        notes="Explain why standard Retrieval-Augmented Generation (RAG) or naive KATE few-shot prompting is insufficient on its own, motivating RQ2-Personalize (Slot-Masked Personalization) and RQ3-Govern (Symbolic Governance).",
    )
    D.add_card(
        s, 0.35, 1.48, 6.15, 3.25,
        title="Hazard 1: Exemplar Entity Leakage (Hallucinated Terms)",
        header_bg=CORAL,
        bg_color=RED_BG,
        bullets=[
            "<b>What happens in standard few-shot prompting (Liu et al., 2022):</b>",
            (1, "To teach the LLM how to speak to an <i>Open Explorer</i>, a standard retrieval system fetches 3 similar past transcripts from a vector database and inserts them into the prompt."),
            "<b>The Contamination Trap:</b>",
            (1, "If those retrieved historical examples mention specific resort names (<i>'Sapphire Bay Resort'</i>), airlines (<i>'SkyBridge Airways'</i>), historical prices (<i>'$1,149'</i>), or promo codes (<i>'VIP25'</i>), the neural language model copies those stale entities directly into the active customer's reply!"),
        ],
        font_size=10.5,
    )
    D.add_card(
        s, 6.80, 1.48, 6.18, 3.25,
        title="Hazard 2: Enterprise Policy Blindness (Rule Violations)",
        header_bg=CORAL,
        bg_color=RED_BG,
        bullets=[
            "<b>What happens when rules are only written in natural language prompts:</b>",
            (1, "Travel bookings are governed by strict numeric constraints: international departures require ≥ 15 days visa processing lead time; passports require ≥ 6 months validity; FIT packages cap at ≤ 4 adults; promotional discounts cap at ≤ 15%."),
            "<b>The Attention Competition Trap (Yao et al., 2024):</b>",
            (1, "When the LLM optimizes attention to mimic conversational tone and style from few-shot examples, it routinely overlooks arithmetic policy thresholds buried in system instructions."),
        ],
        font_size=10.5,
    )
    D.add_card(
        s, 0.35, 4.82, 12.63, 1.46,
        title="Why Both Neural Adaptation AND Symbolic Governance Are Required",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>1. Neural Prompting Alone (Style Without Rules):</b> Adapts conversational tone and verbosity when routed to the right persona, but leaks stale exemplar entities and fails strict booking rules.",
            "<b>2. Symbolic Rules Alone (Rules Without Style):</b> Enforces arithmetic visa, passport, capacity, and discount policies deterministically, but produces rigid, one-size-fits-all responses that ignore shopper persona.",
            "<b>3. Neuro-Symbolic Synthesis:</b> Only by joining early persona routing (`Identify`), `[SLOT]`-masked exemplar retrieval (`Personalize`), declarative `YAML` policy checks (`Govern`), and an informed-slot ledger (`Optimize`) can an assistant achieve both style and compliance.",
        ],
        font_size=9.8,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`RQ2-Personalize` → `RQ3-Govern`):</b> "
        "This technical paradox defines the central tension of the solution approach: <b>RQ2-Personalize</b> tests whether persona clustering improves LLM style, while <b>RQ3-Govern</b> tests whether combining declarative symbolic rules with `[SLOT]`-masked adaptive prompting resolves entity leakage and policy blindness.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 5: STORYLINE APPEARANCE #1 — CONCEPTUAL 4-STAGE STORYLINE (IMMEDIATELY AFTER PROBLEM STATEMENT)
    # =========================================================================
    add_storyline_discovery_slide(D, stage_step=0)

    # =========================================================================
    # SLIDE 6: CORE CONCEPTS EXPLAINED FROM THE GROUND UP
    # =========================================================================
    s = D.content_slide(
        "1. Problem Statement & 4-Stage Solution Approach",
        "Core Concepts Explained from the Ground Up (Plain-English Primer)",
        "Bridging AI/NLP terminology and statistical measurement across all four stages of the solution approach",
        notes="Use this slide to make sure interdisciplinary committee members have crystal-clear intuition for the 6 building blocks mapped across RQ1-Identify to RQ4-Optimize.",
    )
    D.add_table(
        s, 0.35, 1.46, 12.63, 4.80,
        headers=["Solution Stage & Concept", "Plain-English Meaning", "Real-World Analogy", "How It Is Operationalized in This Study"],
        rows=[
            [
                "RQ1-Identify Stage:\nVector Embedding\n(SBERT 384-d & Gemini 3,072-d)",
                "Converting a sentence or dialogue prefix into a list of coordinates so similar meanings and behaviors sit close together in geometry.",
                "Like GPS coordinates (latitude, longitude) on a map, extended to 384 or 3,072 dimensions capturing meaning and tone.",
                "Cosine similarity [-1, +1] between vectors: +1 = identical direction/style; 0 = orthogonal/unrelated.",
            ],
            [
                "RQ1-Identify Stage:\nUnsupervised Clustering\n(K-Means, Ward, HDBSCAN)",
                "Automatically grouping training dialogues into natural customer behavior segments without pre-labeled categories.",
                "Sorting retail shoppers into 'Quick Grab-and-Go', 'Window Browsers', and 'Strict Budget Hunters' by watching how they shop.",
                "Cosine Silhouette [-1, +1] (higher = tighter separation), Davies–Bouldin (lower = better), and Bootstrap ARI stability [0, 1].",
            ],
            [
                "RQ1 → RQ2 Handoff:\nEarly-Turn Prefix Routing\n(RefinedArchetypeRouter)",
                "Predicting which behavioral archetype a new customer belongs to after reading only their opening M (e.g., 5 to 9) messages.",
                "An experienced hotel concierge recognizing a guest's decision style within the first 60 seconds of conversation.",
                "Out-of-sample Routing Accuracy (%), Macro-F1, Multiclass ROC-AUC, and chance-corrected Cohen's Kappa (κ).",
            ],
            [
                "RQ2-Personalize Stage:\nSlot-Masked FAISS\nFew-Shot Prompting",
                "Retrieving the 3 closest past dialogues from the matched archetype's FAISS index with entities masked as [SLOT] to guide LLM style.",
                "Giving a sales associate 3 redacted scripts showing *how* to structure an answer without letting them quote last week's prices.",
                "De-lexicalized SBERT Style Convergence Cosine and Pacing Calibration Error (|generated words − target archetype words|).",
            ],
            [
                "RQ3-Govern Stage:\nNeuro-Symbolic Guardrail\n(Declarative Rule Engine)",
                "Combining a neural LLM (for fluent language) with deterministic code rules (YAML policies) that verify constraints pre- & post-generation.",
                "An architect designing a creative building (Neural LLM) checked by a structural engineer's building-code calculator (Symbolic Engine).",
                "Rule Adherence Rate (RAR: Violation Sensitivity & Compliant Specificity), Exemplar Leakage Rate (ELR), and Factual Slot F1 [0, 1].",
            ],
            [
                "RQ4-Optimize Stage:\nTurn Economy & Redundant\nElicitation Rate (RER)",
                "How many back-and-forth turns are needed to reach an agreed package quotation, and how often the agent wastes turns re-asking stated facts.",
                "Closing a travel quotation in 5 focused turns instead of 9 repetitive turns asking 'Where are you flying from?' twice.",
                "Turns to Goal Completion (TGC, raw & natural-log transformed ln TGC) and RER = redundant slot questions / total assistant turns.",
            ],
        ],
        col_widths=[2.0, 3.2, 3.4, 4.0],
        font_size=9.5,
        align_left_cols=(0, 1, 2, 3),
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment:</b> These six concepts map one-to-one onto the 4-stage cascade: <b>Embeddings, Clustering & Prefix Routing</b> power `RQ1-Identify Stage` → <b>Slot-Masked FAISS Retrieval</b> powers `RQ2-Personalize Stage` → <b>Declarative YAML Rule Verification</b> powers `RQ3-Govern Stage` → <b>Turn Economy & Zero-RER Slot Ledgers</b> power `RQ4-Optimize Stage`.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 7: LITERATURE REVIEW (PART 1): STREAMS 1 & 2 LINKED TO THE STORYLINE
    # =========================================================================
    s = D.content_slide(
        "2. Literature Collection & Synthesis Aligned with Solution Approach",
        "Literature Synthesis (Part 1): Hospitality AI Value & Task-Oriented Corpora",
        "Streams 1 & 2: How prior tourism ROI research and human Wizard-of-Oz corpora inspired RQ1-Identify Stage and RQ4-Optimize Stage",
        notes="Now that the audience understands the 4-stage big picture, show how Literature Streams 1 and 2 inspired RQ1-Identify Stage and RQ4-Optimize Stage.",
    )
    D.add_card(
        s, 0.35, 1.48, 6.15, 4.78,
        title="Stream 1: Hospitality AI Value & Turn Economy → RQ4-Optimize & RQ1-Identify",
        header_bg=NAVY,
        bullets=[
            "<b>Prior Literature Foundations:</b>",
            (1, "<b>Buhalis & Sinarta (2019):</b> Framed real-time 'nowness' co-creation in smart tourism—travelers expect rapid, context-aware itinerary synthesis."),
            (1, "<b>Ivanov & Webster (2019):</b> Established the economic ROI model for hospitality AI: automation yields net value only when resolving consultative queries without human escalation."),
            (1, "<b>Melián-González et al. (2021):</b> Surveyed <i>N</i> = 1,476 consumers and showed perceived interaction efficiency and task fit drive chatbot adoption."),
            (1, "<b>Jannach et al. (2021) & Inaba et al. (2022):</b> Documented qualitatively that travelers vary widely in initiative, exploration breadth, and constraint rigidity."),
            "<b>Gap in Prior Work & Solution Approach Operationalization:</b>",
            (1, "Prior tourism studies relied on <i>post-hoc perception surveys</i> rather than programmatic dialogue policies."),
            (1, "<b>Inspiration for RQ1-Identify & RQ4-Optimize:</b> Translate qualitative shopper traits into a <b>16-field quantitative behavioral codebook (`RQ1-Identify`)</b> and instrument direct conversational efficiency metrics—<b>Turns to Goal Completion (`ln TGC`) and Redundant Elicitation Rate (`RER`) (`RQ4-Optimize`)</b>."),
        ],
        font_size=9.8,
    )
    D.add_card(
        s, 6.80, 1.48, 6.18, 4.78,
        title="Stream 2: Task-Oriented Dialogue Corpora → RQ1-Identify & RQ4-Optimize",
        header_bg=TEAL,
        bullets=[
            "<b>Prior Literature Foundations:</b>",
            (1, "<b>El Asri et al. (2017) [Microsoft Frames]:</b> Collected 1,369 human–human Wizard-of-Oz vacation package negotiations (19,986 turns) to study non-linear <i>frame-switching</i> across flight+hotel bundles under budget ceilings."),
            (1, "<b>Budzianowski et al. (2018) & Zang et al. (2020) [MultiWOZ 2.2]:</b> Built a 10,438-dialogue benchmark for supervised multi-domain slot-filling across local city services."),
            (1, "<b>Walker et al. (1997) [PARADISE] & Deriu et al. (2021):</b> Established decoupling dialogue-internal task success (agreed quotation) from exogenous checkout noise."),
            "<b>Gap in Prior Work & Solution Approach Operationalization:</b>",
            (1, "Both Frames and MultiWOZ were modeled with <i>uniform supervised state trackers</i> that treat all speakers identically and ignore enterprise policy rules."),
            (1, "<b>Inspiration for RQ1-Identify & RQ4-Optimize:</b> Use Microsoft Frames (<i>N</i> = 1,334 analytic) to discover latent shopper negotiation archetypes (`RQ1-Identify`), use MultiWOZ (<i>N</i> = 1,499) as an external domain-transfer control, and ground closed-loop turn-economy simulations (`RQ4-Optimize`)."),
        ],
        font_size=9.8,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Foundation (Streams 1 & 2 → RQ1-Identify & RQ4-Optimize):</b> "
        "Stream 1 provides the <b>behavioral constructs</b> (`decisiveness, exploration, rigidity` → `RQ1-Identify`) and <b>business efficiency criteria</b> (`turn economy & non-redundancy` → `RQ4-Optimize`), while Stream 2 provides the <b>authentic human negotiation trajectories</b> (`Microsoft Frames`) required to discover and test those stages.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 8: LITERATURE REVIEW (PART 2): STREAMS 3 & 4 LINKED TO THE STORYLINE
    # =========================================================================
    s = D.content_slide(
        "2. Literature Collection & Synthesis Aligned with Solution Approach",
        "Literature Synthesis (Part 2): Representation Learning, FAISS ICL & Guardrails",
        "Streams 3 & 4: How embedding geometry, k-NN in-context learning, and programmable rails inspired RQ1-Identify, RQ2-Personalize, and RQ3-Govern",
        notes="Show how Literature Stream 3 inspired RQ1-Identify Stage and Stream 4 inspired RQ2-Personalize Stage and RQ3-Govern Stage.",
    )
    D.add_card(
        s, 0.35, 1.48, 6.15, 4.78,
        title="Stream 3: Embeddings, Clustering & LLM Coding → RQ1-Identify Stage",
        header_bg=BLUE,
        bullets=[
            "<b>Prior Literature Foundations:</b>",
            (1, "<b>Reimers & Gurevych (2019) [SBERT]</b> & <b>Lee et al. (2025) [Gemini Embeddings]:</b> Bi-encoder transformers map text into metric cosine spaces suitable for clustering."),
            (1, "<b>McInnes et al. (2017, 2018) [HDBSCAN & UMAP]</b> & <b>Hennig (2007) [Bootstrap ARI]:</b> Density clustering and bootstrap cluster stability (`ARI ≥ .60`)."),
            (1, "<b>Gilardi et al. (2023):</b> Zero-temperature LLMs achieve high inter-coder reliability on structured behavioral annotation tasks."),
            "<b>Where Prior Methods Stop & Solution Approach Operationalization:</b>",
            (1, "Standard clustering studies embed <i>entire documents</i>. In multi-turn dialogues, whole-chat embeddings mix customer and agent turns and leak end-of-session outcomes (`Booked` vs. `No Option`), making early-turn routing fail!"),
            (1, "<b>Inspiration for RQ1-Identify Stage:</b> Truncate transcripts to the <b>opening M user messages</b> and fuse <b>PCA-20 Gemini prefix embeddings with Gilardi-style zero-temp LLM behavioral ratings (`46-d Blocks`)</b> plus an L1 logistic prefix router."),
        ],
        font_size=9.8,
    )
    D.add_card(
        s, 6.80, 1.48, 6.18, 4.78,
        title="Stream 4: Dynamic FAISS ICL & Symbolic Rails → RQ2-Personalize & RQ3-Govern",
        header_bg=GOLD,
        bullets=[
            "<b>Prior Literature Foundations:</b>",
            (1, "<b>Brown et al. (2020) [Few-Shot ICL]</b>, <b>Liu et al. (2022) [KATE]</b> & <b>Johnson et al. (2021) [FAISS]:</b> Retrieving nearest-neighbor in-context exemplars via FAISS outperforms static prompts on single-turn NLP benchmarks."),
            (1, "<b>Rebedea et al. (2023) [NeMo Guardrails]</b>, <b>Yao et al. (2024) [τ-bench]</b> & <b>Acikgoz et al. (2025) [TD-EVAL]:</b> Prompt-only LLMs fail domain policy rules in >50% of multi-turn tool/booking interactions."),
            "<b>Where Prior Methods Stop & Solution Approach Operationalization:</b>",
            (1, "KATE retrieves from one <i>unpartitioned global pool</i> with raw unmasked entities (causing entity leakage). NeMo and τ-bench evaluate guardrails without dynamic persona style routing."),
            (1, "<b>Inspiration for RQ2-Personalize Stage & RQ3-Govern Stage:</b> Partition FAISS into <b>persona-specific `[SLOT]`-masked sub-indices (`RQ2-Personalize`)</b> and cross them factorially with a <b>deterministic `YAML` Rule Engine (`RQ3-Govern`)</b>."),
        ],
        font_size=9.8,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Foundation (Streams 3 & 4 → RQ1-Identify, RQ2-Personalize & RQ3-Govern):</b> "
        "Stream 3 inspires the <b>prefix-truncated hybrid `Blocks` clustering & router (`RQ1-Identify`)</b>; Stream 4's KATE/FAISS inspires <b>persona-partitioned exemplar prompting (`RQ2-Personalize`)</b>, while τ-bench and NeMo Guardrails inspire <b>symbolic `YAML` policy verification and `[SLOT]` sanitization (`RQ3-Govern`)</b>.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 9: 6-COLUMN LITERATURE RELEVANCE & STORYLINE OPERATIONALIZATION MATRIX (TABLE 2)
    # =========================================================================
    s = D.content_slide(
        "2. Literature Collection & Synthesis Aligned with Solution Approach",
        "Literature Relevance Matrix Mapped to the Four-Stage Solution Approach (Table 2)",
        "Mapping all 26 peer-reviewed sources across Streams 1–4 to their target solution stage and operationalized architecture component",
        notes="Walk through Table 2 from the Final Report, showing how every literature stream maps directly to Identify, Personalize, Govern, and Optimize.",
    )
    D.add_table(
        s, 0.35, 1.46, 12.63, 4.80,
        headers=[
            "Literature Stream & Representative Sources (26 Total)",
            "Core Prior Contribution",
            "Limitation When Applied Directly to Travel AI",
            "Solution Stage Mapped",
            "Inspiration & Operationalization in This Study",
        ],
        rows=[
            [
                "Stream 1: Hospitality AI & Buyer Behavior\nBuhalis & Sinarta (2019); Ivanov & Webster (2019); Melián-González et al. (2021); Jannach et al. (2021); Inaba et al. (2022)",
                "Real-time tourism co-creation, automation ROI models, and qualitative buyer initiative/flexibility traits.",
                "Relied on post-hoc surveys; did not build early-turn persona routers or measure turn-level slot redundancy.",
                "RQ1-Identify Stage\n&\nRQ4-Optimize Stage",
                "Operationalized qualitative traits into the 16-field `UserBehaviour` schema (`RQ1-Identify`) and defined `Turns to Goal Completion (ln TGC)` & `RER` (`RQ4-Optimize`).",
            ],
            [
                "Stream 2: Task-Oriented Dialogue Corpora\nEl Asri et al. (2017) [Frames]; Budzianowski et al. (2018); Zang et al. (2020) [MultiWOZ 2.2]; Walker et al. (1997) [PARADISE]",
                "Human Wizard-of-Oz travel package negotiations (`Frames`) and multi-domain slot tracking (`MultiWOZ`).",
                "Treated all travelers as one uniform population; lacked Tier-2 enterprise policy slots and persona routing.",
                "RQ1-Identify Stage\n&\nRQ4-Optimize Stage",
                "Used `Frames (N=1,334)` for archetype discovery & simulation seeding, `MultiWOZ (N=1,499)` for cross-corpus transfer (`RQ1-Identify`), and PARADISE quotation closure (`RQ4-Optimize`).",
            ],
            [
                "Stream 3: Embeddings, Clustering & LLM Coding\nReimers & Gurevych (2019) [SBERT]; Lee et al. (2025) [Gemini]; McInnes et al. (2017) [HDBSCAN]; Hennig (2007); Gilardi et al. (2023)",
                "Bi-encoder vector geometry, density/centroid clustering, bootstrap ARI stability, and zero-temp LLM annotation.",
                "Whole-dialogue embeddings confound wizard identity & end-of-chat outcomes; HDBSCAN drops >35% of speakers as noise.",
                "RQ1-Identify Stage",
                "Designed prefix-truncated (`M=9` user msgs) `46-d Blocks` (`PCA-20 Gemini + 13 LLM scales`), `K-Means (k=3, 100% cov.)`, and the L1 `RefinedArchetypeRouter`.",
            ],
            [
                "Stream 4a: Dynamic In-Context Learning\nBrown et al. (2020) [GPT-3 ICL]; Liu et al. (2022) [KATE]; Johnson et al. (2021) [FAISS]; Zhang et al. (2020) [BERTScore]",
                "Nearest-neighbor FAISS exemplar retrieval improves single-turn semantic accuracy over random few-shot.",
                "Global unrouted pool ignores persona pacing; raw exemplars leak stale hotel, airline, and price entities.",
                "RQ2-Personalize Stage",
                "Partitioned FAISS into `k=3` persona sub-indices (`IndexFlatIP(46)`) with `[SLOT]` placeholder masking and persona word-pacing directives.",
            ],
            [
                "Stream 4b: Dialogue Guardrails & Statistical Design\nRebedea et al. (2023) [NeMo]; Yao et al. (2024) [τ-bench]; Acikgoz et al. (2025); Cohen (1988); Wobbrock et al. (2011) [ART]",
                "Programmable rails, policy failure benchmarks, noncentral-F power analysis, and non-parametric factorial ANOVA.",
                "Tested safety rails in isolation without measuring how symbolic verification interacts with persona few-shot style.",
                "RQ3-Govern Stage\n&\nRQ4-Optimize Stage",
                "Built the deterministic `YAML` `RuleEngine` (`5 rules` + entity sanitizer) for the `2×2` RQ3-Govern governance test and the `Verified Informed Slot Ledger` for RQ4-Optimize.",
            ],
        ],
        col_widths=[2.6, 2.2, 2.4, 1.5, 3.9],
        font_size=9.1,
        align_left_cols=(0, 1, 2, 4),
        highlight_rows=(0, 1, 2, 3, 4),
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Synthesis:</b> No single prior stream solves consultative travel AI alone. The 4-stage solution approach is the direct operational synthesis of all four streams—joining <b>Stream 3 clustering (`Identify`)</b> + <b>Stream 4a FAISS ICL (`Personalize`)</b> + <b>Stream 4b symbolic guardrails (`Govern`)</b> + <b>Streams 1–2 turn-economy evaluation (`Optimize`)</b>.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 10: OPERATIONALIZATION SYNTHESIS — HOW LITERATURE BUILT THE 4-STAGE CASCADE
    # =========================================================================
    s = D.content_slide(
        "2. Literature Collection & Synthesis Aligned with Solution Approach",
        "Operationalization Synthesis: From Isolated Papers to a 4-Stage Cascade",
        "How specific methodological inspirations and failure modes in the literature shaped each stage's design and handoff",
        notes="Summarize the 4-paragraph literature operationalization synthesis added to Section 2.5 of the Final Report.",
    )
    D.add_card(
        s, 0.35, 1.48, 6.15, 2.32,
        title="1. Operationalizing RQ1-Identify Stage from Streams 1–3",
        header_bg=NAVY,
        bullets=[
            "<b>Literature Inspiration:</b> Qualitative shopper typologies (Jannach et al., 2021; Inaba et al., 2022) + bi-encoder embeddings (Reimers & Gurevych, 2019; Lee et al., 2025) + zero-temperature LLM coding (Gilardi et al., 2023) + bootstrap stability (Hennig, 2007).",
            "<b>Operational Adaptation in This Approach:</b> Standard document clustering embeds the whole transcript, which confounds who the shopper is with how the session ended (`outcome`). RQ1-Identify operationalizes <b>prefix-truncated (`M=9` user messages) hybrid `46-d Blocks` clustering</b> and a supervised L1 router so persona identification happens <i>early enough</i> to guide live generation.",
        ],
        font_size=9.4,
    )
    D.add_card(
        s, 6.80, 1.48, 6.18, 2.32,
        title="2. Operationalizing RQ2-Personalize Stage from Stream 4a",
        header_bg=TEAL,
        bullets=[
            "<b>Literature Inspiration:</b> Few-shot in-context learning (Brown et al., 2020) + KATE nearest-neighbor example selection (Liu et al., 2022) + exact inner-product FAISS indexing (Johnson et al., 2021).",
            "<b>Operational Adaptation in This Approach:</b> KATE retrieves from one undifferentiated global pool for single-turn tasks. RQ2-Personalize operationalizes <b>archetype-partitioned FAISS sub-indices (`1 per RQ1-Identify cluster`) paired with persona word-pacing directives</b>—and tests the causal hypothesis that KATE-style retrieval only improves style when RQ1-Identify prefix routing is coherent.",
        ],
        font_size=9.4,
    )
    D.add_card(
        s, 0.35, 3.92, 6.15, 2.32,
        title="3. Operationalizing RQ3-Govern Stage from Stream 4b",
        header_bg=CORAL,
        bullets=[
            "<b>Literature Inspiration:</b> NeMo Guardrails (Rebedea et al., 2023) + τ-bench policy compliance failures (Yao et al., 2024) + TD-EVAL multi-dimensional auditing (Acikgoz et al., 2025).",
            "<b>Operational Adaptation in This Approach:</b> Prior benchmarks showed that prompt-only LLMs fail domain rules, but did not test how guardrails interact with few-shot style adaptation. RQ3-Govern operationalizes a <b>`2 × 2` factorial crossing (`Rules Off/Active × Zero-Shot/Cluster-Adaptive`)</b> using `[SLOT]` exemplar masking, 5 declarative `YAML` rules, and post-generation sanitization.",
        ],
        font_size=9.4,
    )
    D.add_card(
        s, 6.80, 3.92, 6.18, 2.32,
        title="4. Operationalizing RQ4-Optimize Stage from Streams 1, 2 & 4b",
        header_bg=GREEN,
        bullets=[
            "<b>Literature Inspiration:</b> Hospitality automation ROI (Ivanov & Webster, 2019; Melián-González et al., 2021) + PARADISE task-resolution decoupling (Walker et al., 1997) + Frames package trade-offs (El Asri et al., 2017).",
            "<b>Operational Adaptation in This Approach:</b> RQ4-Optimize cascades the validated outputs of RQ1-Identify to RQ3-Govern (`Blocks` Router + `[SLOT]` FAISS + Active `RuleEngine`) and adds a <b>Verified Informed Slot Ledger</b> and <b>persona-specific package framing (`1-Opt Confirm / 3-Opt Compare / Dual Trade-Off`)</b> to compress multi-turn negotiations.",
        ],
        font_size=9.4,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Setting the Stage for Dataset & Exploratory Data Analysis (Next Section):</b> "
        "Before executing this 4-stage operational blueprint, the human dialogue corpora (`Microsoft Frames` and `MultiWOZ 2.2`) must be audited for data hygiene, partitioned behind a strict <b>70/30 zero-leakage firewall</b>, and explored across univariate, bivariate, and multivariate dimensions.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 11: DATASET AUTHENTICITY, ORIGIN & FIT FOR PURPOSE
    # =========================================================================
    s = D.content_slide(
        "3. Dataset Provenance, Hygiene & Exploratory Data Analysis",
        "Dataset Authenticity, Provenance, and Fit for Purpose",
        "Why Microsoft Frames (N = 1,334 analytic) and MultiWOZ 2.2 (N = 1,499 analytic) were created and how they anchor the 4-stage solution approach",
        notes="Explain the provenance and authenticity of Microsoft Frames and MultiWOZ 2.2, and how structural dataset boundaries are transparently bridged.",
    )
    D.add_card(
        s, 0.35, 1.48, 6.15, 3.20,
        title="Primary Corpus: Microsoft Frames (El Asri et al., 2017)",
        header_bg=NAVY,
        bullets=[
            "<b>Origin & Collection Protocol:</b> Collected by Maluuba / Microsoft Research across 12 human participants (85 user–wizard pairs) over 20 days in a Wizard-of-Oz environment connected to a database of flights and hotels.",
            "<b>Why It Was Created:</b> Standard corpora only tested linear slot-filling. Frames (1,369 raw dialogues; 19,986 turns) was specifically designed to capture <b>multi-turn consultative vacation package negotiation, budget ceilings, and non-linear frame-switching</b>.",
            "<b>Fit for the Solution Approach:</b> Contains authentic human behavioral heterogeneity—decisive buyers, multi-city explorers, and strict budget/star negotiators—plus 20+ dialogue act types (`inform`, `offer`, `switch_frame`).",
        ],
        font_size=9.8,
    )
    D.add_card(
        s, 6.80, 1.48, 6.18, 3.20,
        title="Comparison Corpus: MultiWOZ 2.2 (Zang et al., 2020)",
        header_bg=TEAL,
        bullets=[
            "<b>Origin & Collection Protocol:</b> Created at the University of Cambridge (Budzianowski et al., 2018; 10,438 dialogues) via crowd-sourced tourists and clerks, with Google-verified slot annotations in v2.2 (Zang et al., 2020).",
            "<b>Why It Was Created:</b> Gold-standard benchmark for supervised multi-domain Dialogue State Tracking (hotel, train, attraction, taxi, restaurant).",
            "<b>Role of the Seeded Sample (`N = 1,500 raw → 1,499 analytic`):</b> Serves as an external structural contrast in EDA and tests <b>cross-corpus domain specificity in RQ1-Identify Stage</b>—verifying whether consultative package negotiation archetypes are distinct from transactional city slot-filling.",
        ],
        font_size=9.8,
    )
    D.add_card(
        s, 0.35, 4.78, 12.63, 1.50,
        title="Transparently Bridging Two Public Corpus Boundaries (`RQ3-Govern` & `RQ4-Optimize`)",
        header_bg=GOLD,
        bg_color=CALLOUT_BG,
        bullets=[
            "<b>Boundary 1 — Zero Tier-2 Enterprise Policy Slots in Public Corpora (Appendix Table E4):</b> Programmatic audit of all 1,334 Frames dialogues confirmed that 0.0% record visa lead windows, passport expiry months, or promo discount percentages (only `budget_amount` is observed in 78.5%). <b>RQ3-Govern Solution:</b> Authentic held-out Frames user prefixes are preserved and paired with a deterministic, seeded (`seed=42`) experimental injector attaching controlled Tier-2 states (50% violating, 50% compliant).",
            "<b>Boundary 2 — Static Transcripts Cannot React to New Agent Policies in Multi-Turn Loops:</b> Corpus logs have fixed historical wizard replies. <b>RQ4-Optimize Solution:</b> Closed-loop simulations are grounded in the exact Tier-1 trip goals of 180 held-out Frames seeds and validated via blind `gemini-2.5-pro` persona auditing.",
        ],
        font_size=9.4,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`Data Foundation → RQ1-Identify to RQ4-Optimize`):</b> "
        "Microsoft Frames supplies the authentic human trajectories for <b>RQ1-Identify clustering</b> and <b>RQ2-Personalize FAISS exemplar indexing</b>, while its held-out test partition (`D_test = 401`) anchors the controlled <b>RQ3-Govern policy experiment</b> and <b>RQ4-Optimize closed-loop simulations</b>.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 12: TWO-TIER SCHEMA, DATA CLEANING AUDIT & 70/30 FIREWALL
    # =========================================================================
    s = D.content_slide(
        "3. Dataset Provenance, Hygiene & Exploratory Data Analysis",
        "Two-Tier Canonical Schema, Data Hygiene Audit & 70/30 Firewall",
        "Programmatic validation (`src/canonical_schema.py` & Table 5) and strict separation of Golden Discovery (n = 933) vs. Held-Out Test (n = 401)",
        notes="Walk through the Two-Tier Pydantic Schema, Table 5 cleaning audit, and the stratified 70/30 split firewall.",
    )
    D.add_card(
        s, 0.35, 1.48, 5.20, 3.45,
        title="Two-Tier Pydantic Schema (`src/canonical_schema.py`)",
        header_bg=NAVY,
        bullets=[
            "<b>Tier 1: Core Travel Booking Slots (9 Universal Fields)</b>",
            (1, "<i>origin_city</i> (98.4% observed in Frames)"),
            (1, "<i>destination_city</i> (99.1% in Frames; 92.2% in MultiWOZ)"),
            (1, "<i>departure_date</i> (96.0%) & <i>return_date</i> (91.2%)"),
            (1, "<i>duration_nights</i> (78.2%), <i>adults</i> (83.4%), <i>children</i> (25.0%)"),
            (1, "<i>budget_amount</i> in USD (78.5%) & <i>accommodation_tier</i> (69.5%)"),
            "<b>Tier 2: Enterprise Policy Guardrail Slots (5 Fields)</b>",
            (1, "<i>visa_processing_window_days</i> (< 15 days triggers warning)"),
            (1, "<i>passport_expiry_months</i> (< 6 months blocks international)"),
            (1, "<i>package_type</i> & <i>traveler_count_adults</i> (> 4 FIT escalates)"),
            (1, "<i>discount_applied_percentage</i> (> 15% capped by manager rule)"),
        ],
        font_size=9.8,
    )
    D.add_table(
        s, 5.75, 1.48, 7.23, 3.45,
        headers=["Quality Audit Check (Table 5)", "Detection Rule", "Frames (1,369)", "MultiWOZ (1,500)", "Programmatic Treatment"],
        rows=[
            ["Duplicate IDs / Empty turns", "Primary key / strip()", "0", "0", "Verified 100% unique & non-empty"],
            ["Exact duplicate text", "SHA-256 text hash", "1", "0", "Removed duplicate (`bf46892e...`)"],
            ["Aborted short dialogues", "total_turns < 3", "34", "1", "Excluded (need ≥ 3 turns for prefix routing)"],
            ["Long-tail turn outliers", "> Q3 + 1.5 × IQR", "20 (>30.5t)", "21 (>24.0t)", "Retained (real negotiations); log-transformed in RQ4-Optimize"],
            ["Unobserved slot values", "Slot never stated", "See Table E1", "See Table E1", "Preserved as null (`None`); never imputed"],
            ["Entity leakage risk", "Regex slot/number match", "All exemplars", "All exemplars", "Masked with `[SLOT]` tokens in FAISS index"],
            ["Final Analytic Sample", "Locked post-cleaning", "1,334", "1,499", "Total N = 2,833 analytic dialogues"],
        ],
        col_widths=[1.5, 1.4, 0.9, 0.9, 2.5],
        font_size=9.2,
        align_left_cols=(0, 1, 4),
        highlight_rows=(6,),
    )
    D.add_card(
        s, 0.35, 5.02, 12.63, 1.26,
        title="Stratified 70/30 Discovery-to-Evaluation Firewall (`seed = 42`)",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>70% Golden Discovery Partition (`D_gold`, n = 933; 74.3% wizard task success):</b> Exclusively used to fit all unsupervised clustering models (`K-Means, Ward, HDBSCAN`), the `PCA-20` projection matrix, the supervised L1 `RefinedArchetypeRouter`, and the 3 `[SLOT]`-masked FAISS `IndexFlatIP` exemplar sub-indices.",
            "<b>30% Held-Out Test Partition (`D_test`, n = 401; 74.1% wizard task success):</b> Strictly isolated for out-of-sample prefix routing evaluation (`RQ1-Identify`), repeated-measures prompting (`RQ2-Personalize, N = 33`), `2 × 2` compliance testing (`RQ3-Govern, N = 144`), and `2 × 3` closed-loop simulations (`RQ4-Optimize, N = 180`).",
        ],
        font_size=9.5,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`Zero-Leakage Handoff Across RQ1-Identify to RQ4-Optimize`):</b> "
        "Removing aborted `< 3`-turn fragments (`34` in Frames) guarantees every dialogue has a valid opening prefix for `RQ1-Identify`, while the <b>70/30 firewall</b> ensures that every `RQ1–RQ4` test statistic measures genuine out-of-sample generalization on `D_test (n = 401)`.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 13: UNIVARIATE & OUTCOME-STRATIFIED EXPLORATORY DATA ANALYSIS (FIGURE 1 & TABLE 6)
    # =========================================================================
    s = D.content_slide(
        "3. Dataset Provenance, Hygiene & Exploratory Data Analysis",
        "Univariate & Session-Outcome Stratified EDA (Figure 1 & Table 6)",
        "Distributional profiles across corpora, partitions, stated trip budgets, party composition, and session resolution outcomes",
        notes="Walk through Figure 1 and Table 6 from the expanded EDA section of the Final Report, emphasizing the session outcome stratification and why outcome cannot be used as a clustering input.",
    )
    D.add_figure(
        s, os.path.join(FIG_INT, "fig_eda_turns.png"),
        0.35, 1.48, 5.50, 4.78,
        caption="Figure 1: Turn-Count Distributions for Microsoft Frames (N = 1,334) vs. MultiWOZ 2.2 (N = 1,499)",
    )
    D.add_table(
        s, 6.00, 1.48, 6.98, 2.92,
        headers=["Corpus / Stratum & Variable (Table 6)", "N", "Mean (SD)", "Median (IQR)", "Min–Max", "Skewness"],
        rows=[
            ["Frames Total — Dialogue Turns", "1,334", "14.90 (6.74)", "15.0 (10.0)", "3–47", "+0.44"],
            ["Frames Golden (`D_gold`) / Test (`D_test`) Turns", "933 / 401", "14.94 / 14.81", "15.0 / 14.0", "3–45 / 3–47", "+0.40 / +0.52"],
            ["MultiWOZ 2.2 — Dialogue Turns", "1,499", "13.52 (4.46)", "14.0 (6.0)", "4–34", "+0.37"],
            ["Frames — Slot Revisions / Agent Offers", "1,334", "2.62 / 1.88", "2.0 / 1.0", "0–12 / 0–13", "+0.82 / +1.67"],
            ["Frames — Stated Trip Budget (USD)", "1,047", "$3,142 ($2,418)", "$2,500 ($2,300)", "$200–$18,000", "+2.14"],
            ["Outcome 1: Booked (65.6% of Frames)", "875", "15.61 (6.42) t", "2.81 rev | 2.19 off", "Decisiveness: 3.62", "Expl: 2.38"],
            ["Outcome 2: No Suitable Option (28.1%)", "375", "13.18 (7.15) t", "2.14 rev | 1.18 off", "Decisiveness: 2.89", "Expl: 1.94"],
            ["Outcome 3: Undecided / Exploring (6.2%)", "84", "15.22 (6.88) t", "2.79 rev | 1.77 off", "Decisiveness: 2.41", "Expl: 3.12"],
        ],
        col_widths=[2.35, 0.68, 1.05, 1.05, 1.00, 0.85],
        font_size=8.4,
        align_left_cols=(0,),
        highlight_rows=(0, 5, 6, 7),
    )
    D.add_card(
        s, 6.00, 4.50, 6.98, 1.76,
        title="Key Analytical Insights from Univariate & Outcome-Stratified EDA",
        header_bg=NAVY,
        bullets=[
            "<b>1. Consultative Dispersion & Party Mix:</b> Frames exhibits 51% wider turn dispersion than MultiWOZ (`SD = 6.74 vs. 4.46`) across diverse party types (`38.4% Solo/Couple, 25.0% Family with Children, 36.6% Multi-Adult Group`) and right-skewed budgets (`Skew = +2.14`).",
            "<b>2. Golden vs. Held-Out Partition Balance:</b> `D_gold (14.94t)` and `D_test (14.81t)` are statistically indistinguishable (`Welch t = 0.32, p = .748`), confirming an unbiased 70/30 split.",
            "<b>3. Crucial Outcome Asymmetry:</b> `No Suitable Option` sessions are shorter (`13.18t vs. 15.61t Booked, F = 17.42, p < .001`) with 46% fewer package offers (`1.18 vs. 2.19`) because rigid budget/star conflicts terminate early when unresolved.",
        ],
        font_size=8.9,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`Why EDA Dictates RQ1-Identify Truncation & RQ4-Optimize Log-Turns`):</b> "
        "Because session resolution (`Booked` vs. `No Suitable Option`) strongly alters total turns (`F = 17.42, p < .001`), clustering whole dialogues in `RQ1-Identify` would leak end-of-chat outcomes (<b>Red path</b>)—requiring <b>prefix truncation (`M = 9`) and excluding `outcome` (`Field 14`) from clustering</b>! Meanwhile, right-skewed turn/offer counts motivate `ln(Turns)` in `RQ4-Optimize`.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.2,
    )

    # =========================================================================
    # SLIDE 14: BIVARIATE PARAMETRIC & NON-PARAMETRIC EDA (FIGURE 2 & TABLE 7)
    # =========================================================================
    s = D.content_slide(
        "3. Dataset Provenance, Hygiene & Exploratory Data Analysis",
        "Bivariate Parametric (Pearson r) & Non-Parametric (Spearman ρ) EDA",
        "Figure 2 & Table 7: Validating negotiation constructs and discovering speaker verbosity independence across N = 1,334 Frames dialogues",
        notes="Walk through Figure 2 and Table 7, explaining why both Pearson r and Spearman rho are reported and how every bivariate relationship informs the 4-stage solution approach.",
    )
    D.add_figure(
        s, os.path.join(FIG_FIN, "fig_eda_bivariate.png"),
        0.35, 1.48, 5.55, 4.78,
        caption="Figure 2: Bivariate Turns vs. Slot Revisions (Panel A) & Archetype Negotiation Intensity (Panel B)",
    )
    D.add_table(
        s, 6.05, 1.48, 6.93, 2.85,
        headers=["Bivariate Variable Pair (Frames N = 1,334, Table 7)", "Pearson r (p)", "Spearman ρ (p)", "Solution Stage Implication"],
        rows=[
            ["Dialogue Turns × Slot Revisions", ".602 (< .001)", ".582 (< .001)", "Iterative constraint changes drive turn inflation (RQ4-Optimize)"],
            ["Dialogue Turns × Agent Package Offers", ".636 (< .001)", ".661 (< .001)", "Sequential 1-by-1 package quoting expands turns (RQ4-Optimize)"],
            ["Slot Revisions × Hesitation Markers", ".192 (< .001)", ".206 (< .001)", "Linguistic uncertainty tracks constraint shifts (RQ1-Identify)"],
            ["Slot Revisions × LLM Exploration Breadth", ".554 (< .001)", ".580 (< .001)", "Strong criterion validity of LLM codebook (RQ1-Identify)"],
            ["Dialogue Turns × LLM Decisiveness", "−.229 (< .001)", "−.222 (< .001)", "Decisive shoppers finish in fewer turns (RQ1-Identify & RQ4-Optimize)"],
            ["User Words/Turn × Agent Words/Turn", "−.026 (.341)", ".014 (.618)", "Human wizards fail to mirror user verbosity! (RQ2-Personalize)"],
        ],
        col_widths=[2.35, 1.00, 1.00, 2.58],
        font_size=8.8,
        align_left_cols=(0, 3),
        highlight_rows=(0, 1, 3, 5),
    )
    D.add_card(
        s, 6.05, 4.45, 6.93, 1.81,
        title="Three Analytical Conclusions from Bivariate EDA",
        header_bg=TEAL,
        bullets=[
            "<b>1. Concordance of Parametric (`r`) and Rank (`ρ`) Correlations:</b> Close agreement between linear Pearson `r` and rank-based Spearman `ρ` across all pairs confirms that relationships are structural and not artifacts of long-tail turn outliers.",
            "<b>2. Construct Validity of LLM Behavioral Ratings:</b> Zero-temperature LLM ratings of `exploration_breadth` (`ρ = .580`) and `decisiveness` (`ρ = −.222`) strongly track ground-truth human slot revisions and turn counts.",
            "<b>3. Speaker Verbosity Independence (`r = −.026, p = .341`):</b> Utterance length is completely uncorrelated between traveler and human wizard (`M = 12.69 vs. 19.65 words/turn`), proving that unguided responses do not naturally calibrate to user pacing.",
        ],
        font_size=8.9,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`Bivariate EDA → RQ1-Identify, RQ2-Personalize & RQ4-Optimize`):</b> "
        "Strong correlation between LLM ratings and ground-truth revisions (`ρ = .580`) validates the `RQ1-Identify` behavioral codebook; speaker verbosity independence (`r = −.026`) proves `RQ2-Personalize Stage` must inject explicit <b>persona word-pacing directives</b>; and revision/offer turn inflation (`r = .602/.636`) motivates `RQ4-Optimize` comparative & trade-off quoting.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.2,
    )

    # =========================================================================
    # SLIDE 15: MULTIVARIATE EDA — SPEARMAN MATRIX & PCA BIPLOT (FIGURE 3)
    # =========================================================================
    s = D.content_slide(
        "3. Dataset Provenance, Hygiene & Exploratory Data Analysis",
        "Multivariate EDA: Correlation Structure & Principal Component Biplot",
        "Figure 3: Ten structural and behavioral variables span three orthogonal dimensions explaining 68.6% of total variance",
        notes="Explain Figure 3 (Panel A Spearman heatmap and Panel B PCA biplot) and how the continuous 3D manifold informs RQ1-Identify clustering.",
    )
    D.add_figure(
        s, os.path.join(FIG_FIN, "fig_eda_multivariate.png"),
        0.35, 1.48, 7.35, 4.78,
        caption="Figure 3: Multivariate Spearman Rank Correlation Matrix (Panel A) & PCA Biplot by Refined Archetype (Panel B)",
    )
    D.add_table(
        s, 7.85, 1.48, 5.13, 3.05,
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
        col_widths=[2.0, 1.04, 1.04, 1.05],
        font_size=8.8,
        align_left_cols=(0,),
        highlight_rows=(0, 1, 2, 7, 8),
    )
    D.add_card(
        s, 7.85, 4.62, 5.13, 1.64,
        title="Interpreting the 3 Orthogonal Principal Components",
        header_bg=NAVY,
        bullets=[
            "<b>PC1 (40.8% var.) — Exploration vs. Rigidity:</b> Loaded on slot revisions (`+.416`), exploration breadth (`+.392`), and turns (`+.390`). Separates <i>Open Explorers</i> from <i>Rigid-Constraint Seekers</i>.",
            "<b>PC2 (17.2% var.) — Decisiveness & Price Focus:</b> Loaded on decisiveness (`−.509`) and price sensitivity (`−.426`). Isolates <i>Decisive Bookers</i>.",
            "<b>PC3 (10.6% var.) — Utterance Verbosity:</b> Dominated by user words per turn (`+.893`).",
        ],
        font_size=8.8,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Alignment (`Multivariate Manifold Geometry → RQ1-Identify Clustering Choice`):</b> "
        "Panel B of Figure 3 reveals that traveler behavior forms a <b>continuous, overlapping 3-dimensional manifold (`PC1–PC3 = 68.6% variance`)</b> rather than disjoint islands with empty density valleys—explaining why density-based `HDBSCAN` discards >35% of speakers as noise (<b>Red</b>) while centroid-based `K-Means (k = 3)` cleanly partitions the three directional poles (<b>Green</b>).",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.2,
    )

    # =========================================================================
    # SLIDE 16: EDA-TO-STORYLINE HANDOFF SUMMARY
    # =========================================================================
    s = D.content_slide(
        "3. Dataset Provenance, Hygiene & Exploratory Data Analysis",
        "EDA-to-Solution Handoff: How Exploratory Findings Shape RQ1-Identify to RQ4-Optimize",
        "Synthesizing what Exploratory Data Analysis proves, what it rules out, and what design constraints it passes to the methodology",
        notes="Bridge the completed EDA section directly to the RQs and Methodology section, showing how every EDA diagnostic informed a concrete design choice in RQ1-Identify to RQ4-Optimize.",
    )
    D.add_table(
        s, 0.35, 1.48, 12.63, 4.78,
        headers=[
            "Exploratory Data Analysis Finding",
            "Empirical EDA Metric (Tables 5–7, E4 & Figs. 1–3)",
            "What Is Ruled Out / Dropped (Red Path ✗)",
            "What Is Passed into the 4-Stage Solution Approach Design (Green Path ✓)",
        ],
        rows=[
            [
                "1. Aborted Fragments &\nPartition Balance",
                "`34` Frames chats `< 3` turns removed;\n`D_gold (14.94t)` vs `D_test (14.81t)`, `p = .748`.",
                "✗ Evaluating routing or prompting on uncleaned fragments or leaky in-sample data.",
                "✓ <b>All Stages:</b> Strict <b>70/30 Firewall (`D_gold = 933` vs. `D_test = 401`)</b> ensures every test evaluates out-of-sample generalization.",
            ],
            [
                "2. Session Outcome\nConfounding (`Table 6`)",
                "`Booked (65.6%, 15.61t)` vs. `No Option (28.1%, 13.18t)` vs. `Undecided (6.2%, 15.22t)`, `F = 17.42, p < .001`.",
                "✗ Using whole-dialogue transcripts or `outcome` (`Field 14`) as clustering features.",
                "✓ <b>RQ1-Identify Stage:</b> Truncate clustering inputs to <b>opening user prefixes (`M = 9`)</b> and hold out `Fields 14–16` strictly for post-hoc audit.",
            ],
            [
                "3. Continuous 3D Behavioral\nManifold (`Figure 3`)",
                "`PC1 (40.8% Exploration)`, `PC2 (17.2% Decisiveness)`, `PC3 (10.6% Verbosity)` = `68.6%` variance.",
                "✗ Assuming disjoint density islands where `HDBSCAN` can retain all speakers.",
                "✓ <b>RQ1-Identify Stage:</b> Benchmark `K-Means (k=3)` vs. `Ward` vs. `HDBSCAN` and fuse `PCA-20` prefix embeddings with the 16-field LLM codebook (`46-d Blocks`).",
            ],
            [
                "4. Speaker Verbosity\nIndependence (`Table 7`)",
                "User words/turn × Wizard words/turn:\n`r = −.026 (p = .341)`, `ρ = .014 (p = .618)`.",
                "✗ Relying on zero-shot or unrouted prompts to naturally match user pacing.",
                "✓ <b>RQ2-Personalize Stage:</b> Pair persona-partitioned FAISS exemplars with explicit <b>persona word-pacing directives</b> (`word_abs_err` metric).",
            ],
            [
                "5. Zero Public Tier-2\nPolicy Slots (`Table E4`)",
                "`0.0%` of 1,334 Frames chats log visa days, passport months, FIT cap, or promo % (`budget` = 78.5%).",
                "✗ Testing enterprise policy compliance on unannotated raw corpus replies alone.",
                "✓ <b>RQ3-Govern Stage:</b> Pair authentic `D_test` user prefixes with a seeded (`seed=42`) <b>Tier-2 policy injector</b> (`50% violating / 50% compliant`) across a `2 × 2` design.",
            ],
            [
                "6. Right-Skewed Turns &\nNegotiation Loops (`Figs. 1–2`)",
                "Turns × Revisions `r = .602`; Turns × Offers `r = .636`; positive skewness `+0.44` to `+1.67`.",
                "✗ Sequential 1-option quoting & unlogged slot elicitation; testing raw turns alone.",
                "✓ <b>RQ4-Optimize Stage:</b> Specify <b>`Y = ln(TGC)` alongside Raw Turns & `RER`</b>, and test the `Verified Informed Slot Ledger` + persona package policies (`2 × 3`).",
            ],
        ],
        col_widths=[2.2, 2.8, 3.2, 4.43],
        font_size=8.9,
        align_left_cols=(0, 1, 2, 3),
        highlight_rows=(0, 1, 2, 3, 4, 5),
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Transition to Research Questions & Methodology (Next Section):</b> "
        "Every design choice in the upcoming Methodology section (`Slides 17–24`) directly operationalizes these six EDA findings—establishing a transparent, pre-declared experimental protocol before any hypothesis test is run.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 17: THE FOUR LINKED RESEARCH QUESTIONS & HYPOTHESES (METHODOLOGY ONLY)
    # =========================================================================
    s = D.content_slide(
        "4. Experimental Design & Statistical Methodology",
        "Research Questions & Hypotheses Mapped to the Four-Stage Solution Approach",
        "Formal specification of RQ1–RQ4, manipulated IVs (X), measured DVs (Y), and null/alternative hypotheses (Methodology Only)",
        notes="Present the four research questions and formal hypotheses without any post-hoc empirical numbers—strictly methodology and expected relationships.",
    )
    D.add_table(
        s, 0.35, 1.46, 12.63, 4.80,
        headers=[
            "Solution Stage & RQ",
            "Formal Research Question",
            "Manipulated Independent Variable (X)",
            "Measured Dependent Variables (Y)",
            "Formal Hypotheses (H0 vs. Ha)",
            "Role in the 4-Stage Solution Approach Cascade",
        ],
        rows=[
            [
                "RQ1-Identify: IDENTIFY\n(RQ1 — Discovery &\nEarly Routing)",
                "Which clustering algorithm best separates travel trajectories, and which early-routable user archetypes emerge from opening prefixes?",
                "<b>X<sub>1</sub>:</b> Clustering Algorithm (`K-Means, Ward, HDBSCAN`) × Prefix Horizon `M ∈ {3, 5, 7, 9, whole}` × Representation (`Embeddings, LLM Codebook, 46-d Blocks`)",
                "<b>Y<sub>1</sub>:</b> Cosine Silhouette, Davies–Bouldin Index, Bootstrap `ARI` Stability, and Held-Out Prefix Routing `κ`, Accuracy & `Macro-F1`",
                "<b>H<sub>01</sub>:</b> `μ_Sil` equal across algorithms.\n<b>H<sub>a1</sub>:</b> Algorithms differ (`p < .05`) & prefix `Blocks` yields stable (`ARI ≥ .60`), routable personas.",
                "Establishes the 3 traveler archetypes, the live prefix router, and the 3 partitioned FAISS exemplar sub-indices passed to RQ2-Personalize.",
            ],
            [
                "RQ2-Personalize: PERSONALIZE\n(RQ2 — Style &\nPacing ICL)",
                "Does cluster-adaptive few-shot prompting improve style convergence and pacing calibration over static few-shot and zero-shot baselines?",
                "<b>X<sub>2</sub>:</b> Prompting Strategy (`Zero-Shot`, `Static Few-Shot k=3`, `Cluster-Adaptive Few-Shot k=3` with persona pacing directives)",
                "<b>Y<sub>2</sub>:</b> De-lexicalized SBERT Style Cosine (primary), Gemini 3,072-d Cosine, `BERTScore F1`, and Pacing Calibration Error `|W_gen − μ_k|`",
                "<b>H<sub>02</sub>:</b> `μ_style` & `μ_pacing` equal across all 3 prompt modes.\n<b>H<sub>a2</sub>:</b> `Cluster-Adaptive` > `Static` & `Zero-Shot` (`p < .05`).",
                "Tests whether routing into RQ1-Identify's persona FAISS sub-indices improves LLM conversational style & pacing, while exposing rule/leakage risks for RQ3-Govern.",
            ],
            [
                "RQ3-Govern: GOVERN\n(RQ3 — Symbolic\nPolicy & Leakage)",
                "How do a declarative rule engine and cluster-adaptive prompting interact to govern policy compliance, entity leakage, and slot F1?",
                "<b>X<sub>3</sub>:</b> `2 × 2` Factorial Crossing:\n`Factor A (Rules Mode)`: `Off` vs. `Active`\n`Factor B (Prompting)`: `Zero-Shot` vs. `Cluster-Adaptive`",
                "<b>Y<sub>3</sub>:</b> Rule Adherence Rate (`RAR`: Viol. Sens. & Comp. Spec.)\n<b>Y<sub>4</sub>:</b> Exemplar Entity Leakage (`ELR`)\n<b>Y<sub>5</sub>:</b> Factual `Slot F1` & Style Cosine",
                "<b>H<sub>03</sub>:</b> No main or `2 × 2` interaction effects.\n<b>H<sub>a3</sub>:</b> `Rules Active` raises `RAR` & `Slot F1` and eliminates few-shot leakage (`Int. p < .05`).",
                "Proves how symbolic `YAML` verification and `[SLOT]` masking interact with RQ2-Personalize's adaptive prompting to deliver safe, compliant personalization for RQ4-Optimize.",
            ],
            [
                "RQ4-Optimize: OPTIMIZE\n(RQ4 — Multi-Turn\nTurn Economy)",
                "Does governed cluster-adaptive prompting with an informed-slot ledger reduce turns to quotation agreement and redundant questions across archetypes?",
                "<b>X<sub>4</sub>:</b> `2 × 3` Factorial Crossing:\n`Factor A (Prompting)`: `Zero-Shot` vs. `Cluster-Adaptive (Full Stack)`\n`Factor B (Archetype)`: `DB, OE, RCS`",
                "<b>Y<sub>6</sub>:</b> Natural-Log Turns to Goal Completion (`ln TGC`, primary), Raw Turns (`TGC`), and Redundant Elicitation Rate (`RER`)",
                "<b>H<sub>04</sub>:</b> No main or `2 × 3` interaction effects.\n<b>H<sub>a4</sub>:</b> `Cluster-Adaptive` cuts `ln(TGC)` & `RER` with a `Prompt × Archetype` interaction (`p < .05`).",
                "Culmination of the solution approach: tests whether the combined `RQ1-Identify + RQ2-Personalize + RQ3-Govern` engine + `Slot Ledger` achieves business turn economy across all 3 personas.",
            ],
        ],
        col_widths=[1.65, 2.25, 2.25, 2.15, 2.15, 2.18],
        font_size=8.9,
        align_left_cols=(0, 1, 2, 3, 4, 5),
        highlight_rows=(0, 1, 2, 3),
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Methodology Link:</b> Notice that the four RQs are not independent studies: <b>`Y1` (RQ1-Identify's validated archetypes, router, and FAISS sub-indices)</b> becomes the routing mechanism for <b>`X2` (RQ2-Personalize)</b>, the adaptive arm of <b>`X3` (RQ3-Govern)</b>, and <b>Factor B of `X4` (RQ4-Optimize)</b>.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 18: PICTORIAL METHODOLOGY BLUEPRINT OF IVs, DVs, TESTS & BULLET-PROOFING
    # =========================================================================
    add_pictorial_methodology_slide(D)

    # =========================================================================
    # SLIDE 19: WHY EACH STATISTICAL TEST WAS CHOSEN + REAL-WORLD ANALOGIES (METHODOLOGY ONLY)
    # =========================================================================
    s = D.content_slide(
        "4. Experimental Design & Statistical Methodology",
        "Why Each Statistical Test Was Chosen & Everyday Real-World Analogies",
        "Mathematical justification and intuitive real-world parallels for the primary parametric tests in RQ1-Identify to RQ4-Optimize (Methodology Only)",
        notes="Explain WHY One-Way ANOVA, Repeated-Measures ANOVA, 2x2 Factorial ANOVA, and 2x3 Factorial ANOVA are mathematically required, without presenting empirical results yet.",
    )
    D.add_table(
        s, 0.35, 1.46, 12.63, 4.80,
        headers=[
            "Solution Stage & Experimental Structure",
            "Chosen Primary Statistical Test",
            "Why This Exact Test Is Mathematically Required",
            "Everyday Real-World Analogy",
            "Alignment With the Conversational AI Scenario",
        ],
        rows=[
            [
                "RQ1-Identify Stage:\nComparing 3 Clustering Algorithms across N = 159 subsample runs\n(3 groups, continuous DV: Silhouette)",
                "One-Way Between-Subjects ANOVA\n+ Matched Subsample RM-ANOVA\n+ Tukey HSD / Games–Howell",
                "Comparing means of k = 3 groups simultaneously. Running 3 separate t-tests inflates Type I false-positive risk from 5% to 1 − (0.95)³ = 14.3%. Omnibus ANOVA preserves α = .05, while Matched RM-ANOVA controls for shared subsample seeds.",
                "<b>Clinical Trial Comparing 3 Blood-Pressure Drugs:</b>\n159 cohorts (53 per drug) assigned to Drug A, Drug B, or Drug C to compare mean blood-pressure reduction.",
                "Each of the 159 subsample runs (53 K-Means, 53 Ward, 53 HDBSCAN on 80% draws of D_gold) yields a continuous Cosine Silhouette score.",
            ],
            [
                "RQ2-Personalize Stage:\nTesting 3 Prompting Strategies on the SAME N = 33 held-out dialogues\n(Within-subjects design, 99 calls)",
                "One-Way Repeated-Measures ANOVA\n(Greenhouse–Geisser ε correction)\n+ Holm Step-Down Paired t-tests",
                "Every held-out dialogue is evaluated under ALL 3 prompt strategies. Repeated-Measures ANOVA partitions out baseline dialogue-to-dialogue difficulty variance (ρ), isolating the pure within-dialogue effect of the prompt.",
                "<b>Coffee Tasting Panel (Crossover Trial):</b>\nThe same 33 expert tasters rate Blend A, Blend B, and Blend C. Subtracting taster-level harshness vastly increases sensitivity.",
                "Travel dialogues vary widely in complexity. Testing Zero-Shot, Static, and Cluster-Adaptive on the exact same 33 dialogue prefixes removes topic noise.",
            ],
            [
                "RQ3-Govern Stage:\nCrossing Rules Mode (2) × Prompting Strategy (2)\n(Balanced 2 × 2 design, N = 144, n = 36/cell)",
                "2 × 2 Between-Subjects Factorial OLS ANOVA\n(Orthogonal Type II/III Sum Contrasts)",
                "Two independent factors (Rules Mode and Prompting Mode) are manipulated simultaneously. Only a 2 × 2 Factorial ANOVA can test (1) Main Effect of Rules, (2) Main Effect of Prompting, and (3) their INTERACTION (Rules × Prompting).",
                "<b>Agricultural Crop Trial (Fertilizer × Irrigation):</b>\nTesting whether Fertilizer boosts yield only when Irrigation is ALSO active (a synergistic or protective interaction).",
                "Tests whether symbolic rule verification interacts with few-shot prompting to suppress exemplar entity leakage while preserving style.",
            ],
            [
                "RQ4-Optimize Stage:\nCrossing Prompting (2) × Traveler Archetype (3)\n(Balanced 2 × 3 design, N = 180, n = 30/cell)",
                "2 × 3 Between-Subjects Factorial ANOVA on Y = ln(Turns), Raw Turns & RER\n+ Within-Archetype Contrasts",
                "Tests whether turn-saving gains from Cluster-Adaptive prompting are uniform across all travelers (Main Effect A) or moderated by Traveler Archetype (A × B Interaction), using natural-log turns to normalize right-skewed count data.",
                "<b>Education Trial (Teaching Method × Learning Style):</b>\nTesting whether interactive tutoring vs. lecture helps Visual, Auditory, and Hands-On learners by different magnitudes.",
                "Evaluates whether Decisive Bookers, Open Explorers, and Rigid-Constraint Seekers experience differential turn compression from persona-tailored policies.",
            ],
        ],
        col_widths=[2.0, 2.0, 2.8, 2.8, 3.03],
        font_size=9.2,
        align_left_cols=(0, 1, 2, 3, 4),
        highlight_rows=(0, 1, 2, 3),
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Methodology Link:</b> The statistical design evolves alongside the 4-stage solution approach—moving from <b>unsupervised cluster evaluation (`RQ1-Identify`)</b> to <b>within-dialogue crossover prompting (`RQ2-Personalize`)</b>, <b>`2 × 2` safety × style factorial governance (`RQ3-Govern`)</b>, and <b>`2 × 3` policy × persona multi-turn optimization (`RQ4-Optimize`)</b>.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 20: MATHEMATICAL MECHANICS OF ANOVA, EFFECT SIZES & BULLET-PROOFING (METHODOLOGY ONLY)
    # =========================================================================
    s = D.content_slide(
        "4. Experimental Design & Statistical Methodology",
        "Mathematical Mechanics of ANOVA, Effect Sizes & Bullet-Proofing Triad",
        "Signal-to-noise F-ratios, variance-accounted-for metrics (η², ηp², d), and distribution-free robustness checks (Methodology Only)",
        notes="Explain F-ratios, eta-squared, Cohen's d, Greenhouse-Geisser, Welch/HC3, and Aligned Rank Transform (ART) purely as methodology.",
    )
    D.add_card(
        s, 0.35, 1.48, 4.05, 2.35,
        title="1. The F-Statistic: Signal-to-Noise Ratio",
        header_bg=NAVY,
        bullets=[
            "<b>Formula:</b>  <i>F</i> = MS<sub>between</sub> / MS<sub>within (error)</sub>",
            "<b>Mathematical Intuition:</b>",
            (1, "<b>Numerator (Signal):</b> Systematic variance between experimental treatment means."),
            (1, "<b>Denominator (Noise):</b> Unexplained residual variance within experimental cells."),
            (1, "Under the null hypothesis <i>H</i><sub>0</sub>, <i>F</i> ≈ 1.0; values exceeding critical threshold <i>F</i><sub>crit</sub> (at α = .05) reject <i>H</i><sub>0</sub>."),
        ],
        font_size=9.5,
    )
    D.add_card(
        s, 4.60, 1.48, 4.10, 2.35,
        title="2. Effect Sizes (η², ηp², and Cohen's d)",
        header_bg=TEAL,
        bullets=[
            "<b>Partial Eta-Squared:</b>  η<sub><i>p</i></sub><sup>2</sup> = SS<sub>effect</sub> / (SS<sub>effect</sub> + SS<sub>error</sub>)",
            (1, "Quantifies the exact proportion of variance explained by a factor after partialling out other factors."),
            (1, "<b>Cohen's (1988) Benchmarks:</b> Small η<sup>2</sup> = .01 (`f=.10`), Medium η<sup>2</sup> = .06 (`f=.25`), Large η<sup>2</sup> ≥ .14 (`f≥.40`)."),
            "<b>Standardized Mean Difference (`Cohen's d / d_z`):</b>",
            (1, "Measures pairwise shift in standard deviation units (`|d| ≥ 0.80` = large practical magnitude)."),
        ],
        font_size=9.5,
    )
    D.add_card(
        s, 8.90, 1.48, 4.08, 2.35,
        title="3. Main Effects vs. Factorial Interactions (A × B)",
        header_bg=BLUE,
        bullets=[
            "<b>Main Effect (A or B):</b> Average effect of one factor collapsed across levels of the other factor.",
            "<b>Interaction Effect (A × B):</b> Tests whether the effect of Factor A <i>depends on</i> the active level of Factor B.",
            "<b>Geometric Diagnostic on Interaction Plots:</b>",
            (1, "<b>Parallel lines</b> = Additive main effects only (`Interaction F ≈ 1.0`)."),
            (1, "<b>Non-parallel / diverging lines</b> = Significant moderation / protective interaction!"),
        ],
        font_size=9.5,
    )
    D.add_table(
        s, 0.35, 3.94, 12.63, 2.34,
        headers=[
            "Potential Distributional Violation",
            "Where It Can Arise in Dialogue Experiments",
            "Heteroscedasticity-Robust Parametric Check",
            "Distribution-Free Non-Parametric Check",
        ],
        rows=[
            [
                "1. Unequal Cell Variances\n(Heteroscedasticity / Zero-Variance Boundary)",
                "When a guardrail or slot ledger drives error rates (`ELR, RER`) to `0.000` or turn counts to a deterministic floor (`SD = 0.00`).",
                "<b>Welch's ANOVA (RQ1-Identify) & MacKinnon–White HC3 Sandwich SEs (RQ3-Govern & RQ4-Optimize):</b> Avoids pooled variance assumptions.",
                "<b>Games–Howell Post Hoc (RQ1-Identify) & Mann–Whitney U (RQ4-Optimize):</b> Rank-based pairwise comparisons.",
            ],
            [
                "2. Bounded Proportions `[0, 1]`\n& Floor/Ceiling Clustering",
                "Rule Adherence (`RAR`), Entity Leakage (`ELR`), `Slot F1` (RQ3-Govern), and Redundant Elicitation (`RER`, RQ4-Optimize).",
                "<b>Balanced Factorial Cells (`n = 36`/cell in RQ3-Govern; `n = 30`/cell in RQ4-Optimize):</b> Maximizes ANOVA robustness under CLT.",
                "<b>Aligned Rank Transform (ART) Factorial ANOVA (Wobbrock et al., 2011):</b> Aligns effects before ranking for exact non-parametric main & interaction tests.",
            ],
            [
                "3. Sphericity Departure (`ε < 1.0`)\n& Right-Skewed Turn Counts",
                "Correlated within-dialogue differences across 3 prompts (RQ2-Personalize); positive right-skewed multi-turn counts (RQ4-Optimize).",
                "<b>Greenhouse–Geisser (`ε`) df Adjustment (RQ2-Personalize) & Natural-Log Transformation `Y = ln(TGC)` (RQ4-Optimize).</b>",
                "<b>Friedman Rank Test `χ²(2)` (RQ2-Personalize) & Kruskal–Wallis `H` (RQ1-Identify):</b> Invariant to monotone transformations.",
            ],
        ],
        col_widths=[2.5, 3.3, 3.4, 3.43],
        font_size=8.8,
        align_left_cols=(0, 1, 2, 3),
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Bullet-Proofing Rule:</b> To ensure that no stage handoff in `Identify → Personalize → Govern → Optimize` can be challenged on normality, skewness, or zero-variance boundary grounds, every hypothesis test is pre-specified as a <b>Parametric + Robust (Welch/HC3) + Non-Parametric (Kruskal/Friedman/ART) triad</b>.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 21: A PRIORI SAMPLE-SIZE DERIVATION VIA NONCENTRAL-F (METHODOLOGY ONLY)
    # =========================================================================
    s = D.content_slide(
        "4. Experimental Design & Statistical Methodology",
        "A Priori Sample-Size Derivation via the Noncentral-F Distribution",
        "Table 8 & Equation 1: How α = .05, Power (1 − β) = .80, Cohen's f = .25, and Noncentrality λ determine exact sample sizes (Methodology Only)",
        notes="Explain alpha, beta, power, Cohen's f, and noncentrality lambda purely from a priori power methodology (`step0_sample_size.py`).",
    )
    D.add_card(
        s, 0.35, 1.48, 5.95, 3.40,
        title="The Noncentral-F Power Formulation (`step0_sample_size.py`)",
        header_bg=NAVY,
        bullets=[
            "<b>Exact Power Equation (Equation 1 — Cohen, 1988; Faul et al., 2007):</b>",
            (1, "<b>Power (1 − β) = 1 − <i>F</i><sub>nc</sub>(<i>F</i><sub>crit</sub> ; <i>df</i><sub>1</sub>, <i>df</i><sub>2</sub>, λ)</b>,  where <i>F</i><sub>crit</sub> = <i>F</i><sub>1−α</sub>(<i>df</i><sub>1</sub>, <i>df</i><sub>2</sub>)"),
            "<b>Four Standard A Priori Design Parameters:</b>",
            (1, "<b>1. Significance Level (α = .05):</b> 5% maximum Type I false-positive risk under <i>H</i><sub>0</sub>."),
            (1, "<b>2. Statistical Power (1 − β ≥ .80, β ≤ .20):</b> 80% minimum probability of detecting a true effect under <i>H</i><sub>a</sub> (standard 4:1 β-to-α weighting)."),
            (1, "<b>3. Minimum Detectable Effect Size (<i>f</i> = .25):</b> Medium effect benchmark where signal SD is 25% of error SD (equivalent to η<sup>2</sup> = <i>f</i><sup>2</sup> / (1 + <i>f</i><sup>2</sup>) = .0588, or ~6% variance)."),
            (1, "<b>4. Noncentrality Parameter (λ):</b> Shifts the <i>F</i> distribution under <i>H</i><sub>a</sub>:\n"
                "      • Between-subjects (RQ1-Identify, RQ3-Govern, RQ4-Optimize):  <b>λ = <i>f</i><sup>2</sup> · <i>N</i></b>\n"
                "      • Repeated-measures (RQ2-Personalize, <i>m</i>=3, ρ=.50):  <b>λ = <i>f</i><sup>2</sup> · <i>N</i> · <i>m</i> · ε / (1 − ρ)</b>"),
        ],
        font_size=9.5,
    )
    D.add_table(
        s, 6.50, 1.48, 6.48, 3.40,
        headers=["Stage (RQ)", "Planned Design", "df at N_min", "λ at N_min", "F_crit", "N_min (.80)", "Final N (+≥10% Buffer)", "A Priori Power"],
        rows=[
            ["RQ1-Identify", "One-way ANOVA (3 algs)", "2, 155", "9.88", "3.05", "158", "159 (n = 53 / alg)", ".804"],
            ["RQ2-Personalize", "RM-ANOVA (3 conds, ρ=.50)", "2, 54", "10.50", "3.17", "28", "33 (99 eval calls)", ".865"],
            ["RQ3-Govern", "2 × 2 Factorial (df1 = 1)", "1, 124", "8.00", "3.92", "128", "144 (n = 36 / cell)", ".847"],
            ["RQ4-Optimize", "2 × 3 Factorial (df1 = 2)", "2, 152", "9.88", "3.06", "158", "180 (n = 30 / cell)", ".857"],
        ],
        col_widths=[0.95, 1.55, 0.72, 0.68, 0.58, 0.68, 1.25, 0.72],
        font_size=9.2,
        align_left_cols=(0, 1),
        highlight_rows=(0, 1, 2, 3),
    )
    D.add_card(
        s, 0.35, 4.98, 12.63, 1.30,
        title="Step-by-Step Algebraic Derivation of N_min and the +10% Cell-Balancing Buffer",
        header_bg=TEAL,
        bullets=[
            "<b>1. Solving for `N_min` when `df_1 = 1` (RQ3-Govern Main Effect & 2 × 2 Interaction):</b> Achieving 80% power at α = .05 (`F_crit = 3.92`) requires noncentrality shift <b>λ ≈ 8.00</b>. Substituting <i>f</i><sup>2</sup> = (0.25)<sup>2</sup> = 0.0625 into λ = <i>f</i><sup>2</sup> · <i>N</i> gives <b><i>N</i><sub>min</sub> = 8.00 / 0.0625 = 128</b> (`32/cell`), buffered by +12.5% to <b><i>N</i> = 144 (`n = 36/cell`, 12 per archetype per cell, power = .847)</b>.",
            "<b>2. Solving for `N_min` when `df_1 = 2` (RQ1-Identify Algorithms & RQ4-Optimize 2 × 3 Interaction):</b> With 2 numerator <i>df</i> (`F_crit ≈ 3.05`), 80% power requires <b>λ ≈ 9.88</b>, yielding <b><i>N</i><sub>min</sub> = 9.88 / 0.0625 = 158</b>—buffered to <b><i>N</i> = 159 (`53 × 3` in RQ1-Identify, power = .804)</b> and <b><i>N</i> = 180 (`30 × 6` in RQ4-Optimize, power = .857)</b>.",
            "<b>3. Solving for `N_min` in Repeated-Measures RQ2-Personalize (`m = 3, ρ = .50`):</b> Within-subject correlation ρ = .50 halves residual error variance, multiplying λ by <i>m</i> / (1 − ρ) = 6 and requiring only <b><i>N</i><sub>min</sub> = 28 dialogues</b>, buffered by +17.9% to <b><i>N</i> = 33 (`11` per archetype × 3 prompts = `99` calls, power = .865)</b>.",
        ],
        font_size=9.1,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Methodology Link:</b> Every stage of `Identify → Personalize → Govern → Optimize` is powered a priori (`1 − β = .804 to .865`) so that all four experiments fit cleanly inside the <b>401 held-out test dialogues (`D_test`)</b> while guaranteeing sensitivity to medium-or-larger effects (`f ≥ .25`).",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 22: COUNTERFACTUAL METHODOLOGY ANALYSIS & DOMAIN HYPERPARAMETERS (METHODOLOGY ONLY)
    # =========================================================================
    s = D.content_slide(
        "4. Experimental Design & Statistical Methodology",
        "Counterfactual Parameter Analysis & Domain Hyperparameter Design",
        "Why improper choices of α, 1 − β, f, λ, or ρ break validity, and how turn decay λ_d = 0.15 & prefix horizon M are formulated (Methodology Only)",
        notes="Walk through the counterfactual parameter scenarios and the mathematical formulation of exponential turn decay lambda_d = 0.15 and prefix truncation horizon M.",
    )
    D.add_table(
        s, 0.35, 1.46, 12.63, 2.78,
        headers=[
            "Counterfactual Parameter Scenario",
            "Altered Parameter vs. Standard Design",
            "Resulting λ, F_crit & Sample Size N",
            "Methodological Failure Mode Avoided by the Standard Design",
        ],
        rows=[
            [
                "1. Underpowered Small Sample\n(Too Small N → Low λ)",
                "Use `N = 36` total (`n = 9/cell` in RQ3-Govern or `6/cell` in RQ4-Optimize) instead of `N = 144 / 180`.",
                "`λ = 0.0625 × 36 = 2.25`\nPower `1 − β` collapses from `.847` to `.308` (`69.2%` false-negative risk!).",
                "<b>Severe Type II Error Risk:</b> Nearly 70% of true medium improvements (`f = .25`) or factorial interactions would fail to reach significance and be falsely discarded.",
            ],
            [
                "2. Inflated Alpha Level\n(Loose α = .20)",
                "Relax significance threshold from `α = .05` to `α = .20`.",
                "`F_crit` drops from `3.92` to `1.66` (at `df = 1, 140`).",
                "<b>20% Type I False-Positive Risk:</b> Random LLM sampling noise or ineffective coarse routing would be falsely accepted and passed forward to the next solution approach stage!",
            ],
            [
                "3. Overly Tiny Effect Target\n(Chasing Noise f = .05)",
                "Target trivial effect `f = .05` (`η² = .0025`, 0.25% variance) instead of `f = .25`.",
                "`N_min = 9.88 / .0025 = 3,952` dialogues (exceeds the entire 1,334 Frames corpus!).",
                "<b>Exhausted Corpus & Zero Practical Value:</b> Wastes thousands of API calls to detect a 0.04-turn shift imperceptible to travelers.",
            ],
            [
                "4. Ignoring Sphericity Risk\nin RQ2-Personalize (`ρ` & `ε`)",
                "Omit the `+18%` buffer (`N = 28 → 33`) or assume optimistic `ρ = .90` (`N_min = 7`).",
                "If Greenhouse–Geisser `ε < 1.0` reduces effective `df`, unbuffered `N` loses power.",
                "<b>Protection Against Sphericity Departure:</b> Buffering `N = 28` to `33` (`11/persona`) preserves `>80%` power even when `ε` compresses degrees of freedom.",
            ],
        ],
        col_widths=[2.3, 2.7, 2.7, 4.93],
        font_size=8.8,
        align_left_cols=(0, 1, 2, 3),
    )
    D.add_card(
        s, 0.35, 4.34, 6.15, 1.94,
        title="Domain Hyperparameter 1: Exponential Turn Decay λ_d = 0.15 (Eq. 2)",
        header_bg=NAVY,
        bullets=[
            "<b>Trajectory Pooling Formula:</b>  <b>v = Σ <i>w<sub>t</sub></i> e<sub><i>t</i></sub></b>,   where  <b><i>w<sub>t</sub></i> ∝ exp[−λ<sub>d</sub>(<i>T</i> − <i>t</i>)]</b>",
            "<b>Methodological Rationale:</b> Turn 1 is often a generic greeting, while recent turns carry active constraint negotiation. Setting λ<sub>d</sub> = 0.15 weights the latest turn at 1.00, 3 turns prior at 0.64, and 10 turns prior at 0.22.",
            "<b>Sensitivity Grid (`step2b`):</b> Contrasts uniform pooling (`λ_d = 0.0`, which dilutes active constraints) against memoryless last-turn (`λ_d ≥ 1.0`) and user-only prefix pooling.",
        ],
        font_size=9.0,
    )
    D.add_card(
        s, 6.80, 4.34, 6.18, 1.94,
        title="Domain Hyperparameter 2: Prefix Truncation Horizon M ∈ {3, 5, 7, 9}",
        header_bg=TEAL,
        bullets=[
            "<b>Prefix Operator:</b> Restricts input transcripts to the first <b>`min(M, M_i)` user messages</b> (`step2g_rq1_truncation.py`).",
            "<b>Methodological Trade-Off Evaluated in RQ1-Identify:</b>",
            (1, "<b>Too small (`M = 1–2`):</b> Insufficient behavioral signal before initial preferences are stated."),
            (1, "<b>Too large (`Whole Dialogue`):</b> Includes closing turns (`'Book it!'` vs. `'Too expensive'`), confounding clusters with session outcome (`Field 14`)."),
            (1, "<b>Grid Evaluation:</b> Systematically sweeps `M ∈ {3, 5, 7, 9, whole}` across bootstrap `ARI`, core membership, outcome Cramér's `V`, and out-of-sample prefix routing `κ`."),
        ],
        font_size=9.0,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Methodology Link:</b> Distinguishing <b>statistical noncentrality `λ`</b> (which sizes `N = 159, 33, 144, 180` across RQ1-Identify to RQ4-Optimize) from <b>temporal turn decay `λ_d = 0.15` and prefix horizon `M`</b> (which govern RQ1-Identify representation design) ensures mathematical clarity across the defense.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 23: FEATURE IMPORTANCE & PREFIX ROUTER EVALUATION METHODOLOGY (METHODOLOGY ONLY)
    # =========================================================================
    s = D.content_slide(
        "4. Experimental Design & Statistical Methodology",
        "Feature Importance & Prefix Router Evaluation Methodology",
        "Three-tier feature importance protocol (η², ‖β_j‖₂, Δκ) and Train / 5-Fold CV / Held-Out Test routing evaluation (Methodology Only)",
        notes="Explain the exact methodology used to assess feature importance across the 46-d Blocks representation and how those importance results are used in RQ1-Identify and RQ2-Personalize.",
    )
    D.add_card(
        s, 0.35, 1.48, 4.05, 3.10,
        title="Tier 1: Unsupervised Cluster\nDiscrimination Importance (η²)",
        header_bg=NAVY,
        bullets=[
            "<b>How It Is Computed (`step2g` & `step2i`):</b>",
            (1, "For each of the 46 candidate features in `Blocks` (`20 Gemini PCs + 10 Ordinal LLM scales + 16 One-Hot/Multi-Hot Goal/Tone indicators`), compute one-way ANOVA variance accounted for across the discovered clusters on `D_gold (n = 933)`:"),
            (1, "<b>η<sub><i>j</i></sub><sup>2</sup> = SS<sub>between, <i>j</i></sub> / SS<sub>total, <i>j</i></sub></b>"),
            "<b>How It Is Used in the Analysis:</b>",
            (1, "Identifies which behavioral and semantic dimensions drive cluster separation and defines the <b>deterministic centroid-naming rules (Appendix F)</b>."),
        ],
        font_size=9.2,
    )
    D.add_card(
        s, 4.60, 1.48, 4.10, 3.10,
        title="Tier 2: Supervised L1 Logistic Router\nCoefficient Importance (‖β_j‖₂)",
        header_bg=TEAL,
        bullets=[
            "<b>How It Is Computed (`src/final_pipeline/routing.py`):</b>",
            (1, "Standardize all 46 features (`z`-score on `D_gold`) and fit a multinomial L1-penalized (LASSO) logistic regression router predicting cluster membership from opening prefixes `m ∈ {3, 5, 7, 9}`."),
            (1, "Compute the L2 magnitude across the 3 class log-odds vectors:  <b>‖β<sub><i>j</i></sub>‖<sub>2</sub> = √(Σ<sub><i>c</i>=1..3</sub> β<sub><i>c,j</i></sub><sup>2</sup>)</b>."),
            "<b>How It Is Used in the Analysis:</b>",
            (1, "L1 sparsity automatically prunes uninformative tail PCs (`β_j = 0`) to prevent overfitting during live early-turn routing."),
        ],
        font_size=9.2,
    )
    D.add_card(
        s, 8.90, 1.48, 4.08, 3.10,
        title="Tier 3: Block-Drop Ablation (Δκ) &\nOut-of-Sample Router Audit",
        header_bg=BLUE,
        bullets=[
            "<b>Block-Drop Ablation (`Δκ` & `ΔARI`):</b>",
            (1, "Systematically drop each feature block (`Ordinal Scales`, `Categorical Goal/Tone`, or `Gemini PCs 1–20`) and measure the drop in bootstrap `ARI` and held-out routing `Δκ` on `D_test (n = 401)`."),
            "<b>Three-Split Generalization Protocol:</b>",
            (1, "Report Accuracy, Cohen's `κ`, and Macro-F1 across <b>(1) `D_gold` Train (`n=933`)</b>, <b>(2) `D_gold` 5-Fold Stratified CV (`n=933`)</b>, and <b>(3) Held-Out `D_test` (`n=401`)</b>, plus the <b>3 × 3 Confusion Matrix & Multiclass One-vs-Rest ROC-AUC curves</b>."),
        ],
        font_size=9.2,
    )
    D.add_table(
        s, 0.35, 4.68, 12.63, 1.60,
        headers=[
            "Feature Block in `46-d Blocks` (`X^(9)`)",
            "Dimensions",
            "Scale & Weighting in `Blocks`",
            "Analytical Role in RQ1-Identify Stage & RQ2-Personalize Stage",
        ],
        rows=[
            [
                "Block 1: Truncated User Prefix Embeddings (`Gemini-001`)",
                "20 cols (`PC1–PC20`)",
                "3,072-d user prefix (`≤ M` msgs) → `PCA-20`, scaled to unit block variance (`w = 1.0`).",
                "Captures continuous semantic intent, phrasing, and destination/package domain context.",
            ],
            [
                "Block 2: Validated Ordinal Behavioral Scales (`Fields 1–10`)",
                "10 cols (`1–5` Likert)",
                "Standardized (`z`-score) and weighted (`w = 1.5`) so behavioral traits balance 20 PCs.",
                "Quantifies flexibility, exploration breadth, decisiveness, revision tendency, politeness & price sensitivity.",
            ],
            [
                "Block 3: Categorical Goal & Tone Indicators (`Fields 11–13`)",
                "16 binary cols",
                "One-hot (`goal_specificity`, `tone`) & multi-hot (`secondary_goals`), block-scaled (`w = 1.0`).",
                "Encodes explicit booking vs. exploration goals; `Fields 14–16` (`outcome, party, flag`) excluded from clustering!",
            ],
        ],
        col_widths=[3.1, 1.5, 3.8, 4.23],
        font_size=8.8,
        align_left_cols=(0, 2, 3),
        highlight_rows=(0, 1, 2),
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Solution Approach Methodology Link:</b> This 3-tier feature importance framework directly addresses how features are selected, weighted, and validated in `RQ1-Identify Stage`—ensuring that only non-leaky, high-discrimination features enter the `RefinedArchetypeRouter` and `RQ2-Personalize` FAISS sub-indices.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=9.5,
    )

    # =========================================================================
    # SLIDE 24: SYSTEM ARCHITECTURE (FIGURE 4) & ALGORITHMIC WORKFLOWS (FIGURE 5) (METHODOLOGY ONLY)
    # =========================================================================
    s = D.content_slide(
        "4. Experimental Design & Statistical Methodology",
        "End-to-End Neuro-Symbolic System Architecture & Stage Workflows",
        "Figures 4 & 5: Offline discovery on D_gold (n = 933), 1 FAISS sub-index per cluster (k = 3), and online runtime on D_test (n = 401)",
        notes="Walk through Figures 4 and 5 side-by-side to show the complete engineering architecture and how 1 FAISS index per cluster works in RQ1-Identify -> RQ2-Personalize.",
    )
    D.add_figure(
        s, os.path.join(FIG_FIN, "fig_system_architecture.png"),
        0.35, 1.48, 6.25, 3.45,
        caption="Figure 4: Five-Layer Neuro-Symbolic System Architecture (Offline D_gold vs. Online D_test)",
    )
    D.add_figure(
        s, os.path.join(FIG_FIN, "fig_rq_workflows_4panel.png"),
        6.75, 1.48, 6.23, 3.45,
        caption="Figure 5: Four-Panel Execution Workflows for RQ1-Identify (A), RQ2-Personalize (B), RQ3-Govern (C), and RQ4-Optimize (D)",
    )
    D.add_card(
        s, 0.35, 5.00, 12.63, 1.30,
        title="How the 4-Stage Architecture Operates & How FAISS Indexing Works in RQ1-Identify → RQ2-Personalize",
        header_bg=NAVY,
        bullets=[
            "<b>1. Offline Discovery (`Layers 1–2 on D_gold = 933`):</b> Parses Two-Tier Pydantic trajectories → extracts `min(M, 9)` opening user prefixes → computes `46-d Blocks` → fits `K-Means (k = 3)` and the L1 `RefinedArchetypeRouter`. Crucially, it builds <b>exactly 1 `faiss.IndexFlatIP(46)` vector index per cluster (`3 FAISS sub-indices total` across `D_gold`)</b> with all exemplar entities masked as `[SLOT]` tokens.",
            "<b>2. Online Runtime (`Layers 3–5 on D_test = 401`):</b> `RQ1-Identify` projects the active user prefix into `46-d Blocks` (`< 2 ms`) and routes to winning cluster `k* ∈ {1, 2, 3}` → `RQ2-Personalize` queries <b>only Cluster `k*`'s FAISS sub-index</b> for the top `k_shot = 3` `[SLOT]`-masked exemplars + persona pacing directive → `RQ3-Govern` executes pre/post `YAML` rule verification (`< 1 ms`) → `RQ4-Optimize` updates the `Verified Informed Slot Ledger` and selects the persona package policy.",
        ],
        font_size=9.1,
    )
    D.add_callout(
        s, 0.35, 6.38, 12.63, 0.74,
        "<b>Transition from Methodology to Empirical Results (Next Section):</b> "
        "With the 4-stage conceptual solution approach, literature operationalization, 70/30 data firewall, noncentral-<i>F</i> sample sizes, and system architecture locked in, `Slides 25–48` now present the complete empirical results and stage-by-stage solution approach handoffs.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=9.5,
    )
