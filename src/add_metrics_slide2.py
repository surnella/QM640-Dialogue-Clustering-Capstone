"""
Populate Slide 2 of `final/Conversational_Quality_Turn_Economy_Editable.pptx`
WITHOUT modifying the user's edited Slide 1 (`prs.slides[0]`).

Slide 2 presents all actionable metrics tracked inside each block to improve
the conversational solution up to the point of Turn Economy (`Interactions to Lead`
and `Interactions to Quote`), and explicitly shows on the right side why
Converted Booking metrics cannot be correlated with these conversational metrics
(forcing a correlation injects exogenous noise into the system).
"""

import os
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PPTX_PATH = os.path.join(ROOT, "final", "Conversational_Quality_Turn_Economy_Editable.pptx")


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


def add_zone_box(slide, left, top, width, height, title, bg_hex, border_hex, dashed=False):
    box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(height),
    )
    box.adjustments[0] = 0.02
    box.fill.solid()
    box.fill.fore_color.rgb = rgb(bg_hex)
    box.line.color.rgb = rgb(border_hex)
    box.line.width = Pt(1.75)
    if dashed:
        set_line_dash(box, "dash")

    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Inches(0.10)
    tf.margin_top = Inches(0.04)
    tf.margin_right = Inches(0.10)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    r.text = title
    r.font.name = "Calibri"
    r.font.size = Pt(10.0)
    r.font.bold = True
    r.font.color.rgb = rgb(border_hex)
    return box


def add_card(
    slide, left, top, width, height, title, bullets,
    bg_hex="#FFFFFF", border_hex="#1565C0", title_hex=None,
    shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, font_size=7.6, dashed=False,
):
    sh = slide.shapes.add_shape(
        shape_type, Inches(left), Inches(top), Inches(width), Inches(height),
    )
    if shape_type == MSO_SHAPE.ROUNDED_RECTANGLE:
        sh.adjustments[0] = 0.04
    sh.fill.solid()
    sh.fill.fore_color.rgb = rgb(bg_hex)
    sh.line.color.rgb = rgb(border_hex)
    sh.line.width = Pt(1.4)
    if dashed:
        set_line_dash(sh, "dash")

    tf = sh.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Inches(0.07)
    tf.margin_right = Inches(0.07)
    tf.margin_top = Inches(0.05)
    tf.margin_bottom = Inches(0.04)

    p0 = tf.paragraphs[0]
    p0.alignment = PP_ALIGN.LEFT
    p0.space_after = Pt(1.8)
    r0 = p0.add_run()
    r0.text = title
    r0.font.name = "Calibri"
    r0.font.size = Pt(font_size + 0.9)
    r0.font.bold = True
    r0.font.color.rgb = rgb(title_hex or border_hex)

    for b in bullets:
        p = tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(1.0)
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


def add_connector(
    slide, x1, y1, x2, y2, color_hex="#37474F", width_pt=1.75,
    dashed=False, both_ends=False, label=None, label_x=None, label_y=None,
    label_w=1.55, label_h=0.25, label_bg="#FFFFFF", label_border=None,
):
    conn = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT,
        Inches(x1), Inches(y1), Inches(x2), Inches(y2),
    )
    conn.line.color.rgb = rgb(color_hex)
    conn.line.width = Pt(width_pt)
    if dashed:
        set_line_dash(conn, "dash")
    add_arrow_head(conn, head_end=True, tail_end=both_ends)

    if label:
        lx = label_x if label_x is not None else (x1 + x2) / 2 - label_w / 2
        ly = label_y if label_y is not None else (y1 + y2) / 2 - label_h / 2
        lbl = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(lx), Inches(ly), Inches(label_w), Inches(label_h),
        )
        lbl.adjustments[0] = 0.15
        lbl.fill.solid()
        lbl.fill.fore_color.rgb = rgb(label_bg)
        if label_border:
            lbl.line.color.rgb = rgb(label_border)
            lbl.line.width = Pt(1.0)
        else:
            lbl.line.fill.background()
        tf = lbl.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = Inches(0.04)
        tf.margin_right = Inches(0.04)
        tf.margin_top = Inches(0.02)
        tf.margin_bottom = Inches(0.02)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = label
        r.font.name = "Calibri"
        r.font.size = Pt(7.2)
        r.font.bold = True
        r.font.color.rgb = rgb(color_hex)
    return conn


def build_slide2():
    prs = Presentation(PPTX_PATH)
    while len(prs.slides) < 2:
        prs.slides.add_slide(prs.slide_layouts[6])

    s2 = prs.slides[1]
    # Clear any existing shapes on Slide 2 ONLY (Slide 1 is untouched!)
    for sh in list(s2.shapes):
        sp = sh._element
        sp.getparent().remove(sp)

    # Top Title Banner (aligned with User's Slide 1 header position 0.20, 0.15, 12.93x0.53)
    hdr = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.20), Inches(0.15), Inches(12.93), Inches(0.53))
    hdr.adjustments[0] = 0.04
    hdr.fill.solid()
    hdr.fill.fore_color.rgb = rgb("#1B365D")
    hdr.line.fill.background()
    tf = hdr.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.20)
    p = tf.paragraphs[0]
    r1 = p.add_run()
    r1.text = "Metrics Tracked Per Layer to Improve Conversational AI (Up to Turn Economy — Separated from Conversion Noise)"
    r1.font.name = "Calibri"
    r1.font.size = Pt(13.5)
    r1.font.bold = True
    r1.font.color.rgb = rgb("#FFFFFF")

    # =========================================================================
    # TOP-LEFT BAND: LIVE CUSTOMER INTERACTION CHANNELS — RUNTIME METRICS
    # =========================================================================
    add_zone_box(
        s2, 0.20, 0.78, 8.75, 1.82,
        "Live Customer Interaction Channels — Runtime Execution & Turn-Economy Metrics (1 Interaction = Cust + Bot/Agent Turn)",
        bg_hex="#F0F4F8", border_hex="#1565C0",
    )

    add_card(
        s2, 0.32, 1.06, 1.85, 1.45,
        "Customer / Traveler Signals",
        [
            ("• Upfront Slot Share: ", "% of trip constraints stated in Turn 1", "#1B365D"),
            ("• Drop-Off / Abandon Rate: ", "% exiting before Lead/Quote", "#1B365D"),
            ("• Sentiment Trajectory: ", "Shift from frustrated to satisfied", "#1B365D"),
            ("• Option Exploration Depth: ", "# of packages compared", "#1B365D"),
        ],
        bg_hex="#FFFFFF", border_hex="#1B365D", font_size=7.4,
    )

    add_card(
        s2, 2.35, 1.06, 2.22, 1.45,
        "Autonomous Chatbot Metrics",
        [
            ("★ Primary KPI: ", "Interactions to Lead", "#1565C0"),
            ("• Lead Qualification Rate: ", "% reaching verified lead", "#1565C0"),
            ("• Zero-Repeat Slot Capture: ", "% slots filled with 0 re-asking", "#1565C0"),
            ("• Containment Rate: ", "% resolved without escalation", "#1565C0"),
            ("• Bot Response Latency: ", "p95 turn generation time (ms)", "#1565C0"),
        ],
        bg_hex="#E3F2FD", border_hex="#1565C0", font_size=7.4,
    )

    add_card(
        s2, 4.75, 1.06, 1.85, 1.45,
        "Human Sales Agent Metrics",
        [
            ("• Active Turn Handle Time: ", "Avg time per agent turn", "#00695C"),
            ("• Assist Adoption Rate: ", "% of Co-Pilot drafts used", "#00695C"),
            ("• Quote Completeness: ", "% quotes with full pricing/rules", "#00695C"),
            ("• Objection Resolution: ", "% budget conflicts resolved", "#00695C"),
        ],
        bg_hex="#FFFFFF", border_hex="#00695C", font_size=7.4,
    )

    add_card(
        s2, 6.78, 1.06, 2.05, 1.45,
        "Agent Assist Co-Pilot Metrics",
        [
            ("★ Primary KPI: ", "Interactions to Quote", "#00695C"),
            ("• Card Precision@K: ", "Relevance of surfaced Cards", "#00695C"),
            ("• Live Slot Recall: ", "% stated slots auto-logged", "#00695C"),
            ("• Trade-Off Framing Lift: ", "Turns saved on strict budgets", "#00695C"),
        ],
        bg_hex="#E0F2F1", border_hex="#00695C", font_size=7.4,
    )

    add_connector(s2, 2.17, 1.78, 2.35, 1.78, "#1565C0", both_ends=True)
    add_connector(s2, 6.60, 1.78, 6.78, 1.78, "#00695C", both_ends=True)

    # =========================================================================
    # MIDDLE-LEFT BAND: REFERENCE KNOWLEDGE & PERSONALIZATION METRICS
    # =========================================================================
    add_zone_box(
        s2, 0.20, 3.00, 8.75, 1.82,
        "Reference Knowledge & Human-Like Personalization Layer — Pattern, Golden Repository & Knowledge Card Metrics",
        bg_hex="#F3E5F5", border_hex="#6A1B9A",
    )

    add_card(
        s2, 0.35, 3.28, 2.65, 1.45,
        "User Behavioral Pattern Metrics",
        [
            ("• Early Routing Accuracy (κ / F1): ", "Pattern identification within first 3–5 interactions", "#5E35B1"),
            ("• Human-Like Style Similarity: ", "Cosine / rubric match to top human consultants", "#5E35B1"),
            ("• Pacing Calibration Error: ", "|Generated words − Target persona word norm|", "#5E35B1"),
            ("• Persona Drift Detection: ", "Accuracy on mid-chat style shifts", "#5E35B1"),
        ],
        bg_hex="#EDE7F6", border_hex="#5E35B1", font_size=7.4,
    )

    add_card(
        s2, 3.28, 3.28, 2.60, 1.45,
        "Golden Conversations Metrics",
        [
            ("• Scenario Coverage Rate (%): ", "% of live intents matched by Golden Dialogues", "#E65100"),
            ("• Exemplar Retrieval Similarity: ", "Mean nearest-neighbor match score", "#E65100"),
            ("• Golden Win-Rate Lift: ", "Reduction in Interactions to Lead/Quote", "#E65100"),
            ("• Corpus Freshness Rate: ", "% of Golden Dialogues updated per sprint", "#E65100"),
        ],
        bg_hex="#FFF8E1", border_hex="#F57F17", title_hex="#E65100",
        shape_type=MSO_SHAPE.CAN, font_size=7.3,
    )

    add_card(
        s2, 6.15, 3.28, 2.68, 1.45,
        "Agent-Specific Knowledge Card Metrics",
        [
            ("• Card Utilization Rate (%): ", "% of eligible turns using Knowledge Cards", "#E65100"),
            ("• Policy & Rule Adherence (%): ", "Compliance on visa, passport & promo caps", "#E65100"),
            ("• Exemplar Leakage Rate (0%): ", "Zero hallucinated cities/prices from exemplars", "#E65100"),
            ("• Factual Slot Coverage F1: ", "Precision & recall of active user constraints", "#E65100"),
        ],
        bg_hex="#FFF3E0", border_hex="#E65100", font_size=7.4,
    )

    add_connector(s2, 3.28, 4.00, 3.00, 4.00, "#5E35B1")
    add_connector(s2, 5.88, 4.00, 6.15, 4.00, "#E65100")

    # =========================================================================
    # BOTTOM-LEFT BAND: CONVERSATION DB, AUDIT/QC BOT & HITL METRICS
    # =========================================================================
    add_zone_box(
        s2, 0.20, 5.22, 8.75, 2.08,
        "Post-Conversation Storage, Audit/QC Bot Scoring & Continuous HITL Refinement — Evaluation & Loop Metrics",
        bg_hex="#E8F5E9", border_hex="#2E7D32",
    )

    add_card(
        s2, 0.35, 5.50, 1.92, 1.68,
        "Conversation DB Telemetry",
        [
            ("• Logging Completeness: ", "100% turn & timestamp capture", "#455A64"),
            ("• Milestone Audit Trail: ", "Verified Lead & Quote flags", "#455A64"),
            ("• Slot State Ledger: ", "Stated vs. asked slot history", "#455A64"),
        ],
        bg_hex="#ECEFF1", border_hex="#455A64", shape_type=MSO_SHAPE.CAN, font_size=7.3,
    )

    add_card(
        s2, 2.45, 5.50, 2.20, 1.68,
        "Turn Economy & Quality Boundary\n(Controllable AI Outcome Ceiling)",
        [
            ("1. Chatbot KPI: ", "Interactions to Lead", "#0277BD"),
            ("2. Agent-Assist KPI: ", "Interactions to Quote", "#00695C"),
            ("3. Redundant Elicitation (RER): ", "% re-asked slots (Target = 0.0%)", "#0277BD"),
            ("4. First-Contact Resolution: ", "% reaching Lead/Quote in 1 session", "#0277BD"),
        ],
        bg_hex="#B3E5FC", border_hex="#0277BD", font_size=7.4,
    )

    add_card(
        s2, 4.82, 5.50, 2.15, 1.68,
        "Audit / QC Bot Scoring Metrics",
        [
            ("• Composite QC Score (0–100): ", "Turn economy + style + policy compliance", "#2E7D32"),
            ("• QC–Human Agreement (κ): ", "Inter-rater reliability with QA experts", "#2E7D32"),
            ("• High-Friction Flag Rate: ", "% chats exceeding interaction budget", "#2E7D32"),
            ("• Missing Scenario Alerts: ", "New unmapped customer patterns found", "#2E7D32"),
        ],
        bg_hex="#C8E6C9", border_hex="#2E7D32", font_size=7.4,
    )

    add_card(
        s2, 7.14, 5.50, 1.68, 1.68,
        "HITL Expert Loop Metrics",
        [
            ("• Golden Curation Rate: ", "# Golden Dialogues refined/added", "#1B5E20"),
            ("• Card Update Velocity: ", "Turnaround time for new Cards", "#1B5E20"),
            ("• Post-HITL Turn Lift: ", "Δ drop in Interactions to Quote", "#1B5E20"),
        ],
        bg_hex="#FFFFFF", border_hex="#1B5E20", font_size=7.4,
    )

    add_connector(s2, 2.27, 6.34, 2.45, 6.34, "#455A64")
    add_connector(s2, 4.65, 6.34, 4.82, 6.34, "#0277BD")
    add_connector(s2, 6.97, 6.34, 7.14, 6.34, "#2E7D32")

    # =========================================================================
    # VERTICAL METRIC FLOWS BETWEEN LEFT BANDS (aligned with Slide 1)
    # =========================================================================
    add_connector(
        s2, 2.10, 2.51, 2.10, 3.28, "#5E35B1", both_ends=True,
        label="Pattern Match & Pacing Telemetry", label_x=1.25, label_y=2.68, label_w=1.85, label_h=0.24,
        label_bg="#EDE7F6", label_border="#5E35B1",
    )
    add_connector(
        s2, 4.55, 2.51, 4.55, 3.28, "#F57F17", both_ends=True,
        label="Golden Retrieval Hit-Rate", label_x=3.72, label_y=2.68, label_w=1.65, label_h=0.24,
        label_bg="#FFF8E1", label_border="#F57F17",
    )
    add_connector(
        s2, 7.50, 2.51, 7.50, 3.28, "#E65100", both_ends=True,
        label="Knowledge Card Usage & Compliance", label_x=6.52, label_y=2.68, label_w=1.95, label_h=0.24,
        label_bg="#FFF3E0", label_border="#E65100",
    )

    add_connector(
        s2, 0.43, 2.51, 0.43, 5.50, "#455A64", width_pt=2.0,
        label="Interaction & Milestone Logs", label_x=0.25, label_y=4.90, label_w=1.65, label_h=0.24,
        label_bg="#ECEFF1", label_border="#455A64",
    )

    add_connector(
        s2, 7.95, 5.50, 7.95, 4.73, "#1B5E20", width_pt=2.2,
        label="QC Insights Drive New Golden Scenarios & Cards", label_x=6.15, label_y=4.90, label_w=2.55, label_h=0.25,
        label_bg="#C8E6C9", label_border="#1B5E20",
    )

    # =========================================================================
    # CENTER ATTRIBUTION FIREWALL + RIGHT COMMERCIAL CONVERSION ZONE
    # (Matching Slide 1's exact right-side alignment: x = 9.52 line, x = 10.18 zone)
    # =========================================================================
    fw_line = s2.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT,
        Inches(9.52), Inches(0.82), Inches(9.52), Inches(7.28),
    )
    fw_line.line.color.rgb = rgb("#C62828")
    fw_line.line.width = Pt(2.5)
    set_line_dash(fw_line, "dash")

    # Two Firewall Badges along the vertical divider (matching Slide 1 positions)
    b1 = s2.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.05), Inches(2.15), Inches(0.95), Inches(0.82),
    )
    b1.adjustments[0] = 0.12
    b1.fill.solid()
    b1.fill.fore_color.rgb = rgb("#FFEBEE")
    b1.line.color.rgb = rgb("#C62828")
    b1.line.width = Pt(1.5)
    tf_b1 = b1.text_frame
    tf_b1.word_wrap = True
    tf_b1.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_b1 = tf_b1.paragraphs[0]
    p_b1.alignment = PP_ALIGN.CENTER
    r_b1 = p_b1.add_run()
    r_b1.text = "✖ NO\nDIRECT\nCORRELATION"
    r_b1.font.name = "Calibri"
    r_b1.font.size = Pt(7.8)
    r_b1.font.bold = True
    r_b1.font.color.rgb = rgb("#C62828")

    b2 = s2.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.05), Inches(4.75), Inches(0.95), Inches(0.88),
    )
    b2.adjustments[0] = 0.12
    b2.fill.solid()
    b2.fill.fore_color.rgb = rgb("#FFF3E0")
    b2.line.color.rgb = rgb("#E65100")
    b2.line.width = Pt(1.5)
    tf_b2 = b2.text_frame
    tf_b2.word_wrap = True
    tf_b2.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_b2 = tf_b2.paragraphs[0]
    p_b2.alignment = PP_ALIGN.CENTER
    r_b2 = p_b2.add_run()
    r_b2.text = "⚠ FORCING\nLINK =\nSYSTEM NOISE"
    r_b2.font.name = "Calibri"
    r_b2.font.size = Pt(7.6)
    r_b2.font.bold = True
    r_b2.font.color.rgb = rgb("#B71C1C")

    # Right Zone Box (pos=(10.18, 0.78), size=(2.95x6.52) matching Slide 1!)
    add_zone_box(
        s2, 10.18, 0.78, 2.95, 6.52,
        "Post-Quote Commercial Conversion Zone\n(Excluded from Conversational AI Metrics)",
        bg_hex="#FFEBEE", border_hex="#C62828", dashed=True,
    )

    add_card(
        s2, 10.30, 1.32, 2.71, 1.48,
        "Converted Booking Metrics\n(NOT Used to Score Bots or Agents!)",
        [
            ("• Paid Booking Conversion (%): ", "% of quotes that become paid orders", "#B71C1C"),
            ("• Net Booking Revenue ($): ", "Checkout payment volume", "#B71C1C"),
            ("• Post-Quote Cancellation (%): ", "Trips cancelled after quote", "#B71C1C"),
            ("✖ Excluded from AI Loop: ", "Governed by exogenous factors below", "#C62828"),
        ],
        bg_hex="#EF9A9A", border_hex="#B71C1C", font_size=7.4,
    )

    add_card(
        s2, 10.30, 2.95, 2.71, 2.02,
        "Why Correlation Cannot Be Established\n(Real-World Exogenous Confounders)",
        [
            ("• Case A (Great Chat, 0 Conversion): ", "Agent delivers a flawless quote in 4 interactions (QC = 98%), but customer gets a one-off competitor coupon or has a medical/family emergency.", "#C62828"),
            ("• Case B (Poor Chat, 100% Conversion): ", "Bot takes 14 repetitive interactions (QC = 40%), yet customer still books due to an urgent monopoly flight route.", "#C62828"),
            ("→ Result: ", "Statistically orthogonal (r ≈ 0) to chat quality!", "#B71C1C"),
        ],
        bg_hex="#FFCDD2", border_hex="#C62828", font_size=7.3, dashed=True,
    )

    add_card(
        s2, 10.30, 5.12, 2.71, 2.05,
        "Consequence of Forcing Correlation:\nSevere Noise in the AI / HITL Loop",
        [
            ("1. Corrupts Golden Repository: ", "Penalizes & deletes high-performing Golden Dialogues whenever customers cancel for personal emergencies.", "#B71C1C"),
            ("2. Misguides Agent Coaching: ", "Blames agents for competitor price wars instead of coaching actual communication gaps.", "#B71C1C"),
            ("3. Design Principle: ", "Track & optimize metrics strictly up to Turn Economy (Interactions to Lead / Quote); keep Conversion separate!", "#1B5E20"),
        ],
        bg_hex="#FFF3E0", border_hex="#E65100", title_hex="#B71C1C", font_size=7.3,
    )

    prs.save(PPTX_PATH)
    print(f"Successfully updated Slide 2 (Slide 1 untouched) in: {PPTX_PATH}")


if __name__ == "__main__":
    build_slide2()

