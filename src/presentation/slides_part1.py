"""
Part 1 of the QM640 Capstone Defense Presentation (Slides 1–21):
  - Module 1 (Slides 1–5): Foundations & The Real-World Story (Ground-Up Basics for AI & Non-AI Experts)
  - Module 2 (Slides 6–9): Literature Analysis — What Others Tried, How We Use It, and What Is Uniquely New (With Data Examples)
  - Module 3 (Slides 10–13): Dataset Authenticity, Two-Tier Schema, Data Cleaning & Exploratory Data Analysis
  - Module 4 (Slides 14–19): Ground-Up Statistical Methodology — Why Each Test & Parameter (α, 1−β, f, λ) Was Chosen & Counterfactuals
  - Module 5 (Slides 20–21): End-to-End Neuro-Symbolic System Architecture & Per-RQ Execution Workflows
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
from report.final_context import FIG_FIN, FIG_INT, REPO, TITLE


def build_slides_part1(D, ctx):
    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    D.add_title_slide(
        title=TITLE,
        subtitle="A Neuro-Symbolic Framework Coupling Early-Turn Behavioral-Semantic Archetype Routing, "
                 "Slot-Masked FAISS In-Context Learning, and Declarative Policy Verification",
        author_lines=[
            "<b>Author:</b> Surnella Sandeep  |  <b>Course:</b> QM640: Data Analytics Capstone (Department of Data Analytics, Walsh College)",
            "<b>Instructor & Capstone Mentor:</b> Mr. Smitraj Raut  |  <b>Date:</b> October 2026",
            f"<b>Reproducible Code & Data Repository:</b> {REPO}",
            "<b>Empirical Scope:</b> 2,833 Analytic Human Dialogues (Microsoft Frames N = 1,334; MultiWOZ 2.2 N = 1,499) + ~8,900 Gemini 2.5 Flash/Pro Evaluations",
        ],
        notes=(
            "Welcome to the defense presentation for my QM640 Data Analytics Capstone. "
            "This presentation is structured from the ground up so both AI specialists and non-AI/mathematics "
            "committee members can follow every intuition, statistical test choice, sample-size derivation, "
            "literature comparison, empirical result across RQ1 to RQ4, and the roadmap to my future doctoral dissertation."
        ),
    )

    # =========================================================================
    # SLIDE 2: PRESENTATION ROADMAP
    # =========================================================================
    s = D.content_slide(
        "Module 1: Foundations & Story",
        "Presentation Roadmap: Building the Story from Basics to Defense Synthesis",
        "An 8-module progressive narrative designed for both AI/ML specialists and statistical/business domain experts",
        notes="Walk the committee through the 8 modules so they see how basic intuition and statistical rigor precede the empirical results.",
    )
    D.add_card(
        s, 0.35, 1.50, 3.05, 2.55,
        title="1. Ground-Up Basics (Slides 1–5)",
        header_bg=NAVY,
        bullets=[
            "Why static travel chatbots frustrate real travelers.",
            "Why naive few-shot AI prompts leak entities & break rules.",
            "Plain-English glossary: Embeddings, Clustering, FAISS, Symbolic Rules, Turn Economy.",
        ],
    )
    D.add_card(
        s, 3.55, 1.50, 3.05, 2.55,
        title="2. Literature & Novelty (Slides 6–9)",
        header_bg=TEAL,
        bullets=[
            "26 peer-reviewed studies across 4 streams.",
            "How we build on prior work & where prior papers stop.",
            "Concrete data examples from RQ1–RQ4 proving our unique contributions.",
        ],
    )
    D.add_card(
        s, 6.75, 1.50, 3.05, 2.55,
        title="3. Data Authenticity & EDA (Slides 10–13)",
        header_bg=BLUE,
        bullets=[
            "Why Microsoft Frames & MultiWOZ 2.2 were created & why they fit.",
            "Two-tier Pydantic schema & 70/30 leakage-free split.",
            "Univariate, Bivariate & Multivariate PCA insights.",
        ],
    )
    D.add_card(
        s, 9.95, 1.50, 3.03, 2.55,
        title="4. Statistical Foundations (Slides 14–19)",
        header_bg=GOLD,
        bullets=[
            "Why ANOVA, RM-ANOVA, and 2×2 / 2×3 Factorial ANOVA were chosen.",
            "Everyday real-world analogies for every test.",
            "Why α=.05, Power=.80, f=.25, λ are standard & what fails if mischosen.",
        ],
    )
    D.add_card(
        s, 0.35, 4.25, 3.05, 2.55,
        title="5. System Architecture (Slides 20–21)",
        header_bg=NAVY,
        bullets=[
            "5-Layer Neuro-Symbolic Architecture diagram.",
            "Offline Golden Discovery (n=933) vs. Online Runtime (n=401).",
            "Step-by-step execution workflows for RQ1 to RQ4.",
        ],
    )
    D.add_card(
        s, 3.55, 4.25, 3.05, 2.55,
        title="6. Deep-Dive Results RQ1–RQ4 (Slides 22–34)",
        header_bg=GREEN,
        bullets=[
            "RQ1: 159-run clustering + M=9 Blocks router (κ = .535–.958).",
            "RQ2: Why Primary failed (p=.211) & Refined succeeded (p<.001).",
            "RQ3: 2×2 Rules × Prompting (0% leakage, 98.6% compliance).",
            "RQ4: 2×3 Turn Economy (−29.5% to −42.7% turns, 0% RER).",
        ],
    )
    D.add_card(
        s, 6.75, 4.25, 3.05, 2.55,
        title="7. Defense Q&A Bank (Slides 35–38)",
        header_bg=CORAL,
        bullets=[
            "Direct answers to anticipated committee questions:",
            "(1) Sample size assumptions; (2) Prior work used;",
            "(3) Unique novelty; (4) Dataset authenticity & fit;",
            "(5) Dual-LLM judge & simulator validity.",
        ],
    )
    D.add_card(
        s, 9.95, 4.25, 3.03, 2.55,
        title="8. Dissertation Roadmap (Slides 39–42)",
        header_bg=BLUE,
        bullets=[
            "Unified causal story across all 4 RQs.",
            "Limitations that bound the master's capstone.",
            "Doctoral Dissertation: 'Dialogue Clustering & Methodologies for Human-Like Conversations'.",
        ],
    )
    D.add_callout(
        s, 0.35, 6.85, 12.63, 0.34,
        "<b>Core Thesis:</b> Personalizing chatbot style without symbolic guardrails causes hallucinations (35.9% leakage); enforcing rules without persona routing causes rigid, repetitive dialogues. Combining both yields a Pareto-optimal travel assistant.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=11,
    )

    # =========================================================================
    # SLIDE 3: THE REAL-WORLD BUSINESS PROBLEM (CONCRETE DIALOGUE EXAMPLES)
    # =========================================================================
    s = D.content_slide(
        "Module 1: Foundations & Story",
        "The Real-World Business Problem: Why Static Travel Chatbots Fail",
        "Travelers do not all shop the same way—yet commercial chatbots force every customer through one static script",
        notes="Start with a relatable real-world scenario. Show how three different customers enter an Online Travel Agency (OTA) portal and get frustrated by a one-size-fits-all chatbot.",
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
            (1, "Follows a slow 8-step intake script; re-asks slots already stated in Turn 1 (19.4% Redundant Elicitation Rate in our Zero-Shot baseline)."),
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
            (1, "<i>'We have a week off in September and $3,000—what beach or European cities could we compare?'</i>"),
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
            (1, "Says 'No package found' or argues for 4 turns before revealing alternatives (44.5% end with no suitable option in human corpus)."),
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
    # SLIDE 4: THE TECHNICAL PARADOX — WHY NAIVE AI ADAPTATION FAILS
    # =========================================================================
    s = D.content_slide(
        "Module 1: Foundations & Story",
        "The Technical Paradox: Why Naive Few-Shot AI Adaptation Fails",
        "Simply pasting retrieved past dialogues into an LLM prompt introduces two severe production hazards",
        notes="Explain why we cannot just use standard Retrieval-Augmented Generation (RAG) or naive KATE few-shot prompting.",
    )
    D.add_card(
        s, 0.35, 1.50, 6.15, 3.80,
        title="Hazard 1: Exemplar Entity Leakage (Hallucinated Terms)",
        header_bg=CORAL,
        bg_color=RED_BG,
        bullets=[
            "<b>What happens in standard few-shot prompting (Liu et al., 2022):</b>",
            (1, "To teach the LLM how to talk to an <i>Open Explorer</i>, the system retrieves 3 similar past transcripts from the database and puts them in the prompt."),
            "<b>The Contamination Trap (Proven in our RQ3 Experiment):</b>",
            (1, "If those retrieved examples mention <b>'Sapphire Bay Resort'</b>, <b>'SkyBridge Airways'</b>, <b>'$1,149'</b>, or promo code <b>'VIP25'</b>, the LLM copies those stale entities into the current customer's reply!"),
            "<b>Empirical Proof from Our Data (RQ3 Table 15):</b>",
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
            "<b>Empirical Proof from Our Data (RQ3 Table 15):</b>",
            (1, "Without an external symbolic rule engine (<i>Rules Off</i>), Gemini 2.5 Flash enforced violated booking rules in only <b>5.6% of violating sessions</b> (missing <b>94.4%</b> of violations!)."),
        ],
    )
    D.add_card(
        s, 0.35, 5.45, 12.63, 1.65,
        title="Our Solution: A Neuro-Symbolic Cluster-Adaptive Architecture",
        header_bg=GREEN,
        bg_color=GREEN_BG,
        bullets=[
            "<b>1. Early-Turn Hybrid Archetype Routing (RQ1):</b> Identify whether the user is a <i>Decisive Booker</i>, <i>Open Explorer</i>, or <i>Rigid-Constraint Seeker</i> from opening user messages without leaking end-of-dialogue outcomes.",
            "<b>2. Slot-Masked FAISS Exemplar Retrieval (RQ2):</b> Replace all entities in retrieved examples with `[SLOT]` placeholders (e.g., `[HOTEL_NAME]`, `[BUDGET_USD]`) so the LLM learns <i>conversational style and pacing</i> without copying stale facts.",
            "<b>3. Deterministic Declarative Rule Engine + Informed Slot Ledger (RQ3 & RQ4):</b> Enforce YAML booking policies (0.0% leakage, 98.6% compliance) and lock stated user slots so the bot never re-asks known information (0.0% redundant elicitation).",
        ],
        font_size=11.5,
    )

    # =========================================================================
    # SLIDE 5: CORE CONCEPTS EXPLAINED FROM THE GROUND UP
    # =========================================================================
    s = D.content_slide(
        "Module 1: Foundations & Story",
        "Core Concepts Explained from the Ground Up (Plain-English Primer)",
        "Bridging AI/NLP terminology and statistical measurement for interdisciplinary defense committee members",
        notes="Use this slide to make sure non-AI professors have crystal-clear intuition for the 6 building blocks used throughout the presentation.",
    )
    D.add_table(
        s, 0.35, 1.50, 12.63, 5.55,
        headers=["Concept / Term", "Plain-English Meaning", "Real-World Analogy", "How It Is Measured in This Study"],
        rows=[
            [
                "1. Vector Embedding\n(SBERT 384-d &\nGemini 3,072-d)",
                "Converting a sentence or dialogue into a list of numbers (coordinates) so dialogues with similar meaning sit close together in geometry.",
                "Like GPS coordinates (latitude, longitude) on a map, but with 384 or 3,072 dimensions capturing meaning and tone.",
                "Cosine similarity [-1, +1] between vectors: +1 = identical direction/style; 0 = unrelated.",
            ],
            [
                "2. Unsupervised\nTrajectory Clustering\n(K-Means, Ward, HDBSCAN)",
                "Automatically grouping 933 training dialogues into natural customer segments without pre-labeled categories.",
                "Sorting thousands of retail shoppers into 'Quick Grab-and-Go', 'Window Browsers', and 'Coupon Bargain Hunters' by watching how they walk.",
                "Silhouette score [-1, +1] (higher = tighter, well-separated clusters), Davies–Bouldin index (lower = better), and Bootstrap ARI stability [0, 1].",
            ],
            [
                "3. Early-Turn Prefix\nRouting\n(RefinedArchetypeRouter)",
                "Predicting which archetype a new customer belongs to after reading only their first M (e.g., 5 to 9) messages.",
                "An experienced hotel concierge recognizing a guest's style within the first 60 seconds of conversation.",
                "Out-of-sample Routing Accuracy (%) and chance-corrected Cohen's Kappa (κ) on 401 held-out test dialogues.",
            ],
            [
                "4. Slot-Masked FAISS\nFew-Shot Prompting",
                "Retrieving the 3 closest past dialogues from the customer's archetype with hotel/price names masked as [SLOT], showing them to the LLM as style templates.",
                "Giving a new sales associate 3 redacted scripts showing *how* to structure an answer without letting them quote last week's prices.",
                "Style Convergence Cosine (similarity to human wizard style) and Pacing Calibration Error (|generated words − target archetype words|).",
            ],
            [
                "5. Neuro-Symbolic\nGuardrail\n(Declarative Rule Engine)",
                "Combining a neural LLM (for fluent language) with deterministic code rules (if/then YAML policies) that audit facts before & after generation.",
                "An architect designing a creative building (Neural LLM) checked by a structural engineer's building-code calculator (Symbolic Engine).",
                "Rule Adherence Rate (RAR), Exemplar Entity Leakage Rate (ELR), and Factual Slot Coverage F1 [0, 1].",
            ],
            [
                "6. Turn Economy &\nRedundant Elicitation\nRate (RER)",
                "How many back-and-forth turns it takes to reach a successful booking, and how often the bot wastes turns re-asking already-stated facts.",
                "Closing a travel booking in 5 focused turns instead of 9 repetitive turns asking 'Where are you flying from?' twice.",
                "Turns to Goal Completion (TGC, raw & log-transformed) and RER = redundant slot questions / total agent turns.",
            ],
        ],
        col_widths=[1.8, 3.3, 3.5, 4.0],
        font_size=10.5,
        align_left_cols=(0, 1, 2, 3),
    )

    # =========================================================================
    # SLIDE 6: LITERATURE STREAM 1 & 2 (BUSINESS VALUE & DIALOGUE CORPORA)
    # =========================================================================
    s = D.content_slide(
        "Module 2: Literature Analysis & Uniqueness",
        "Literature Review (Part 1): Hospitality AI Value & Task-Oriented Corpora",
        "What prior business and corpus studies discovered, how we use their foundations, and what they left unsolved",
        notes="Directly addresses Committee Question 2 & 3 on prior literature in business hospitality and dialogue datasets.",
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
            "<b>How We Use This Knowledge:</b>",
            (1, "We operationalize their qualitative constructs—<i>decisiveness, exploration breadth, constraint rigidity, and interaction effort</i>—into 16 quantitative behavioral variables and multi-turn turn-economy metrics."),
            "<b>What Is Uniquely New in Our Study (With Data Proof):</b>",
            (1, "Prior tourism papers relied on <i>post-hoc user surveys</i>. We are the first to instrument actual LLM turn economy, proving a <b>35.8% reduction in turns (7.93 → 5.09 turns, p < .001)</b> and <b>0.0% redundant questions</b>."),
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
            "<b>How We Use This Knowledge:</b>",
            (1, "We use Frames (<i>N</i> = 1,334 analytic) as our primary consultative travel testbed and MultiWOZ 2.2 (<i>N</i> = 1,499) as an external structural transfer benchmark."),
            "<b>What Is Uniquely New in Our Study (With Data Proof):</b>",
            (1, "Both corpora were built for <i>supervised slot state tracking</i>, treating all users as uniform. Neither clustered user decision-making archetypes nor audited policy compliance."),
            (1, "Our cross-corpus test in RQ1 proves that Frames negotiation archetypes do not transfer trivially to simple MultiWOZ slot-filling (centroid cosine <b>.467 vs. .269, t = 28.08, p < .001</b>), proving consultative travel requires its own archetype taxonomy."),
        ],
        font_size=11,
    )

    # =========================================================================
    # SLIDE 7: LITERATURE STREAM 3 & 4 (CLUSTERING, ICL & GUARDRAILS)
    # =========================================================================
    s = D.content_slide(
        "Module 2: Literature Analysis & Uniqueness",
        "Literature Review (Part 2): Representation Learning, FAISS ICL & Guardrails",
        "How we integrate vector geometry, dynamic in-context learning, and programmable rails—and overcome their failure modes",
        notes="Continue literature synthesis covering SBERT/Gemini embeddings, KATE k-NN prompting, and NeMo/Tau-bench guardrails.",
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
            "<b>What Failed When Applied Directly (Our Interim Discovery):</b>",
            (1, "When we clustered whole-dialogue embeddings directly (as standard papers do), clusters captured <i>end-of-dialogue outcomes</i> and <i>wizard identity</i> (Cramér's <i>V</i> = .45) rather than user behavior, giving terrible early-turn routing (<b>κ = .24</b>) and a null RQ2 prompting result (<b>p = .211</b>)!"),
            "<b>Our Unique Innovation (RQ1 Breakthrough):</b>",
            (1, "We combined <b>truncated opening user prefixes (first M = 9 user messages)</b> with a <b>16-field LLM behavioral profile (`Blocks`)</b>, raising bootstrap stability to <b>ARI = .76</b> and out-of-sample routing to <b>κ = .535 (M=5) and κ = .958 (M=9)</b>."),
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
            "<b>Our Unique Innovation (RQ2 & RQ3 Breakthrough):</b>",
            (1, "We partition FAISS into <b>archetype-specific sub-indices with `[SLOT]` masking</b>, boosting style convergence over static few-shot by <b>+31.8% (.597 vs. .453, p < .001, d_z = 0.74)</b>."),
            (1, "In RQ3, we prove a <b>significant 2 × 2 interaction (F = 34.82, p < .001)</b>: our declarative rule layer eliminates the <b>35.9% entity leakage</b> of unguarded few-shot prompting down to <b>0.0%</b>."),
        ],
        font_size=11,
    )

    # =========================================================================
    # SLIDE 8: LITERATURE SYNTHESIS MATRIX WITH DATA-BACKED EXAMPLES
    # =========================================================================
    s = D.content_slide(
        "Module 2: Literature Analysis & Uniqueness",
        "Literature Synthesis Matrix: Prior Approaches vs. Our Empirical Findings",
        "Concrete examples quoted directly from our RQ1–RQ4 data illustrating what prior methods miss and what our framework solves",
        notes="Walk through this table row-by-row during the defense to show mastery of the literature and concrete empirical evidence.",
    )
    D.add_table(
        s, 0.35, 1.50, 12.63, 5.55,
        headers=["Prior Literature Benchmark", "What Prior Paper Did", "Limitation When Applied to Travel Dialogues", "Our Unique Methodological Addition", "Concrete Proof Quoted from Our Data (RQ1–RQ4)"],
        rows=[
            [
                "Whole-Text Embedding Clustering\n(Reimers & Gurevych, 2019;\nMcInnes et al., 2017)",
                "Clustered full documents using SBERT / HDBSCAN.",
                "HDBSCAN discards 71.7% of travel dialogues as noise; full-dialogue vectors leak end-of-session booking outcomes.",
                "Prefix-truncated (M=9 user msgs) hybrid Blocks (PCA-20 Gemini + 16 LLM behavioral ratings) with K-Means (k=3).",
                "RQ1: HDBSCAN failed in 53/53 default runs. Our M=9 Blocks router achieved ARI = .76 and raised held-out routing from κ = .24 (39.4%) to κ = .535 (70.1% at M=5) and κ = .958 (97.3% at M=9).",
            ],
            [
                "Global k-NN Few-Shot (KATE)\n(Liu et al., 2022;\nBrown et al., 2020)",
                "Retrieved k nearest examples from one global pool without persona routing.",
                "Static/unrouted examples mismatch user pacing; coarse routing (κ=.24) fails to improve style.",
                "Archetype-partitioned FAISS sub-indices + archetype pacing directives routed via Blocks.",
                "RQ2: Coarse Primary RQ2 failed (F = 1.61, p = .211). Refined RQ2 succeeded (F = 9.79, p < .001, ηp² = .234): style cosine rose from .453 (Static) to .597, and word pacing error fell from 10.12w to 3.87w.",
            ],
            [
                "Unmasked In-Context Examples\n(Standard RAG / Few-Shot)",
                "Inserted raw historical text examples directly into the LLM prompt.",
                "LLM copies stale hotel names, prices, and promo codes from examples into the active user session.",
                "Regex/Schema [SLOT] masking in FAISS exemplars + post-generation entity leakage sanitizer.",
                "RQ3: Unguarded Cluster-Adaptive leaked stale entities ('Sapphire Bay Resort', '$1,149', 'VIP25') in 55.6% of cases (ELR = .359). Rules Active × Cluster-Adaptive reduced leakage to 0.0% (Interaction F = 34.82, p < .001).",
            ],
            [
                "Prompt-Only Policy Instructions\n(Yao et al., 2024 τ-bench;\nRebedea et al., 2023)",
                "Evaluated LLM adherence to domain rules stated only in natural language prompts.",
                "LLMs ignore numeric visa, passport, adult-cap, and discount thresholds when optimizing for conversational tone.",
                "Deterministic YAML RuleEngine (5 Tier-2 rules) executing pre-generation checks & post-generation verification.",
                "RQ3: Under Rules Off, Gemini 2.5 Flash enforced policy violations in only 5.6% of violating sessions. Activating RuleEngine raised violation enforcement to 98.6% (F = 43.92, p < .001) and Slot F1 from .485 to .952.",
            ],
            [
                "Static Sequential Slot-Filling\n(Budzianowski et al., 2018;\nInaba et al., 2022)",
                "Used a single dialogue policy across all users without tracking informed slots.",
                "Re-asks already stated constraints and causes 8.7-turn deadlocks for Rigid-Constraint Seekers.",
                "Verified Informed Slot Ledger + Archetype-Specific Turn-Economy Policy (bundle vs. compare vs. proactive trade-off).",
                "RQ4: Cut turns to booking by −42.7% for Rigid-Constraint Seekers (8.73 → 5.00 turns, d = −3.40), −34.2% for Decisive Bookers (7.60 → 5.00), and −29.5% for Open Explorers (7.47 → 5.27), while cutting RER from .109 to .000.",
            ],
        ],
        col_widths=[1.8, 1.9, 2.3, 2.5, 4.1],
        font_size=9.8,
        align_left_cols=(0, 1, 2, 3, 4),
        highlight_rows=(0, 1, 2, 3, 4),
    )

    # =========================================================================
    # SLIDE 9: THE FOUR LINKED RESEARCH QUESTIONS (CAUSAL CHAIN)
    # =========================================================================
    s = D.content_slide(
        "Module 2: Literature Analysis & Uniqueness",
        "How the Four Research Questions Form One Integrated Causal Chain",
        "Each research question solves a specific bottleneck and feeds its validated output directly into the next stage",
        notes="Show the committee that RQ1, RQ2, RQ3, and RQ4 are not four separate mini-studies—they are four sequential layers of one engineering and scientific argument.",
    )
    D.add_table(
        s, 0.35, 1.50, 12.63, 4.45,
        headers=["RQ", "Research Question", "Manipulated IV (X)", "Measured DV (Y)", "Hypotheses (H0 vs. Ha)", "Why This Step Is Essential in the Story"],
        rows=[
            [
                "RQ1\n(Discovery &\nRouting)",
                "Which clustering algorithm best separates travel trajectories, and which early-routable user archetypes emerge?",
                "X1: Algorithm (K-Means, Ward, HDBSCAN) × Prefix Horizon M ∈ {3,5,7,9,whole} × Representation",
                "Y1: Cosine Silhouette, Davies–Bouldin, Bootstrap ARI Stability, Out-of-Sample Routing κ",
                "H01: μ_Sil equal across algorithms.\nHa1: Algorithms differ (p<.05) & prefix Blocks yield stable (ARI≥.60), routable archetypes.",
                "Without stable, early-routable user archetypes (free of outcome leakage), downstream adaptive prompting cannot know which persona to target.",
            ],
            [
                "RQ2\n(Style &\nPacing)",
                "Does cluster-adaptive few-shot prompting improve style convergence and pacing calibration over static and zero-shot?",
                "X2: Prompting Strategy (Zero-Shot, Static Few-Shot k=3, Cluster-Adaptive Few-Shot k=3)",
                "Y2: De-lexicalized SBERT Style Cosine, Gemini 3,072-d Cosine, BERTScore F1, Pacing Word Error",
                "H02: μ_style equal across 3 conditions.\nHa2: Cluster-Adaptive > Static & Zero-Shot on refined archetypes.",
                "Tests whether routing to an archetype's FAISS sub-index actually makes the LLM mirror human consultant style and verbosity for that persona.",
            ],
            [
                "RQ3\n(Safety &\nCompliance)",
                "How do a declarative rule engine and cluster-adaptive prompting interact to govern compliance, leakage, and slot F1?",
                "X3: 2 × 2 Factorial: Rules Mode (Off vs. Active) × Prompting (Zero-Shot vs. Cluster-Adaptive)",
                "Y3: Rule Adherence Rate (RAR)\nY4: Exemplar Leakage (ELR)\nY5: Slot F1 & Style Cosine",
                "H03: No main or interaction effects.\nHa3: Active rules raise RAR & Slot F1 and eliminate few-shot leakage (Interaction p<.05).",
                "Proves that adaptive style prompting is unsafe on its own (35.9% leakage) and requires symbolic rule verification to be enterprise-ready.",
            ],
            [
                "RQ4\n(Multi-Turn\nEfficiency)",
                "Does cluster-adaptive prompting with an informed-slot ledger reduce turns to booking and redundant questions across archetypes?",
                "X4: 2 × 3 Factorial: Prompting (Zero-Shot vs. Cluster-Adaptive) × Refined Archetype (DB, OE, RCS)",
                "Y6: Log Turns to Goal Completion (ln TGC), Raw Turns, Redundant Elicitation Rate (RER)",
                "H04: No main or interaction effects.\nHa4: Cluster-Adaptive cuts log turns & RER with a significant Prompt × Archetype interaction.",
                "Demonstrates end-to-end business value: fewer turns to booking, zero repetitive slot questions, and tailored trade-off resolution.",
            ],
        ],
        col_widths=[1.1, 2.3, 2.2, 2.1, 2.3, 2.6],
        font_size=10,
        align_left_cols=(0, 1, 2, 3, 4, 5),
    )
    D.add_callout(
        s, 0.35, 6.10, 12.63, 0.98,
        "<b>Key Narrative Link:</b> RQ1 discovers <i>who</i> the traveler is in the first 5–9 messages → RQ2 proves we can match <i>how</i> to speak to them → RQ3 guarantees we never <i>hallucinate or break booking rules</i> while adapting style → RQ4 proves this closes bookings in <i>29.5% to 42.7% fewer turns</i>.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=11.5,
    )

    # =========================================================================
    # SLIDE 10: DATASET AUTHENTICITY, ORIGIN & FIT FOR PURPOSE (DEFENSE Q4)
    # =========================================================================
    s = D.content_slide(
        "Module 3: Data Authenticity, Schema & EDA",
        "Dataset Authenticity, Origin, and Fit for Purpose (Defense Question #4)",
        "Why Microsoft Frames and MultiWOZ 2.2 were created, why they are gold-standard human corpora, and how they match our study",
        notes="This slide directly answers Defense Question 4: What is the authenticity of the datasets, why were they created, and do they match our research?",
    )
    D.add_card(
        s, 0.35, 1.50, 6.15, 3.85,
        title="Primary Corpus: Microsoft Frames (El Asri et al., 2017)",
        header_bg=NAVY,
        bullets=[
            "<b>Who Created It & How:</b> Created by Maluuba / Microsoft Research using 12 human participants (85 user–wizard pairs) over 20 days in a Wizard-of-Oz setup backed by a real database of flights and hotels.",
            "<b>Why It Was Created:</b> Existing datasets only handled simple slot-filling. Microsoft created Frames (1,369 human–human dialogues; 19,986 turns) to study <b>decision-making, budget trade-offs, and frame-switching</b> across multiple vacation packages.",
            "<b>Why It Matches Our Research Perfectly:</b>",
            (1, "Contains genuine human behavioral diversity: decisive buyers, multi-city explorers, and rigid budget/star negotiators."),
            (1, "Rich ground-truth annotations: 20+ dialogue act types (`inform`, `offer`, `switch_frame`, `request_compare`), slot–value histories, wizard task success (74.2%), and user satisfaction ratings."),
        ],
        font_size=10.8,
    )
    D.add_card(
        s, 6.80, 1.50, 6.18, 3.85,
        title="Comparison Corpus: MultiWOZ 2.2 (Zang et al., 2020)",
        header_bg=TEAL,
        bullets=[
            "<b>Who Created It & How:</b> Collected at the University of Cambridge (Budzianowski et al., 2018) via crowd-sourced human tourists and clerks (10,438 dialogues), with schema-guided slot annotations cleaned by Google Research in v2.2 (Zang et al., 2020).",
            "<b>Why It Was Created:</b> Standard benchmark for multi-domain dialogue state tracking (hotel, train, attraction, taxi, restaurant).",
            "<b>Why We Included a Seeded Sample (N = 1,500 raw; 1,499 analytic):</b>",
            (1, "Provides an external structural benchmark in EDA (comparing turn distributions and verbosity)."),
            (1, "Tests <b>cross-corpus domain specificity</b> in RQ1: because MultiWOZ lacks flight routing and multi-package price negotiation, projecting MultiWOZ onto Frames centroids tests whether our archetypes are genuinely consultative vs. generic."),
        ],
        font_size=10.8,
    )
    D.add_card(
        s, 0.35, 5.50, 12.63, 1.60,
        title="Where Public Datasets Had a Gap—and How We Solved It Rigorously Without Compromising Authenticity",
        header_bg=GOLD,
        bg_color=CALLOUT_BG,
        bullets=[
            "<b>Gap 1 (Zero Tier-2 Enterprise Policy Slots in Public Corpora):</b> Our audit of all 1,334 Frames dialogues (Appendix Table E4) proved that 0.0% of public dialogues record visa windows, passport validity months, or promo discount caps (only `budget_amount` is observed in 78.5%). <b>Solution:</b> In RQ3, we took real held-out Frames dialogues (preserving authentic user language and Tier-1 trip constraints) and used a seeded (`seed=42`) experimental injector to attach controlled Tier-2 policy states (50% violating, 50% compliant).",
            "<b>Gap 2 (Static Logs Cannot React to New Agent Replies in RQ4):</b> Static corpus transcripts have fixed wizard replies. <b>Solution:</b> In RQ4, we grounded a persona-conditioned user simulator in the exact Tier-1 constraints of 90 held-out Frames dialogues and verified its persona fidelity with an independent `gemini-2.5-pro` judge (<b>95.6% accuracy, κ = .933</b>).",
        ],
        font_size=10.5,
    )

    # =========================================================================
    # SLIDE 11: TWO-TIER SCHEMA, DATA CLEANING & ZERO-LEAKAGE PARTITIONING
    # =========================================================================
    s = D.content_slide(
        "Module 3: Data Authenticity, Schema & EDA",
        "Two-Tier Canonical Schema, Data Cleaning Audit & Leakage Prevention",
        "Strict programmatic data hygiene (src/canonical_schema.py & step1_prepare_data.py) before any modeling",
        notes="Walk through the two-tier Pydantic schema, the cleaning audit table (Table 5), and how the 70/30 golden/test split prevents data leakage.",
    )
    D.add_card(
        s, 0.35, 1.50, 5.20, 3.60,
        title="Two-Tier Pydantic Schema (src/canonical_schema.py)",
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
        font_size=10.5,
    )
    D.add_table(
        s, 5.75, 1.50, 7.23, 3.60,
        headers=["Quality Audit Check", "Detection Rule", "Frames (1,369)", "MultiWOZ (1,500)", "Programmatic Treatment"],
        rows=[
            ["Duplicate IDs / Empty turns", "Primary key / strip()", "0", "0", "Verified 100% unique & non-empty"],
            ["Exact duplicate text", "SHA-256 text hash", "1", "0", "Removed duplicate (`bf46892e...`)"],
            ["Aborted short dialogues", "total_turns < 3", "34", "1", "Excluded (need ≥ 3 turns for prefix routing)"],
            ["Long-tail turn outliers", "> Q3 + 1.5 × IQR", "20 (>30.5t)", "21 (>24.0t)", "Retained (real negotiations); log-transformed in RQ4"],
            ["Unobserved slot values", "Slot never stated", "See Table E1", "See Table E1", "Preserved as null (`None`); never imputed"],
            ["Entity leakage risk", "Regex slot/number match", "All exemplars", "All exemplars", "Masked with `[SLOT]` tokens in FAISS index"],
            ["Final Analytic Sample", "Locked post-cleaning", "1,334", "1,499", "Total N = 2,833 analytic dialogues"],
        ],
        col_widths=[1.5, 1.4, 0.9, 0.9, 2.5],
        font_size=9.8,
        align_left_cols=(0, 1, 4),
        highlight_rows=(6,),
    )
    D.add_callout(
        s, 0.35, 5.28, 12.63, 1.80,
        "<b>How We Guarantee Zero Data Leakage Between Discovery and Evaluation (Stratified 70/30 Split, Seed = 42):</b>\n"
        "• The <b>1,334 analytic Frames dialogues</b> were partitioned once into a <b>70% Golden Discovery Set (D_gold, n = 933)</b> and a <b>30% Held-Out Test Set (D_test, n = 401)</b>, stratified on wizard task success (74.3% vs. 74.1%).\n"
        "• <b>Strict Firewall:</b> Every clustering model, PCA projection matrix, L1 logistic prefix router, and FAISS exemplar index is fitted <b>exclusively on D_gold (n = 933)</b>. All out-of-sample routing (RQ1), repeated-measures prompting (RQ2, N = 33), 2 × 2 factorial compliance testing (RQ3, N = 144), and 2 × 3 multi-turn simulations (RQ4, N = 180) are evaluated <b>strictly on D_test (n = 401)</b>.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=11,
    )

    # =========================================================================
    # SLIDE 12: UNIVARIATE & BIVARIATE EXPLORATORY DATA ANALYSIS
    # =========================================================================
    s = D.content_slide(
        "Module 3: Data Authenticity, Schema & EDA",
        "Univariate and Bivariate Exploratory Data Analysis (Tables 6–7 & Figures 1–2)",
        "Dialogue length is driven by slot revisions (r = .602) and package offers (r = .636), validating our negotiation constructs",
        notes="Explain the univariate comparison between Frames and MultiWOZ (Figure 1) and the bivariate parametric/non-parametric correlations (Figure 2 & Table 7).",
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
            "<b>Why We Report Both Pearson <i>r</i> and Spearman ρ:</b> Turn counts and revision counts are right-skewed; reporting linear Pearson <i>r</i> alongside rank-based Spearman ρ proves correlations are not artifacts of tail outliers.",
            "<b>Frames vs. MultiWOZ Dispersion:</b> Frames has 51% wider turn dispersion (<i>SD</i> = 6.74 vs. 4.46, range 3–47 turns) because consultative vacation negotiation involves iterative trade-offs.",
            "<b>Golden vs. Held-Out Balance:</b> Golden (<i>M</i> = 14.94 turns) and Held-Out (<i>M</i> = 14.81 turns) partitions are statistically indistinguishable, confirming an unbiased split.",
        ],
        font_size=10.5,
    )

    # =========================================================================
    # SLIDE 13: MULTIVARIATE EDA — SPEARMAN MATRIX & PCA BIPLOT
    # =========================================================================
    s = D.content_slide(
        "Module 3: Data Authenticity, Schema & EDA",
        "Multivariate EDA: Correlation Structure & Principal Component Biplot (Figure 3)",
        "Ten structural and behavioral variables span three orthogonal dimensions explaining 68.6% of total variance",
        notes="Explain how Figure 3 (Panel A Spearman heatmap and Panel B PCA biplot) shows that travel behavior forms a continuous 3D manifold structured around Exploration, Decisiveness, and Verbosity.",
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
    # SLIDE 14: WHY EACH STATISTICAL TEST WAS CHOSEN + REAL-WORLD ANALOGIES
    # =========================================================================
    s = D.content_slide(
        "Module 4: Ground-Up Statistical Methodology",
        "Why Each Statistical Test Was Chosen & Everyday Real-World Analogies",
        "Requirement #1: Explaining the exact statistical test choice for RQ1–RQ4 with intuitive real-world parallels",
        notes="Crucial slide for both math and non-AI professors: explains WHY One-Way ANOVA, Repeated-Measures ANOVA, 2x2 Factorial ANOVA, and 2x3 Factorial ANOVA are the exact right tools, using everyday analogies.",
    )
    D.add_table(
        s, 0.35, 1.50, 12.63, 5.55,
        headers=["RQ & Experimental Structure", "Chosen Statistical Test", "Why This Exact Test Is Mathematically Required", "Classic Real-World Analogy (Where This Test Is Standard)", "Why Our Chatbot Scenario Is Identical"],
        rows=[
            [
                "RQ1: Comparing 3 Clustering Algorithms across N = 159 independent runs\n(3 groups, 1 continuous DV: Silhouette)",
                "One-Way Between-Subjects ANOVA\n+ Welch's ANOVA\n+ Kruskal–Wallis H\n+ Tukey HSD / Games–Howell",
                "Comparing means of k = 3 independent groups at once. Running three separate t-tests would inflate Type I false-positive risk from 5% to 1 − (0.95)³ = 14.3%. Omnibus ANOVA controls α = .05 across all 3 algorithms.",
                "<b>Clinical Trial Comparing 3 Blood-Pressure Drugs:</b>\n159 patients randomly assigned (53 per drug) to Drug A, Drug B, or Drug C; measure blood-pressure drop.",
                "Each of our 159 subsample runs (53 K-Means, 53 Ward, 53 HDBSCAN) is an independent trial producing a continuous Silhouette score.",
            ],
            [
                "RQ2: Testing 3 Prompting Strategies on the SAME N = 33 held-out dialogues\n(Within-subjects design, 99 calls)",
                "One-Way Repeated-Measures ANOVA\n(Greenhouse–Geisser ε correction)\n+ Friedman χ² Test\n+ Holm Paired t-tests",
                "Every dialogue is tested under ALL 3 prompts (Zero-Shot, Static, Cluster-Adaptive). Repeated-Measures ANOVA subtracts out baseline dialogue-to-dialogue difficulty variance, isolating the pure within-dialogue effect of the prompt.",
                "<b>Coffee Tasting Panel (Crossover Trial):</b>\nThe same 33 expert tasters rate Blend A, Blend B, and Blend C. Separating taster-level harshness makes the test much more sensitive.",
                "Dialogues vary wildly in topic and difficulty. Evaluating all 3 prompts on the exact same 33 dialogue prefixes removes dialogue noise (ρ = .50).",
            ],
            [
                "RQ3: Crossing Rules Mode (Off vs. Active) × Prompting (Zero-Shot vs. Cluster-Adaptive)\n(N = 144, n = 36/cell)",
                "2 × 2 Between-Subjects Factorial ANOVA\n+ HC3 Robust SE\n+ Aligned Rank Transform (ART) ANOVA",
                "We have TWO simultaneous independent variables (Rules Mode and Prompting Mode). Only a 2 × 2 Factorial ANOVA can test (1) Main Effect of Rules, (2) Main Effect of Prompting, and (3) their INTERACTION (Rules × Prompting).",
                "<b>Agricultural Crop Yield Trial (Fertilizer × Irrigation):</b>\nTesting whether Fertilizer only boosts yield when Irrigation is ALSO active (synergistic / protective interaction).",
                "Cluster-Adaptive prompting leaks entities when Rules are Off (.359), but Rules Active eliminates that leakage (.000)—a classic protective interaction!",
            ],
            [
                "RQ4: Crossing Prompting (2 levels) × Traveler Archetype (3 levels)\n(N = 180, n = 30/cell)",
                "2 × 3 Between-Subjects Factorial ANOVA on log(Turns) & RER\n+ HC3 + ART\n+ Welch Simple Contrasts",
                "Tests whether the turn-saving benefit of Cluster-Adaptive prompting is uniform across all travelers or moderated by Traveler Archetype (2 × 3 Interaction), using log(Turns) to normalize right-skewed count data.",
                "<b>Education Trial (Teaching Method × Student Learning Style):</b>\nTesting whether interactive tutoring vs. lecture helps Visual, Auditory, and Hands-On learners by different amounts.",
                "All 3 archetypes benefit from adaptive prompting, but Rigid-Constraint Seekers gain the most (−42.7% vs. −29.5%), creating a 2 × 3 interaction.",
            ],
        ],
        col_widths=[1.9, 1.9, 2.8, 3.0, 3.0],
        font_size=9.8,
        align_left_cols=(0, 1, 2, 3, 4),
        highlight_rows=(0, 1, 2, 3),
    )

    # =========================================================================
    # SLIDE 15: MATHEMATICAL MECHANICS OF ANOVA & INTERACTIONS (FOR NON-STATS & STATS PROFS)
    # =========================================================================
    s = D.content_slide(
        "Module 4: Ground-Up Statistical Methodology",
        "How ANOVA, Effect Sizes (η²), and Factorial Interactions Work",
        "Translating F-ratios, Greenhouse–Geisser corrections, and interaction terms into intuitive signal-to-noise ratios",
        notes="Explain the intuition of F = Signal / Noise, eta-squared = % of variance explained, and how to interpret main effects vs. interactions.",
    )
    D.add_card(
        s, 0.35, 1.50, 4.05, 3.70,
        title="1. The F-Statistic: Signal-to-Noise Ratio",
        header_bg=NAVY,
        bullets=[
            "<b>Formula:</b>  <i>F</i> = MS<sub>between</sub> / MS<sub>within (error)</sub>",
            "<b>Plain-English Intuition:</b>",
            (1, "<b>Numerator (Signal):</b> How far apart are the group means (e.g., Rules Active vs. Rules Off)?"),
            (1, "<b>Denominator (Noise):</b> How much random scatter exists <i>inside</i> each group?"),
            "<b>How to Read <i>F</i> in Our Tables:</b>",
            (1, "If null hypothesis <i>H</i><sub>0</sub> is true (no real difference), <i>F</i> ≈ 1.0."),
            (1, "In our study, we observe <b><i>F</i> = 91.33 (RQ1)</b>, <b><i>F</i> = 9.79 (RQ2)</b>, <b><i>F</i> = 43.92 & 489.52 (RQ3)</b>, and <b><i>F</i> = 664.43 (RQ4)</b>—meaning the treatment signal is 10 to 664 times larger than random noise (all <i>p</i> < .001)!"),
        ],
        font_size=10.8,
    )
    D.add_card(
        s, 4.60, 1.50, 4.10, 3.70,
        title="2. Effect Size (η² and Partial ηp²): Practical Magnitude",
        header_bg=TEAL,
        bullets=[
            "<b>Formula:</b>  η<sub><i>p</i></sub><sup>2</sup> = SS<sub>effect</sub> / (SS<sub>effect</sub> + SS<sub>error</sub>)",
            "<b>Why <i>p</i>-values Alone Are Not Enough:</b>",
            (1, "A <i>p</i>-value (< .001) only tells us an effect is <i>not zero</i>; η<sub><i>p</i></sub><sup>2</sup> tells us <i>what percentage of outcome variance is explained</i> by our factor."),
            "<b>Cohen's (1988) Standard Benchmarks:</b>",
            (1, "Small: η<sup>2</sup> = .01 (1% variance)"),
            (1, "Medium: η<sup>2</sup> = .06 (6% variance; <i>f</i> = .25)"),
            (1, "Large: η<sup>2</sup> ≥ .14 (14%+ variance; <i>f</i> ≥ .40)"),
            "<b>Our Observed Effect Sizes:</b>",
            (1, "Every primary effect in RQ1–RQ4 is <b>Large</b>: RQ1 η<sup>2</sup> = .54–.91; RQ2 η<sub><i>p</i></sub><sup>2</sup> = .234; RQ3 η<sub><i>p</i></sub><sup>2</sup> = .239–.778; RQ4 η<sub><i>p</i></sub><sup>2</sup> = .793."),
        ],
        font_size=10.8,
    )
    D.add_card(
        s, 8.90, 1.50, 4.08, 3.70,
        title="3. Main Effects vs. Interaction Effects (A × B)",
        header_bg=BLUE,
        bullets=[
            "<b>Main Effect of Factor A:</b> Does changing A (e.g., turning Rules On) change the outcome on average across all levels of B?",
            "<b>Interaction Effect (A × B):</b> Does the effect of A <i>depend on</i> which level of B is active?",
            "<b>Visual Rule of Thumb on Line Plots:</b>",
            (1, "<b>Parallel lines</b> = No interaction (effects are purely additive)."),
            (1, "<b>Non-parallel / diverging / crossing lines</b> = Significant interaction!"),
            "<b>Why Interactions Matter in RQ3 & RQ4:</b>",
            (1, "In RQ3, entity leakage only happens in <i>Rules Off × Cluster-Adaptive</i> (.359) and vanishes when <i>Rules Active</i> is turned on (.000) → strong diverging lines (<i>F</i> = 34.82, <i>p</i> < .001)."),
        ],
        font_size=10.8,
    )
    D.add_callout(
        s, 0.35, 5.38, 12.63, 1.68,
        "<b>Why We Apply Greenhouse–Geisser (GG) Correction in RQ2 (Greenhouse & Geisser, 1959):</b>\n"
        "In Repeated-Measures ANOVA (RQ2), standard <i>F</i>-tables assume <i>sphericity</i>—that the variance of differences between every pair of conditions (Zero-Shot vs. Static, Zero-Shot vs. Adaptive, Static vs. Adaptive) is equal. When sphericity is violated (ε < 1.0, e.g., ε = 0.94 in style cosine and ε = 0.65 in pacing error), unadjusted <i>F</i>-tests inflate false positives. Multiplying degrees of freedom by ε (e.g., <i>df</i> = 1.88, 60.29) yields an exact, conservative <i>p</i>-value.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=11,
    )

    # =========================================================================
    # SLIDE 16: TRIANGULATED ROBUSTNESS (PARAMETRIC + WELCH/HC3 + NON-PARAMETRIC ART)
    # =========================================================================
    s = D.content_slide(
        "Module 4: Ground-Up Statistical Methodology",
        "Bulletproof Inference: Why We Pair Parametric, Robust, and Non-Parametric Tests",
        "Ensuring no statistical objection can arise from non-normality, bounded [0, 1] rates, or unequal cell variances",
        notes="Explain to statistics professors on the committee why we run THREE layers of tests on every single hypothesis.",
    )
    D.add_table(
        s, 0.35, 1.50, 12.63, 4.35,
        headers=["Potential Statistical Objection", "Where It Occurs in Dialogue Data", "Our Robust Parametric Solution", "Our Distribution-Free Non-Parametric Solution", "Concordance Across All 4 RQs"],
        rows=[
            [
                "1. Heteroscedasticity\n(Unequal variances across cells)",
                "In RQ3, when Rules Active eliminates leakage to 0.0%, variance in that cell drops near zero while Rules Off has high variance (SD = .348).",
                "<b>Welch's ANOVA (RQ1) & MacKinnon–White HC3 Sandwich SEs (RQ3, RQ4):</b>\nEstimates cell-specific error variances without pooling.",
                "<b>Games–Howell Post Hoc (RQ1) & Mann–Whitney U (RQ4):</b>\nRequires zero equal-variance assumptions.",
                "100% agreement: e.g., RQ3 RAR OLS F = 43.92 (p < .001) vs. HC3 F = 42.71 (p < .001).",
            ],
            [
                "2. Non-Normality & Bounded Proportions [0, 1]",
                "RAR, ELR, Slot F1 (RQ3), and RER (RQ4) are proportions bounded between 0 and 1 with floor/ceiling clustering.",
                "<b>Balanced Cell Sizes (n = 36/cell in RQ3, n = 30/cell in RQ4):</b>\nCentral Limit Theorem stabilizes cell means.",
                "<b>Aligned Rank Transform (ART) Factorial ANOVA (Wobbrock et al., 2011):</b>\nAligns data for each main/interaction effect before ranking, allowing exact non-parametric factorial ANOVA!",
                "100% agreement: RQ3 Leakage Interaction OLS F = 34.82 (p < .001) vs. ART F = 2148.81 (p < .001).",
            ],
            [
                "3. Right-Skewed Positive Count Data",
                "Multi-turn dialogue length (Turns to Goal Completion in RQ4) is strictly positive and right-skewed.",
                "<b>Natural Log Transformation:</b>\nPrimary DV pre-registered as Y = ln(Turns), plus raw Turns reported side-by-side.",
                "<b>Mann–Whitney U & ART ANOVA on Both Raw and Log Turns:</b>\nRank-invariant to any monotone transformation.",
                "100% agreement: RQ4 Interaction OLS F = 10.89 (p < .001), HC3 F = 8.58 (p < .001), ART F = 209.46 (p < .001).",
            ],
            [
                "4. Correlated Within-Dialogue Skewness",
                "In RQ2, 33 dialogues are measured 3 times; cosine similarity can have mild negative skew.",
                "<b>Greenhouse–Geisser Sphericity-Corrected RM-ANOVA + Holm Step-Down t-tests.</b>",
                "<b>Friedman Non-Parametric Rank Test (χ²):</b>\nRanks the 3 conditions (1st, 2nd, 3rd) inside each dialogue.",
                "100% agreement: RQ2 Style RM-ANOVA F = 9.79 (p < .001) vs. Friedman χ²(2) = 12.50 (p = .002).",
            ],
        ],
        col_widths=[2.0, 2.6, 2.7, 2.8, 2.5],
        font_size=9.8,
        align_left_cols=(0, 1, 2, 3, 4),
    )
    D.add_callout(
        s, 0.35, 6.00, 12.63, 1.05,
        "<b>Defense Takeaway for Methodology Reviewers:</b> Every single hypothesis test in this study is reported as a <b>triad</b>: (1) Classical Parametric ANOVA, (2) Heteroscedasticity-Consistent (`Welch` / `HC3`) ANOVA, and (3) Non-Parametric (`Kruskal–Wallis` / `Friedman` / `ART`) ANOVA. Because all three reach <i>p</i> < .001 on every RQ, our conclusions are mathematically invariant to distributional assumptions.",
        bg_color=GREEN_BG, border_color=GREEN, font_size=11,
    )

    # =========================================================================
    # SLIDE 17: PROVEN CONCEPTS FOR SAMPLE SIZE PARAMETERS (α, 1−β, f, λ)
    # =========================================================================
    s = D.content_slide(
        "Module 4: Ground-Up Statistical Methodology",
        "Proven Concepts Behind Sample-Size Parameters: α, Power (1 − β), Cohen's f, and λ",
        "Requirement #2 & Defense Question #1: How standard noncentral-F parameters determine exact sample sizes",
        notes="Directly addresses Requirement #2 and Defense Question #1: Explain alpha, beta, power, Cohen's f, and the noncentrality parameter lambda.",
    )
    D.add_card(
        s, 0.35, 1.50, 5.95, 3.55,
        title="The Noncentral-F Power Formulation (Cohen, 1988; Faul et al., 2007)",
        header_bg=NAVY,
        bullets=[
            "<b>Exact Power Equation (Equation 1 in Report):</b>",
            (1, "<b>Power (1 − β) = 1 − <i>F</i><sub>nc</sub>(<i>F</i><sub>crit</sub> ; <i>df</i><sub>1</sub>, <i>df</i><sub>2</sub>, λ)</b>,  where <i>F</i><sub>crit</sub> = <i>F</i><sub>1−α</sub>(<i>df</i><sub>1</sub>, <i>df</i><sub>2</sub>)"),
            "<b>What Each Proven Parameter Means:</b>",
            (1, "<b>α = .05 (Type I Error Rate):</b> Maximum 5% probability of declaring a false positive when the null hypothesis <i>H</i><sub>0</sub> is true."),
            (1, "<b>β = .20 → Power (1 − β) ≥ .80:</b> Minimum 80% probability of detecting a true effect when <i>H</i><sub>a</sub> is true (4-to-1 ratio of β to α recommended by Cohen, 1988)."),
            (1, "<b>Cohen's <i>f</i> = .25 (Medium Effect Size):</b> Signal SD is 25% of within-group error SD (equivalent to η<sup>2</sup> = <i>f</i><sup>2</sup> / (1 + <i>f</i><sup>2</sup>) = .0588, or ~6% explained variance)."),
            (1, "<b>Noncentrality Parameter (λ):</b> Measures total statistical shift away from <i>H</i><sub>0</sub>:\n"
                "      • Between-subjects (RQ1, RQ3, RQ4):  <b>λ = <i>f</i><sup>2</sup> · <i>N</i></b>\n"
                "      • Repeated-measures (RQ2, <i>m</i>=3, ρ=.50):  <b>λ = <i>f</i><sup>2</sup> · <i>N</i> · <i>m</i> · ε / (1 − ρ)</b>"),
        ],
        font_size=10.5,
    )
    D.add_table(
        s, 6.50, 1.50, 6.48, 3.55,
        headers=["RQ", "Planned Design", "df at N_min", "λ at N_min", "F_crit", "N_min (.80)", "Final N (+10% Buffer)", "Final Power"],
        rows=[
            ["RQ1", "One-way ANOVA (3 groups)", "2, 155", "9.88", "3.05", "158", "159 (53 / alg)", ".804"],
            ["RQ2", "RM-ANOVA (3 conds, ρ=.50)", "2, 54", "10.50", "3.17", "28", "33 (99 calls)", ".865"],
            ["RQ3", "2 × 2 Factorial (df1 = 1)", "1, 124", "8.00", "3.92", "128", "144 (36 / cell)", ".847"],
            ["RQ4", "2 × 3 Factorial (df1 = 2)", "2, 152", "9.88", "3.06", "158", "180 (30 / cell)", ".857"],
        ],
        col_widths=[0.6, 1.7, 0.7, 0.7, 0.6, 0.7, 1.1, 0.7],
        font_size=10,
        align_left_cols=(0, 1),
        highlight_rows=(0, 1, 2, 3),
    )
    D.add_callout(
        s, 0.35, 5.20, 12.63, 1.85,
        "<b>Why λ (Noncentrality) Is the Key Bridge Between Effect Size (f) and Sample Size (N):</b>\n"
        "• To achieve 80% power at α = .05, the noncentral <i>F</i> distribution requires a minimum noncentrality shift of <b>λ ≈ 7.85 to 9.88</b> (depending on numerator <i>df</i><sub>1</sub> = 1 or 2).\n"
        "• Since <b>λ = <i>f</i><sup>2</sup> · <i>N</i></b> and <i>f</i><sup>2</sup> = (0.25)<sup>2</sup> = 0.0625, solving 0.0625 · <i>N</i> ≈ 8.00 immediately yields <b><i>N</i><sub>min</sub> = 128</b> for <i>df</i><sub>1</sub> = 1 (RQ3) and solving 0.0625 · <i>N</i> ≈ 9.88 yields <b><i>N</i><sub>min</sub> = 158</b> for <i>df</i><sub>1</sub> = 2 (RQ1, RQ4)!\n"
        "• In RQ2, because each dialogue acts as its own control across <i>m</i> = 3 conditions with within-subject correlation ρ = .50, the variance is halved by (1 − ρ) = 0.50, multiplying λ by <i>m</i>/(1−ρ) = 6 and requiring only <b><i>N</i><sub>min</sub> = 28 dialogues</b> (buffered to <i>N</i> = 33, power = .865).",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=10.8,
    )

    # =========================================================================
    # SLIDE 18: COUNTERFACTUAL EXAMPLES — WHAT HAPPENS IF α, f, λ ARE MISCHOSEN?
    # =========================================================================
    s = D.content_slide(
        "Module 4: Ground-Up Statistical Methodology",
        "Counterfactual Analysis: What Happens If α, Power, f, or λ Are Mischosen?",
        "Requirement #2: Concrete numerical demonstrations of how improper parameter choices break experimental validity",
        notes="Walk through the 4 counterfactual scenarios so the committee sees what goes wrong if a researcher picks arbitrary sample sizes or alpha levels.",
    )
    D.add_table(
        s, 0.35, 1.50, 12.63, 4.35,
        headers=["Parameter Choice Scenario", "Altered Value vs. Standard", "Resulting Noncentrality λ & Sample Size N", "Statistical & Practical Consequence", "Concrete Example in Our Travel Chatbot Study"],
        rows=[
            [
                "Failure Mode 1:\nArbitrary Small Sample\n(Underpowered λ)",
                "Pick N = 36 total (9 per cell in RQ3) instead of N = 144\n→ λ drops from 9.00 to 2.25!",
                "λ = 0.0625 × 36 = 2.25\nPower 1 − β drops from .847 to .308 (69.2% Type II error rate!)",
                "<b>Severe False Negative Risk:</b> Nearly 7 out of 10 times, a genuine medium improvement (f = .25) will produce p > .05 and be falsely dismissed as 'no effect'.",
                "In RQ4, the Prompting × Archetype interaction has ηp² = .111 (f = .35). At N = 36 total (6/cell), power to detect this interaction drops to .44—we would have missed the persona moderation effect!",
            ],
            [
                "Failure Mode 2:\nLoose Significance α\n(Inflated Type I Error)",
                "Set α = .20 instead of α = .05 to 'make it easier to get significance'",
                "F_crit drops from 3.92 to 1.66 (at df = 1, 140)",
                "<b>20% False Positive Risk:</b> Across 4 RQs with multiple metrics, random LLM sampling noise would be falsely published as a scientific improvement.",
                "In Primary RQ2 (coarse routing), style cosine had F = 1.61, p = .211. A loose α = .25 would have falsely claimed coarse routing worked, hiding the need to fix RQ1 prefix routing!",
            ],
            [
                "Failure Mode 3:\nOverly Tiny Target Effect\n(Overpowered for Noise)",
                "Set f = .05 (η² = .0025, 0.25% variance) instead of f = .25",
                "Needs λ = 9.88 with f² = .0025\n→ Requires N = 3,952 dialogues (exceeds the entire Frames corpus of 1,334!)",
                "<b>Trivial Practical Significance & Exhausted Corpus:</b> Wastes thousands of API calls to detect a 0.05-turn difference that has zero business value.",
                "Even if an OTA chatbot saved 0.04 turns (p < .05 at N = 4,000), customers cannot perceive a 0.04-turn difference. Medium effect f = .25 ensures statistical significance aligns with business value.",
            ],
            [
                "Failure Mode 4:\nIgnoring Repeated-Measures ρ in RQ2",
                "Assume ρ = .00 (between-subjects formula) or ρ = .90 (over-optimistic)",
                "If ρ = .90 assumed: N_min = 7 dialogues (severely underpowered if true ρ = .50).\nIf between-subjects used: N = 159 dialogues × 3 = 477 calls.",
                "<b>Miscalibrated Within-Subject Sensitivity:</b> Setting conservative ρ = .50 with a +18% buffer (N = 33 vs. N_min = 28) protects against sphericity loss (ε = 0.65–0.94).",
                "In Refined RQ2, pacing error had Greenhouse–Geisser ε = 0.65. Because we buffered N from 28 to 33, even under ε = 0.65 our test achieved F(1.30, 41.70) = 7.10, p = .007!",
            ],
        ],
        col_widths=[1.8, 2.1, 2.2, 3.0, 3.5],
        font_size=9.8,
        align_left_cols=(0, 1, 2, 3, 4),
    )
    D.add_callout(
        s, 0.35, 6.00, 12.63, 1.05,
        "<b>Summary Rule for Defense Committee:</b> Standard values (<b>α = .05, 1 − β = .80, <i>f</i> = .25, ρ = .50</b>, plus a <b>10% cell-balancing buffer</b>) sit at the exact mathematical sweet spot: large enough (λ = 8.0–10.5) to guarantee >83% detection of meaningful engineering gains, yet compact enough to fit strictly inside the 401 held-out test dialogues of Microsoft Frames.",
        bg_color=CALLOUT_BG, border_color=GOLD, font_size=11,
    )

    # =========================================================================
    # SLIDE 19: DOMAIN HYPERPARAMETERS — WHY λ_d = 0.15 AND M = 9 USER MESSAGES?
    # =========================================================================
    s = D.content_slide(
        "Module 4: Ground-Up Statistical Methodology",
        "Domain Parameter Choices: Why Decay λ_d = 0.15 and Prefix Horizon M = 9?",
        "Mathematical justification and sensitivity proof for our trajectory pooling and truncation parameters",
        notes="Explain the other two lambda/horizon parameters in our paper: exponential turn decay lambda_d = 0.15 (Eq. 2) and truncation horizon M = 9 user messages.",
    )
    D.add_card(
        s, 0.35, 1.50, 6.15, 5.45,
        title="1. Exponential Turn Decay λ_d = 0.15 (Equation 2 in Report)",
        header_bg=NAVY,
        bullets=[
            "<b>Mathematical Formula (Eq. 2):</b>",
            (1, "<b>v = Σ <i>w<sub>t</sub></i> e<sub><i>t</i></sub></b>,   where  <b><i>w<sub>t</sub></i> ∝ exp[−λ<sub>d</sub>(<i>T</i> − <i>t</i>)]</b>"),
            "<b>Why λ<sub>d</sub> = 0.15 Is Used for Trajectory Pooling:</b>",
            (1, "In a multi-turn travel dialogue, Turn 1 is often a generic greeting (<i>'Hi, can you help me?'</i>), while recent turns contain active constraint negotiation."),
            (1, "With λ<sub>d</sub> = 0.15, the most recent turn gets weight 1.00, 3 turns ago gets exp(−0.45) = 0.64, and 10 turns ago gets exp(−1.50) = 0.22—preserving full history while emphasizing active negotiation."),
            "<b>What Happens If λ<sub>d</sub> Is Chosen Poorly (Sensitivity Grid `step2b`):</b>",
            (1, "<b>If λ<sub>d</sub> = 0.0 (Uniform Mean):</b> Opening pleasantries dilute active negotiation constraints."),
            (1, "<b>If λ<sub>d</sub> ≥ 1.0 (Memoryless Last-Turn Only):</b> Forgets early trip constraints stated in Turn 2."),
            (1, "<b>Empirical Check (`t_rq1_rep_matrix.csv`):</b> Testing R0 (λ<sub>d</sub>=0.15), R1 (user-only), and R2 (concatenated) confirmed that embedding pooling alone only reaches ARI = .25–.54, motivating our hybrid `Blocks` representation!"),
        ],
        font_size=10.5,
    )
    D.add_card(
        s, 6.80, 1.50, 6.18, 5.45,
        title="2. Truncation Horizon M = 9 User Messages (`step2g` & `step2h`)",
        header_bg=TEAL,
        bullets=[
            "<b>Why We Must Truncate Before the End of the Conversation:</b>",
            (1, "If we cluster <i>whole conversations</i>, the final turns contain <i>'Great, book it!'</i> vs. <i>'Never mind, too expensive'</i>. The clusters then trivially reflect <b>session outcome</b> (Outcome Cramér's <i>V</i> = .29) rather than <b>how the customer shops</b>!"),
            "<b>What Happens Across Different Values of <i>M</i> (Table D5 Proof):</b>",
            (1, "<b><i>M</i> = 3 user messages:</b> Stability ARI = .69, but many explorers haven't finished stating initial preferences (held-out routing accuracy = 59.4%, κ = .359)."),
            (1, "<b><i>M</i> = 5 user messages:</b> Stability ARI = .57; held-out routing jumps to <b>70.1% (κ = .535)</b>—strong enough for mid-conversation RQ2 prompting!"),
            (1, "<b><i>M</i> = 7 user messages:</b> Stability ARI = .69; held-out routing reaches <b>82.0% (κ = .722)</b>."),
            (1, "<b><i>M</i> = 9 user messages (Adopted Golden Definition):</b> 38.6% of long dialogues are truncated (eliminating end-of-dialogue outcome leakage, <i>V</i> = .20), bootstrap stability peaks at <b>ARI = .76</b> (<b>74.8% core membership</b>), and held-out prefix routing reaches <b>97.3% (κ = .958)</b>!"),
        ],
        font_size=10.5,
    )

    # =========================================================================
    # SLIDE 20: END-TO-END NEURO-SYMBOLIC SYSTEM ARCHITECTURE (FIGURE 4)
    # =========================================================================
    s = D.content_slide(
        "Module 5: System Architecture & Workflows",
        "End-to-End Five-Layer Neuro-Symbolic System Architecture (Figure 4)",
        "Strict separation between Offline Golden Discovery (D_gold, n = 933) and Online Runtime Execution (D_test, n = 401)",
        notes="Walk the committee through Figure 4: Layers 1–2 run offline on D_gold; Layers 3–5 run online on D_test.",
    )
    D.add_figure(
        s, os.path.join(FIG_FIN, "fig_system_architecture.png"),
        0.35, 1.50, 8.25, 5.55,
        caption="Figure 4: Five-Layer Neuro-Symbolic Cluster-Adaptive Conversational System Architecture",
    )
    D.add_card(
        s, 8.75, 1.50, 4.23, 5.55,
        title="Architectural Walkthrough",
        header_bg=NAVY,
        bullets=[
            "<b>Layer 1 (Canonical Ingestion):</b> Parses raw Frames & MultiWOZ JSON into validated Two-Tier Pydantic trajectories.",
            "<b>Layer 2 (Offline Discovery on D_gold = 933):</b>",
            (1, "Extracts first <i>M</i> = 9 user messages."),
            (1, "Computes PCA-20 of 3,072-d Gemini prefix embeddings + 16-field LLM behavioral profile (`Blocks`)."),
            (1, "Freezes <i>k</i> = 3 K-Means centroids, L1 logistic router, and 3 slot-masked FAISS `IndexFlatIP` sub-indices."),
            "<b>Layer 3 (Online Prefix Router & FAISS Retrieval):</b>",
            (1, "Projects live test prefix into golden `Blocks` space (< 2 ms) and retrieves <i>k</i> = 3 `[SLOT]`-masked exemplars."),
            "<b>Layer 4 (Symbolic Guardrails & Generation):</b>",
            (1, "Updates <i>Verified Informed Slot Ledger</i> (prevents re-asking)."),
            (1, "Evaluates 5 YAML rules (`src/rule_engine.py`, < 1 ms) + sanitizes post-generation entity leakage."),
            "<b>Layer 5 (Evaluation & Dual-Judge Audit):</b>",
            (1, "Scores Style Cosine, RAR, ELR, Slot F1, TGC, RER + cross-validates with `gemini-2.5-pro` (κ = .917 & .933)."),
        ],
        font_size=9.8,
    )

    # =========================================================================
    # SLIDE 21: ALGORITHMIC EXECUTION WORKFLOWS ACROSS RQ1–RQ4 (FIGURE 5)
    # =========================================================================
    s = D.content_slide(
        "Module 5: System Architecture & Workflows",
        "Algorithmic Execution Workflows Across RQ1 to RQ4 (Figure 5)",
        "Visualizing the exact experimental pipeline, sample sizes, and statistical tests for each research question",
        notes="Use Figure 5 to orient the committee before diving into the empirical results of RQ1, RQ2, RQ3, and RQ4.",
    )
    D.add_figure(
        s, os.path.join(FIG_FIN, "fig_rq_workflows_4panel.png"),
        0.35, 1.50, 8.35, 5.55,
        caption="Figure 5: Four-Panel Algorithmic Execution Workflows for RQ1 (A), RQ2 (B), RQ3 (C), and RQ4 (D)",
    )
    D.add_card(
        s, 8.85, 1.50, 4.13, 5.55,
        title="How the Four Pipelines Connect",
        header_bg=TEAL,
        bullets=[
            "<b>Panel A (RQ1 — Unsupervised Discovery):</b>",
            (1, "159 subsample runs (53 × 3 algorithms) on MiniLM & Gemini embeddings → Representation × Truncation grid → 3 Refined Archetypes & `RefinedArchetypeRouter`."),
            "<b>Panel B (RQ2 — Within-Subject Prompting):</b>",
            (1, "33 held-out dialogues × 3 conditions = 99 calls. Contrasts Primary Archetypes (κ=.24) vs. Refined Archetypes (κ=.535)."),
            "<b>Panel C (RQ3 — 2 × 2 Factorial Guardrails):</b>",
            (1, "144 held-out scenarios (36/cell; 50% violating) crossing `Rules Off/Active` × `Zero-Shot/Cluster-Adaptive` + 48-unit `gemini-2.5-pro` dual-judge audit."),
            "<b>Panel D (RQ4 — 2 × 3 Multi-Turn Simulation):</b>",
            (1, "180 closed-loop simulations (30/cell) crossing `Zero-Shot/Cluster-Adaptive` × 3 Refined Archetypes + 45-unit blind persona fidelity audit."),
        ],
        font_size=10.2,
    )
