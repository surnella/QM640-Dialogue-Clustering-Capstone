"""
Generate a 100% native, movable, and editable PowerPoint slide deck for the
Conversational AI & Agent-Assist Quality Improvement Loop:
  final/Conversational_Quality_Turn_Economy_Editable.pptx

Layout matches the user's exact specification:
  - Left/Main Vertical Stack (3 Stacked Blocks):
      * Top:    Block 2 — Live Customer Interaction Channels (Starts Here: Customer, Chatbot, Human Agent, Agent Assist Bot)
      * Middle: Block 1 — Reference Knowledge & Human-Like Personalization Layer (User Behavioral Patterns, Golden Conversations, Agent-Specific Knowledge Cards)
      * Bottom: Block 3 — Conversation DB, Audit/QC Bot Scoring & Continuous HITL Analysis (with upward feedback arrows into Block 1)
  - Top-Right Corner:
      * Block 4 — Post-Quote Commercial Conversion Zone (Exogenous Factors & Paid Conversion), separated by the Attribution Firewall.
"""

import os
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PPTX = os.path.join(ROOT, "final", "Conversational_Quality_Turn_Economy_Editable.pptx")
PNG_PATH = os.path.join(ROOT, "final", "conversational_quality_turn_economy_loop.png")


def rgb(hex_str):
    h = hex_str.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def set_line_dash(shape, dash="dash"):
    ln = shape.line._get_or_add_ln()
    prstDash = OxmlElement("a:prstDash")
    prstDash.set("val", dash)
    ln.append(prstDash)


def add_arrow_head(line_Or_connector, head_end=True, tail_end=False):
    ln = line_Or_connector.line._get_or_add_ln()
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
    tf.margin_top = Inches(0.05)
    tf.margin_right = Inches(0.10)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    r.text = title
    r.font.name = "Calibri"
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.color.rgb = rgb(border_hex)
    return box


def add_card(
    slide, left, top, width, height, title, bullets,
    bg_hex="#FFFFFF", border_hex="#1565C0", title_hex=None,
    shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, font_size=8.5, dashed=False,
):
    sh = slide.shapes.add_shape(
        shape_type, Inches(left), Inches(top), Inches(width), Inches(height),
    )
    if shape_type == MSO_SHAPE.ROUNDED_RECTANGLE:
        sh.adjustments[0] = 0.04
    sh.fill.solid()
    sh.fill.fore_color.rgb = rgb(bg_hex)
    sh.line.color.rgb = rgb(border_hex)
    sh.line.width = Pt(1.5)
    if dashed:
        set_line_dash(sh, "dash")

    tf = sh.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Inches(0.08)
    tf.margin_right = Inches(0.08)
    tf.margin_top = Inches(0.06)
    tf.margin_bottom = Inches(0.05)

    p0 = tf.paragraphs[0]
    p0.alignment = PP_ALIGN.LEFT
    p0.space_after = Pt(2)
    r0 = p0.add_run()
    r0.text = title
    r0.font.name = "Calibri"
    r0.font.size = Pt(font_size + 1.0)
    r0.font.bold = True
    r0.font.color.rgb = rgb(title_hex or border_hex)

    for b in bullets:
        p = tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(1.2)
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
    label_w=1.55, label_h=0.32, label_bg="#FFFFFF", label_border=None,
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
        r.font.size = Pt(7.5)
        r.font.bold = True
        r.font.color.rgb = rgb(color_hex)
    return conn


def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: 100% NATIVE EDITABLE ARCHITECTURE & CONTINUOUS LOOP DIAGRAM
    # =========================================================================
    s1 = prs.slides.add_slide(blank)

    # Top Title Banner
    hdr = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.68))
    hdr.fill.solid()
    hdr.fill.fore_color.rgb = rgb("#1B365D")
    hdr.line.fill.background()
    tf = hdr.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.25)
    p = tf.paragraphs[0]
    r1 = p.add_run()
    r1.text = "End-to-End Conversational AI & Agent-Assist Quality Improvement Loop (Editable Diagram)\n"
    r1.font.name = "Calibri"
    r1.font.size = Pt(15)
    r1.font.bold = True
    r1.font.color.rgb = rgb("#FFFFFF")
    r2 = p.add_run()
    r2.text = "Vertical Stack:  [2] Live Customer/Agent Channels (Start)  →  [1] Reference Knowledge & Behavioral Patterns  →  [3] DB, Audit/QC Bot & HITL   |   Top-Right: [4] Exogenous Conversion Firewall"
    r2.font.name = "Calibri"
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = rgb("#B3E5FC")

    # -------------------------------------------------------------------------
    # BLOCK 2 (TOP-LEFT): LIVE CUSTOMER INTERACTION CHANNELS (STARTS HERE)
    # -------------------------------------------------------------------------
    add_zone_box(
        s1, 0.20, 0.78, 8.75, 2.05,
        "2. Live Customer Interaction Channels (Conversations Start Here: Customer, Chatbot & Human Agent + Assist Bot)",
        bg_hex="#F0F4F8", border_hex="#1565C0",
    )

    add_card(
        s1, 0.32, 1.08, 1.85, 1.02,
        "Customer / Traveler",
        [
            "• Initiates inquiry via self-service chat or human sales agent",
            "• Expresses trip preferences, constraints & budget",
        ],
        bg_hex="#FFFFFF", border_hex="#1B365D", font_size=8.0,
    )

    add_card(
        s1, 0.32, 2.15, 3.85, 0.60,
        "Definition: 1 Interaction = 1 Customer Turn + 1 Bot / Agent Turn",
        [
            ("• Chatbot KPI: ", "Interactions to Lead  |  ", "#1565C0"),
            ("• Agent-Assist KPI: ", "Interactions to Quote (Quotation)", "#00695C"),
        ],
        bg_hex="#FFF9C4", border_hex="#F57F17", title_hex="#E65100", font_size=7.8,
    )

    add_card(
        s1, 2.48, 1.06, 2.20, 1.04,
        "Autonomous Chatbot (Self-Service)",
        [
            "• Matches User Behavioral Pattern",
            "• Uses Golden Exemplars & Cards",
            "• Captures intent without re-asking",
            ("• KPI: ", "Interactions to Lead", "#1565C0"),
        ],
        bg_hex="#E3F2FD", border_hex="#1565C0", font_size=8.0,
    )

    add_card(
        s1, 4.95, 1.06, 1.65, 1.04,
        "Human Sales Agent",
        [
            "• Handles consultative multi-option dialogs",
            "• Guided in real time by Agent Assist Bot",
        ],
        bg_hex="#FFFFFF", border_hex="#00695C", font_size=8.0,
    )

    add_card(
        s1, 6.82, 1.06, 2.02, 1.68,
        "Agent Assist Co-Pilot Bot",
        [
            "• Tracks stated customer constraints & behavioral style",
            "• Surfaces Agent-Specific Knowledge Cards in real time",
            "• Drafts side-by-side quotes & trade-off responses",
            ("• KPI: ", "Interactions to Quote", "#00695C"),
        ],
        bg_hex="#E0F2F1", border_hex="#00695C", font_size=8.0,
    )

    # Arrows inside Block 2
    add_connector(s1, 2.17, 1.48, 2.48, 1.48, "#1565C0", both_ends=True)
    add_connector(s1, 2.17, 1.82, 4.95, 1.82, "#00695C", both_ends=True,
                  label="Consultative Chat", label_x=3.35, label_y=2.22, label_w=1.25, label_h=0.24, label_bg="#E0F2F1")
    add_connector(s1, 6.60, 1.52, 6.82, 1.52, "#00695C", both_ends=True)

    # -------------------------------------------------------------------------
    # BLOCK 1 (MIDDLE-LEFT): REFERENCE KNOWLEDGE LAYER (BETWEEN 2 AND 3)
    # -------------------------------------------------------------------------
    add_zone_box(
        s1, 0.20, 3.05, 8.75, 1.92,
        "1. Reference Knowledge & Human-Like Personalization Layer (Accessed by Block 2 at Runtime & Updated by Block 3)",
        bg_hex="#F3E5F5", border_hex="#6A1B9A",
    )

    add_card(
        s1, 0.35, 3.38, 2.65, 1.46,
        "User Behavioral Pattern Engine",
        [
            "• Identifies customer style early (e.g., Decisive, Explorer, Strict Negotiator)",
            "• Calibrates human-like empathy, tone & pacing to match customer",
            "• Prevents repetitive slot re-asking",
        ],
        bg_hex="#EDE7F6", border_hex="#5E35B1", font_size=8.2,
    )

    add_card(
        s1, 3.28, 3.38, 2.60, 1.46,
        "Golden Conversations Repository",
        [
            "• Curated benchmark human dialogues",
            "• Proven multi-turn discovery & negotiation flows",
            "• Continuously enriched with new edge-case scenarios by HITL",
        ],
        bg_hex="#FFF8E1", border_hex="#F57F17", title_hex="#E65100",
        shape_type=MSO_SHAPE.CAN, font_size=8.0,
    )

    add_card(
        s1, 6.15, 3.38, 2.68, 1.46,
        "Agent-Specific Knowledge Cards",
        [
            "• Created from Golden Conversations",
            "• Persona-specific response playbooks",
            "• Side-by-side quote comparison & trade-off scripts",
            "• Verified slot ledger & policy guardrails",
        ],
        bg_hex="#FFF3E0", border_hex="#E65100", font_size=8.2,
    )

    # Arrows inside Block 1
    add_connector(s1, 3.28, 4.10, 3.00, 4.10, "#5E35B1")
    add_connector(s1, 5.88, 4.10, 6.15, 4.10, "#E65100")

    # -------------------------------------------------------------------------
    # BLOCK 3 (BOTTOM-LEFT): CONVERSATION DB, AUDIT/QC BOT & HITL ANALYSIS
    # -------------------------------------------------------------------------
    add_zone_box(
        s1, 0.20, 5.20, 8.75, 2.12,
        "3. Post-Conversation Storage, Audit/QC Bot Scoring & Continuous Human-in-the-Loop (HITL) Refinement",
        bg_hex="#E8F5E9", border_hex="#2E7D32",
    )

    add_card(
        s1, 0.35, 5.52, 1.95, 1.65,
        "Conversation & Interaction DB",
        [
            "• Deposits completed Chatbot & Agent transcripts",
            "• Logs interaction counts, slot ledgers & Knowledge Cards used",
        ],
        bg_hex="#ECEFF1", border_hex="#455A64", shape_type=MSO_SHAPE.CAN, font_size=7.9,
    )

    add_card(
        s1, 2.52, 5.52, 2.10, 1.65,
        "Measurable Chat Outcomes (End of AI Scope)",
        [
            ("• Chatbot: ", "Interactions to Lead", "#0277BD"),
            ("• Agent Assist: ", "Interactions to Quote", "#00695C"),
            "• Zero redundant elicitation",
            "• Human-like style & card adherence",
        ],
        bg_hex="#B3E5FC", border_hex="#0277BD", font_size=8.0,
    )

    add_card(
        s1, 4.84, 5.52, 2.15, 1.65,
        "Audit / QC Bot (Scoring Engine)",
        [
            "• Scores Turn Economy (Interactions to Lead / Quote)",
            "• Audits human-like tone, pacing & Knowledge Card adherence",
            "• Flags stalled chats & missing Golden Conversation scenarios",
        ],
        bg_hex="#C8E6C9", border_hex="#2E7D32", font_size=8.0,
    )

    add_card(
        s1, 7.20, 5.52, 1.65, 1.65,
        "Human-in-the-Loop (HITL) Expert",
        [
            "• Reviews Audit/QC Bot scores & insights",
            "• Modifies Golden Conversations",
            "• Creates new scenario Cards for Agents/Bots",
        ],
        bg_hex="#FFFFFF", border_hex="#1B5E20", font_size=8.0,
    )

    # Arrows inside Block 3
    add_connector(s1, 2.30, 6.35, 2.52, 6.35, "#455A64")
    add_connector(s1, 4.62, 6.35, 4.84, 6.35, "#0277BD")
    add_connector(s1, 6.99, 6.35, 7.20, 6.35, "#2E7D32")

    # -------------------------------------------------------------------------
    # VERTICAL CONNECTIONS ACROSS BLOCKS 2 <-> 1 <-> 3
    # -------------------------------------------------------------------------
    # Block 2 <-> Block 1 (Runtime access to Reference Knowledge)
    add_connector(
        s1, 3.10, 2.10, 2.10, 3.38, "#5E35B1", both_ends=True,
        label="Accesses Behavioral Pattern", label_x=1.85, label_y=2.80, label_w=1.65, label_h=0.25,
        label_bg="#EDE7F6", label_border="#5E35B1",
    )
    add_connector(
        s1, 4.20, 2.10, 4.45, 3.38, "#F57F17", both_ends=True,
        label="Retrieves Golden Exemplars", label_x=3.65, label_y=2.80, label_w=1.65, label_h=0.25,
        label_bg="#FFF8E1", label_border="#F57F17",
    )
    add_connector(
        s1, 7.60, 2.74, 7.50, 3.38, "#E65100", both_ends=True,
        label="Fetches Agent Knowledge Cards", label_x=6.60, label_y=2.82, label_w=1.85, label_h=0.25,
        label_bg="#FFF3E0", label_border="#E65100",
    )

    # Block 2 -> Block 3 (Completed transcripts deposited into Conversation DB)
    add_connector(
        s1, 1.25, 2.75, 1.25, 5.52, "#455A64", width_pt=2.0,
        label="Deposits Completed Chats\n(Interactions to Lead / Quote)", label_x=0.32, label_y=4.88, label_w=1.85, label_h=0.34,
        label_bg="#ECEFF1", label_border="#455A64",
    )

    # Block 3 -> Block 1 (HITL Expert updates Golden Conversations & Knowledge Cards)
    add_connector(
        s1, 7.95, 5.52, 7.65, 4.84, "#1B5E20", width_pt=2.2,
        label="HITL Refines Golden Dialogues\n& Creates New Scenario Cards", label_x=6.65, label_y=4.92, label_w=2.15, label_h=0.34,
        label_bg="#C8E6C9", label_border="#1B5E20",
    )
    add_connector(
        s1, 7.45, 5.52, 5.15, 4.84, "#1B5E20", width_pt=1.8,
    )

    # -------------------------------------------------------------------------
    # BLOCK 4 (TOP-RIGHT CORNER): EXOGENOUS CONVERSION ZONE (NO DIRECT LINK)
    # -------------------------------------------------------------------------
    add_zone_box(
        s1, 9.35, 0.78, 3.78, 6.54,
        "4. Post-Quote Commercial Conversion Zone\n(Exogenous Factors — Kept Separate from Chat Metrics)",
        bg_hex="#FFEBEE", border_hex="#C62828", dashed=True,
    )

    add_card(
        s1, 9.52, 1.38, 3.44, 1.95,
        "Exogenous Market & Personal Factors\n(Uncontrollable by Chatbot or Human Agent)",
        [
            ("• Competitor One-Off Deals: ", "Last-minute flash coupon or promo deal from rival OTA/startup", "#C62828"),
            ("• Personal / Emergency Cancellations: ", "Sudden medical/family emergency, visa delay, or leave cancellation", "#C62828"),
            ("• Off-Platform Alternatives: ", "Staying with friends/family or booking standalone tickets directly", "#C62828"),
        ],
        bg_hex="#FFCDD2", border_hex="#C62828", font_size=8.2, dashed=True,
    )

    add_card(
        s1, 9.52, 3.62, 3.44, 1.15,
        "Final Business Conversion (Paid Booking)",
        [
            "• Customer completes checkout payment",
            "• Heavily confounded by exogenous price & personal emergencies after Lead / Quote delivery",
        ],
        bg_hex="#EF9A9A", border_hex="#B71C1C", font_size=8.3,
    )

    add_connector(
        s1, 11.24, 3.33, 11.24, 3.62, "#B71C1C", width_pt=2.0,
    )

    add_card(
        s1, 9.52, 4.92, 3.44, 2.25,
        "CRITICAL ATTRIBUTION FIREWALL\n(Why Conversion Must Be Kept Separate)",
        [
            ("1. No Automatic Conversion Link: ", "Improving QC Bot scores on Interactions to Quote / Lead does NOT automatically drive paid conversions.", "#B71C1C"),
            ("2. Avoids System Noise: ", "Forcing a correlation between Chat Metrics and Conversion injects severe exogenous noise (e.g., penalizing a great 4-interaction quote cancelled due to an emergency).", "#B71C1C"),
            ("3. True Purpose of QC Bot: ", "Give clean feedback to HITL on missing Golden Scenarios & Agent coaching.", "#1B5E20"),
        ],
        bg_hex="#FFF3E0", border_hex="#E65100", title_hex="#B71C1C", font_size=7.9,
    )

    # Vertical Attribution Firewall Divider Line between Left Stack and Block 4
    fw_line = s1.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT,
        Inches(9.15), Inches(0.82), Inches(9.15), Inches(7.28),
    )
    fw_line.line.color.rgb = rgb("#C62828")
    fw_line.line.width = Pt(2.5)
    set_line_dash(fw_line, "dash")

    # Dashed Warning Connector showing NO direct correlation between Block 3/2 and Block 4
    add_connector(
        s1, 8.84, 1.95, 9.52, 4.10, "#C62828", width_pt=1.8, dashed=True,
        label="✖ NO DIRECT CORRELATION\n(Firewall Prevents Exogenous Noise)",
        label_x=8.22, label_y=2.32, label_w=1.88, label_h=0.38,
        label_bg="#FFEBEE", label_border="#C62828",
    )

    # =========================================================================
    # SLIDE 2: HIGH-RESOLUTION RENDERED PLANTUML DIAGRAM FOR REFERENCE
    # =========================================================================
    if os.path.exists(PNG_PATH):
        s2 = prs.slides.add_slide(blank)
        hdr2 = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.55))
        hdr2.fill.solid()
        hdr2.fill.fore_color.rgb = rgb("#1B365D")
        hdr2.line.fill.background()
        tf2 = hdr2.text_frame
        tf2.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf2.margin_left = Inches(0.25)
        p2 = tf2.paragraphs[0]
        r2 = p2.add_run()
        r2.text = "Rendered PlantUML Diagram Reference (conversational_quality_turn_economy_loop.puml)"
        r2.font.name = "Calibri"
        r2.font.size = Pt(14)
        r2.font.bold = True
        r2.font.color.rgb = rgb("#FFFFFF")

        s2.shapes.add_picture(PNG_PATH, Inches(0.20), Inches(0.65), width=Inches(12.93))

    os.makedirs(os.path.dirname(OUT_PPTX), exist_ok=True)
    prs.save(OUT_PPTX)
    print(f"Saved editable PowerPoint deck: {OUT_PPTX}")


if __name__ == "__main__":
    build_deck()

