"""
Professional Widescreen (16:9) PowerPoint Builder for QM640 Capstone Defense.
Provides reusable layout primitives:
  - Title slide & Section divider slides
  - Content header banner with Module badge, Title, Subtitle, and Slide X / N counter
  - Multi-column cards, callout boxes, formula banners, and comparison panels
  - Styled native PowerPoint tables with rich cell formatting
  - High-resolution figure embedding with aspect-ratio-preserving bounding box fit
  - Comprehensive speaker notes attached to every slide for defense preparation
"""

import os
import re
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

# Palette: Academic Navy, Deep Teal, Slate, Warm Gold, Soft Backgrounds
NAVY = RGBColor(15, 37, 68)        # #0F2544 - Primary header / dark accent
TEAL = RGBColor(13, 110, 110)      # #0D6E6E - Secondary accent
BLUE = RGBColor(28, 78, 128)       # #1C4E80 - Card headers
GOLD = RGBColor(197, 139, 24)      # #C58B18 - Highlight / badge
CORAL = RGBColor(184, 51, 42)      # #B8332A - Warning / negative baseline
GREEN = RGBColor(27, 115, 64)      # #1B7340 - Positive outcome / reject H0
DARK = RGBColor(30, 36, 48)        # #1E2430 - Primary body text
MUTED = RGBColor(90, 101, 119)     # #5A6577 - Subtitle / caption text
WHITE = RGBColor(255, 255, 255)
BG_LIGHT = RGBColor(246, 248, 252) # #F6F8FC - Slide canvas background
CARD_BG = RGBColor(255, 255, 255)  # White card surface
CARD_ALT = RGBColor(238, 243, 250) # Soft blue-gray card surface
CALLOUT_BG = RGBColor(254, 248, 232) # Soft warm gold callout background
GREEN_BG = RGBColor(235, 247, 240) # Soft green callout background
RED_BG = RGBColor(253, 238, 236)   # Soft red callout background
BORDER_GRAY = RGBColor(208, 216, 228)
TBL_HEADER = RGBColor(20, 50, 92)
TBL_EVEN = RGBColor(242, 246, 252)
TBL_ODD = RGBColor(255, 255, 255)

FONT_HEAD = "Calibri"
FONT_BODY = "Calibri"


def _add_formatted_runs(p, text, font_size=13, color=DARK, bold=False, italic=False, font_name=FONT_BODY):
    """
    Parse lightweight inline tags `<b>...</b>`, `<i>...</i>`, `<sub>...</sub>`, and `<sup>...</sup>`
    into native PowerPoint runs (including DrawingML subscript/superscript baseline offsets).
    """
    tokens = re.split(r"(</?(?:b|i|sub|sup)>)", str(text))
    b_state = bold
    i_state = italic
    sub_state = False
    sup_state = False
    for tok in tokens:
        if not tok:
            continue
        if tok == "<b>":
            b_state = True
            continue
        elif tok == "</b>":
            b_state = bold
            continue
        elif tok == "<i>":
            i_state = True
            continue
        elif tok == "</i>":
            i_state = italic
            continue
        elif tok == "<sub>":
            sub_state = True
            continue
        elif tok == "</sub>":
            sub_state = False
            continue
        elif tok == "<sup>":
            sup_state = True
            continue
        elif tok == "</sup>":
            sup_state = False
            continue
        run = p.add_run()
        run.text = tok
        run.font.name = font_name
        run.font.size = Pt(font_size)
        run.font.bold = b_state
        run.font.italic = i_state
        run.font.color.rgb = color
        if sub_state:
            run._r.get_or_add_rPr().set("baseline", "-25000")
        elif sup_state:
            run._r.get_or_add_rPr().set("baseline", "30000")


class DefenseDeck:
    def __init__(self, total_slides_est=42):
        self.prs = Presentation()
        self.prs.slide_width = Inches(13.333)
        self.prs.slide_height = Inches(7.5)
        self.blank_layout = self.prs.slide_layouts[6]
        self.slide_num = 0
        self.total_slides_est = total_slides_est

    def _new_slide(self, bg_color=BG_LIGHT, notes=""):
        self.slide_num += 1
        s = self.prs.slides.add_slide(self.blank_layout)
        bg = s.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5)
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = bg_color
        bg.line.fill.background()
        if notes:
            notes_slide = s.notes_slide
            notes_slide.notes_text_frame.text = notes.strip()
        return s

    def add_title_slide(self, title, subtitle, author_lines, badge_text="QM640 CAPSTONE DEFENSE PRESENTATION", notes=""):
        s = self._new_slide(bg_color=NAVY, notes=notes)
        # Decorative accent bars
        bar1 = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.35), Inches(7.5))
        bar1.fill.solid()
        bar1.fill.fore_color.rgb = GOLD
        bar1.line.fill.background()

        bar2 = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.35), Inches(0), Inches(0.12), Inches(7.5))
        bar2.fill.solid()
        bar2.fill.fore_color.rgb = TEAL
        bar2.line.fill.background()

        # Badge pill
        badge = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.85), Inches(4.6), Inches(0.45))
        badge.fill.solid()
        badge.fill.fore_color.rgb = GOLD
        badge.line.fill.background()
        tf_b = badge.text_frame
        tf_b.word_wrap = True
        p_b = tf_b.paragraphs[0]
        p_b.alignment = PP_ALIGN.CENTER
        _add_formatted_runs(p_b, badge_text, font_size=12, color=NAVY, bold=True)

        # Title
        tb = s.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(11.4), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        _add_formatted_runs(p, title, font_size=34, color=WHITE, bold=True)

        # Subtitle
        tb_sub = s.shapes.add_textbox(Inches(1.0), Inches(3.65), Inches(11.4), Inches(1.1))
        tf_sub = tb_sub.text_frame
        tf_sub.word_wrap = True
        p_sub = tf_sub.paragraphs[0]
        _add_formatted_runs(p_sub, subtitle, font_size=17, color=RGBColor(210, 225, 245), italic=True)

        # Divider line
        line = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(4.85), Inches(11.3), Inches(0.03))
        line.fill.solid()
        line.fill.fore_color.rgb = GOLD
        line.line.fill.background()

        # Author & Metadata block
        tb_au = s.shapes.add_textbox(Inches(1.0), Inches(5.05), Inches(11.3), Inches(1.9))
        tf_au = tb_au.text_frame
        tf_au.word_wrap = True
        for i, line_txt in enumerate(author_lines):
            p_a = tf_au.paragraphs[0] if i == 0 else tf_au.add_paragraph()
            p_a.space_after = Pt(4)
            _add_formatted_runs(p_a, line_txt, font_size=14, color=WHITE)
        return s

    def content_slide(self, module_label, title, subtitle="", notes=""):
        s = self._new_slide(bg_color=BG_LIGHT, notes=notes)
        # Top header bar
        hdr = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.05))
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = NAVY
        hdr.line.fill.background()

        # Left gold stripe in header
        stripe = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.18), Inches(1.05))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = GOLD
        stripe.line.fill.background()

        # Module pill
        pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.35), Inches(0.12), Inches(3.3), Inches(0.26))
        pill.fill.solid()
        pill.fill.fore_color.rgb = TEAL
        pill.line.fill.background()
        tf_p = pill.text_frame
        tf_p.margin_left = tf_p.margin_right = Inches(0.06)
        tf_p.margin_top = tf_p.margin_bottom = Inches(0.01)
        p_p = tf_p.paragraphs[0]
        p_p.alignment = PP_ALIGN.CENTER
        _add_formatted_runs(p_p, module_label.upper(), font_size=9.5, color=WHITE, bold=True)

        # Slide number badge on top-right
        tb_num = s.shapes.add_textbox(Inches(11.6), Inches(0.1), Inches(1.5), Inches(0.3))
        p_num = tb_num.text_frame.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        _add_formatted_runs(p_num, f"Slide {self.slide_num}", font_size=10, color=RGBColor(190, 205, 225), bold=True)

        # Title
        tb_t = s.shapes.add_textbox(Inches(0.35), Inches(0.36), Inches(12.6), Inches(0.42))
        tf_t = tb_t.text_frame
        tf_t.word_wrap = True
        tf_t.margin_top = tf_t.margin_bottom = Inches(0)
        p_t = tf_t.paragraphs[0]
        _add_formatted_runs(p_t, title, font_size=20, color=WHITE, bold=True)

        # Optional subtitle strip below header
        if subtitle:
            sub_bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.05), Inches(13.333), Inches(0.34))
            sub_bar.fill.solid()
            sub_bar.fill.fore_color.rgb = RGBColor(230, 236, 245)
            sub_bar.line.fill.background()
            tb_s = s.shapes.add_textbox(Inches(0.35), Inches(1.07), Inches(12.6), Inches(0.3))
            tf_s = tb_s.text_frame
            tf_s.word_wrap = True
            tf_s.margin_top = tf_s.margin_bottom = Inches(0)
            p_s = tf_s.paragraphs[0]
            _add_formatted_runs(p_s, subtitle, font_size=11.5, color=NAVY, italic=True)

        # Footer bar
        ftr = s.shapes.add_textbox(Inches(0.35), Inches(7.22), Inches(12.6), Inches(0.24))
        p_f = ftr.text_frame.paragraphs[0]
        _add_formatted_runs(
            p_f,
            "Surnella Sandeep | QM640 Data Analytics Capstone | Cluster-Adaptive Prompting for Multi-Turn Travel Conversational Systems",
            font_size=8.5,
            color=MUTED,
        )
        return s

    def add_card(
        self,
        slide,
        left,
        top,
        width,
        height,
        title="",
        bullets=None,
        bg_color=CARD_BG,
        header_bg=BLUE,
        border_color=BORDER_GRAY,
        font_size=12,
        title_size=13,
        bullet_spacing=4,
    ):
        # Card body
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height)
        )
        card.adjustments[0] = 0.02
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1)
        else:
            card.line.fill.background()

        content_top = top + 0.08
        if title:
            hdr_h = 0.36
            hdr = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(hdr_h)
            )
            hdr.adjustments[0] = 0.02
            hdr.fill.solid()
            hdr.fill.fore_color.rgb = header_bg
            hdr.line.fill.background()
            tf_h = hdr.text_frame
            tf_h.word_wrap = True
            tf_h.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf_h.margin_left = Inches(0.12)
            p_h = tf_h.paragraphs[0]
            _add_formatted_runs(p_h, title, font_size=title_size, color=WHITE, bold=True)
            content_top = top + hdr_h + 0.06

        if bullets:
            tb = slide.shapes.add_textbox(
                Inches(left + 0.1),
                Inches(content_top),
                Inches(width - 0.2),
                Inches(max(0.2, height - (content_top - top) - 0.06)),
            )
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_right = Inches(0.04)
            tf.margin_top = tf.margin_bottom = Inches(0.02)
            for i, b in enumerate(bullets):
                p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                p.space_after = Pt(bullet_spacing)
                if isinstance(b, tuple):
                    # (indent_level, text)
                    lvl, txt = b
                    prefix = "    ▪ " if lvl > 0 else "• "
                    _add_formatted_runs(p, prefix + txt, font_size=max(10, font_size - lvl), color=DARK)
                else:
                    prefix = "" if str(b).startswith(("•", "▪", "1.", "2.", "3.", "4.", "5.", "→", "✓", "✗")) else "• "
                    _add_formatted_runs(p, prefix + str(b), font_size=font_size, color=DARK)
        return card

    def add_callout(
        self,
        slide,
        left,
        top,
        width,
        height,
        text,
        bg_color=CALLOUT_BG,
        border_color=GOLD,
        font_size=12,
    ):
        box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height)
        )
        box.adjustments[0] = 0.04
        box.fill.solid()
        box.fill.fore_color.rgb = bg_color
        box.line.color.rgb = border_color
        box.line.width = Pt(1.5)
        tf = box.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_right = Inches(0.14)
        tf.margin_top = tf.margin_bottom = Inches(0.06)
        p = tf.paragraphs[0]
        _add_formatted_runs(p, text, font_size=font_size, color=DARK)
        return box

    def add_table(
        self,
        slide,
        left,
        top,
        width,
        height,
        headers,
        rows,
        col_widths=None,
        font_size=10.5,
        header_size=11,
        align_left_cols=(0,),
        highlight_rows=(),
    ):
        n_rows = 1 + len(rows)
        n_cols = len(headers)
        shape = slide.shapes.add_table(n_rows, n_cols, Inches(left), Inches(top), Inches(width), Inches(height))
        tbl = shape.table
        if col_widths:
            total_w = sum(col_widths)
            for c_i, w in enumerate(col_widths):
                tbl.columns[c_i].width = Inches(width * (w / total_w))

        # Header
        for c_i, h_text in enumerate(headers):
            cell = tbl.cell(0, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = TBL_HEADER
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = cell.margin_right = Inches(0.06)
            cell.margin_top = cell.margin_bottom = Inches(0.03)
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if c_i in align_left_cols else PP_ALIGN.CENTER
            _add_formatted_runs(p, h_text, font_size=header_size, color=WHITE, bold=True)

        # Body rows
        for r_i, row in enumerate(rows):
            is_hi = r_i in highlight_rows
            bg = RGBColor(225, 243, 232) if is_hi else (TBL_EVEN if r_i % 2 == 1 else TBL_ODD)
            for c_i, val in enumerate(row):
                cell = tbl.cell(r_i + 1, c_i)
                cell.fill.solid()
                cell.fill.fore_color.rgb = bg
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                cell.margin_left = cell.margin_right = Inches(0.06)
                cell.margin_top = cell.margin_bottom = Inches(0.025)
                p = cell.text_frame.paragraphs[0]
                p.alignment = PP_ALIGN.LEFT if c_i in align_left_cols else PP_ALIGN.CENTER
                _add_formatted_runs(p, str(val), font_size=font_size, color=DARK, bold=is_hi)
        return tbl

    def add_figure(self, slide, image_path, left, top, max_width, max_height, caption="", border=True):
        if not os.path.exists(image_path):
            self.add_callout(slide, left, top, max_width, max_height, f"Missing image: {image_path}")
            return
        with Image.open(image_path) as im:
            w_px, h_px = im.size
        aspect = w_px / max(1, h_px)
        cap_h = 0.28 if caption else 0.0
        avail_h = max_height - cap_h

        # Fit inside (max_width, avail_h) preserving aspect ratio
        w_in = max_width
        h_in = w_in / aspect
        if h_in > avail_h:
            h_in = avail_h
            w_in = h_in * aspect

        x_in = left + (max_width - w_in) / 2.0
        y_in = top + (avail_h - h_in) / 2.0

        if border:
            frame = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(x_in - 0.04),
                Inches(y_in - 0.04),
                Inches(w_in + 0.08),
                Inches(h_in + 0.08),
            )
            frame.fill.solid()
            frame.fill.fore_color.rgb = WHITE
            frame.line.color.rgb = BORDER_GRAY
            frame.line.width = Pt(1)

        slide.shapes.add_picture(image_path, Inches(x_in), Inches(y_in), width=Inches(w_in), height=Inches(h_in))
        if caption:
            tb = slide.shapes.add_textbox(Inches(left), Inches(top + avail_h), Inches(max_width), Inches(cap_h))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            _add_formatted_runs(p, caption, font_size=9.5, color=MUTED, italic=True)

    def add_storyline_state_slide(
        self,
        module_label,
        title,
        subtitle,
        stages_data,
        handoff_arrows,
        bottom_callout,
        notes="",
    ):
        """
        Render the recurring 4-Stage Solution Approach (`Identify -> Personalize -> Govern -> Optimize`)
        using native Microsoft PowerPoint shapes:
          - Stage containers: MSO_SHAPE.ROUNDED_RECTANGLE
          - Candidate IVs / Paths / Conclusions inside each stage: MSO_SHAPE.ROUNDED_RECTANGLE (with rounded status badges)
            color-coded:
              * 'green': Winner carried forward to next stage
              * 'orange': Partial / requires verification or augmentation in next stage
              * 'red': Closed / dropped path (does not go to next stage)
              * 'blue' / 'pending': Conceptual or upcoming stage
          - Intra-stage & inter-stage connectors: MSO_SHAPE.DOWN_ARROW / MSO_SHAPE.RIGHT_ARROW with test labels.
        """
        s = self.content_slide(module_label, title, subtitle, notes=notes)

        ORANGE_BDR = RGBColor(210, 120, 15)
        ORANGE_BG = RGBColor(255, 244, 222)
        PENDING_BDR = RGBColor(120, 140, 170)
        PENDING_BG = RGBColor(238, 243, 250)

        # Top Legend Bar (y = 1.41, h = 0.28)
        legend_items = [
            (0.24, 3.05, CARD_ALT, NAVY, NAVY, "STAGE CONTAINER", "4 Solution Stages (Identify → Optimize)"),
            (3.37, 3.22, GREEN_BG, GREEN, GREEN, "✓ GREEN NODE", "Proven Winner → Carried to Next Stage"),
            (6.67, 3.38, ORANGE_BG, ORANGE_BDR, ORANGE_BDR, "! ORANGE NODE", "Needs Next-Stage Guard / Verification"),
            (10.13, 2.96, RED_BG, CORAL, CORAL, "✗ RED NODE", "Path Closed / Dropped"),
        ]
        for lx, lw, lbg, lhdr, lbdr, ltag, ldesc in legend_items:
            lbox = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(lx), Inches(1.41), Inches(lw), Inches(0.27))
            lbox.adjustments[0] = 0.15
            lbox.fill.solid()
            lbox.fill.fore_color.rgb = lbg
            lbox.line.color.rgb = lbdr
            lbox.line.width = Pt(1.1)

            lbadge = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(lx + 0.04), Inches(1.43), Inches(1.22), Inches(0.23))
            lbadge.adjustments[0] = 0.20
            lbadge.fill.solid()
            lbadge.fill.fore_color.rgb = lhdr
            lbadge.line.fill.background()
            p_lb = lbadge.text_frame.paragraphs[0]
            p_lb.alignment = PP_ALIGN.CENTER
            _add_formatted_runs(p_lb, ltag, font_size=6.8, color=WHITE, bold=True)

            ltb = s.shapes.add_textbox(Inches(lx + 1.30), Inches(1.42), Inches(lw - 1.34), Inches(0.25))
            ltb.text_frame.word_wrap = True
            ltb.text_frame.margin_left = ltb.text_frame.margin_top = Inches(0)
            p_ld = ltb.text_frame.paragraphs[0]
            _add_formatted_runs(p_ld, ldesc, font_size=7.2, color=DARK, bold=True)

        start_x = 0.24
        col_w = 2.92
        gap_w = 0.39
        stage_top = 1.73
        stage_h = 4.60

        status_palette = {
            "green": (GREEN_BG, GREEN, GREEN, "✓"),
            "orange": (ORANGE_BG, ORANGE_BDR, ORANGE_BDR, "!"),
            "red": (RED_BG, CORAL, CORAL, "✗"),
            "blue": (PENDING_BG, BLUE, BLUE, "●"),
            "pending": ( RGBColor(242, 245, 250), PENDING_BDR, PENDING_BDR, "○"),
        }

        for idx, st in enumerate(stages_data):
            x = start_x + idx * (col_w + gap_w)
            hdr_color = st.get("header_color", NAVY)
            border_color = st.get("border_color", hdr_color)
            bg_tint = st.get("bg_color", WHITE)

            # Outer Stage Rectangle
            rect = s.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(stage_top), Inches(col_w), Inches(stage_h)
            )
            rect.adjustments[0] = 0.02
            rect.fill.solid()
            rect.fill.fore_color.rgb = bg_tint
            rect.line.color.rgb = border_color
            rect.line.width = Pt(1.75)

            # Stage Header Bar
            hdr = s.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(stage_top), Inches(col_w), Inches(0.42)
            )
            hdr.adjustments[0] = 0.02
            hdr.fill.solid()
            hdr.fill.fore_color.rgb = hdr_color
            hdr.line.fill.background()
            tf_h = hdr.text_frame
            tf_h.word_wrap = True
            tf_h.margin_left = tf_h.margin_right = Inches(0.06)
            tf_h.margin_top = tf_h.margin_bottom = Inches(0.02)
            p_h1 = tf_h.paragraphs[0]
            p_h1.alignment = PP_ALIGN.CENTER
            _add_formatted_runs(p_h1, st["stage_title"], font_size=9.2, color=WHITE, bold=True)
            if st.get("stage_subtitle"):
                p_h2 = tf_h.add_paragraph()
                p_h2.alignment = PP_ALIGN.CENTER
                _add_formatted_runs(p_h2, st["stage_subtitle"], font_size=7.2, color=RGBColor(225, 238, 255), italic=True)

            # Input / Objective Strip
            in_box = s.shapes.add_shape(
                MSO_SHAPE.RECTANGLE, Inches(x + 0.07), Inches(stage_top + 0.45), Inches(col_w - 0.14), Inches(0.44)
            )
            in_box.fill.solid()
            in_box.fill.fore_color.rgb = CARD_ALT
            in_box.line.color.rgb = BORDER_GRAY
            in_box.line.width = Pt(0.8)
            tf_in = in_box.text_frame
            tf_in.word_wrap = True
            tf_in.margin_left = tf_in.margin_right = Inches(0.05)
            tf_in.margin_top = tf_in.margin_bottom = Inches(0.02)
            p_in = tf_in.paragraphs[0]
            _add_formatted_runs(p_in, st["input_text"], font_size=6.9, color=DARK)

            # 3 Rounded-Rectangle Nodes inside the Stage Container
            circles = st.get("circles", [])
            connectors = st.get("connectors", [])
            c_top_base = stage_top + 0.93
            c_h = 0.86
            conn_h = 0.17

            for c_i, c_info in enumerate(circles[:3]):
                cy = c_top_base + c_i * (c_h + conn_h)
                c_state = c_info.get("status", "blue")
                c_bg, c_bdr, c_badge_col, c_sym = status_palette.get(c_state, status_palette["blue"])

                # Rounded-Rectangle Shape representing the tested IV / candidate path
                rnode = s.shapes.add_shape(
                    MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x + 0.07), Inches(cy), Inches(col_w - 0.14), Inches(c_h)
                )
                rnode.adjustments[0] = 0.12
                rnode.fill.solid()
                rnode.fill.fore_color.rgb = c_bg
                rnode.line.color.rgb = c_bdr
                rnode.line.width = Pt(1.5)

                # Rounded-rectangle status badge on left side of the node
                s_badge = s.shapes.add_shape(
                    MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x + 0.13), Inches(cy + (c_h - 0.26) / 2.0), Inches(0.26), Inches(0.26)
                )
                s_badge.adjustments[0] = 0.22
                s_badge.fill.solid()
                s_badge.fill.fore_color.rgb = c_badge_col
                s_badge.line.color.rgb = WHITE
                s_badge.line.width = Pt(1.0)
                p_sc = s_badge.text_frame.paragraphs[0]
                p_sc.alignment = PP_ALIGN.CENTER
                _add_formatted_runs(p_sc, c_sym, font_size=8.5, color=WHITE, bold=True)

                # Text inside the rounded rectangle
                tb_c = s.shapes.add_textbox(
                    Inches(x + 0.43), Inches(cy + 0.03), Inches(col_w - 0.54), Inches(c_h - 0.06)
                )
                tf_c = tb_c.text_frame
                tf_c.word_wrap = True
                tf_c.vertical_anchor = MSO_ANCHOR.MIDDLE
                tf_c.margin_left = tf_c.margin_right = Inches(0.02)
                tf_c.margin_top = tf_c.margin_bottom = Inches(0.01)
                p_ct = tf_c.paragraphs[0]
                _add_formatted_runs(p_ct, c_info["title"], font_size=7.4, color=c_bdr, bold=True)
                p_cd = tf_c.add_paragraph()
                p_cd.space_before = Pt(1.0)
                _add_formatted_runs(p_cd, c_info["body"], font_size=6.7, color=DARK)

                # Intra-stage connector arrow to next circle
                if c_i < len(circles[:3]) - 1:
                    ay = cy + c_h + 0.01
                    arr = s.shapes.add_shape(
                        MSO_SHAPE.DOWN_ARROW, Inches(x + 0.42), Inches(ay), Inches(0.18), Inches(conn_h - 0.02)
                    )
                    arr.fill.solid()
                    arr.fill.fore_color.rgb = hdr_color
                    arr.line.fill.background()
                    if c_i < len(connectors) and connectors[c_i]:
                        tb_a = s.shapes.add_textbox(
                            Inches(x + 0.63), Inches(ay - 0.01), Inches(col_w - 0.72), Inches(conn_h + 0.02)
                        )
                        tf_a = tb_a.text_frame
                        tf_a.margin_left = tf_a.margin_top = Inches(0)
                        p_a = tf_a.paragraphs[0]
                        _add_formatted_runs(p_a, connectors[c_i], font_size=6.3, color=NAVY, bold=True)

            # Bottom Stage Handoff Box inside the Stage Rectangle
            out_y = stage_top + stage_h - 0.64
            out_state = st.get("handoff_status", "green")
            out_bg, out_bdr, _, _ = status_palette.get(out_state, status_palette["green"])
            out_box = s.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x + 0.07), Inches(out_y), Inches(col_w - 0.14), Inches(0.58)
            )
            out_box.adjustments[0] = 0.05
            out_box.fill.solid()
            out_box.fill.fore_color.rgb = out_bg
            out_box.line.color.rgb = out_bdr
            out_box.line.width = Pt(1.3)
            tf_out = out_box.text_frame
            tf_out.word_wrap = True
            tf_out.margin_left = tf_out.margin_right = Inches(0.05)
            tf_out.margin_top = tf_out.margin_bottom = Inches(0.02)
            p_out = tf_out.paragraphs[0]
            _add_formatted_runs(p_out, st["handoff_text"], font_size=6.7, color=DARK)

            # Inter-Stage Horizontal Connector Arrow between Stage Rectangles
            if idx < 3 and idx < len(handoff_arrows):
                hx = x + col_w + 0.02
                hw = gap_w - 0.04
                h_info = handoff_arrows[idx]
                h_col = GREEN if h_info.get("active", True) else PENDING_BDR
                h_arr = s.shapes.add_shape(
                    MSO_SHAPE.RIGHT_ARROW, Inches(hx), Inches(stage_top + 2.15), Inches(hw), Inches(0.28)
                )
                h_arr.fill.solid()
                h_arr.fill.fore_color.rgb = h_col
                h_arr.line.color.rgb = NAVY if h_info.get("active", True) else PENDING_BDR
                h_arr.line.width = Pt(0.8)

                tb_ht = s.shapes.add_textbox(
                    Inches(hx - 0.03), Inches(stage_top + 1.48), Inches(hw + 0.06), Inches(0.64)
                )
                tf_ht = tb_ht.text_frame
                tf_ht.word_wrap = True
                tf_ht.margin_left = tf_ht.margin_right = tf_ht.margin_top = Inches(0)
                p_ht = tf_ht.paragraphs[0]
                p_ht.alignment = PP_ALIGN.CENTER
                _add_formatted_runs(p_ht, h_info.get("top_label", ""), font_size=6.4, color=NAVY, bold=True)

                tb_hb = s.shapes.add_textbox(
                    Inches(hx - 0.03), Inches(stage_top + 2.47), Inches(hw + 0.06), Inches(0.95)
                )
                tf_hb = tb_hb.text_frame
                tf_hb.word_wrap = True
                tf_hb.margin_left = tf_hb.margin_right = tf_hb.margin_top = Inches(0)
                p_hb = tf_hb.paragraphs[0]
                p_hb.alignment = PP_ALIGN.CENTER
                _add_formatted_runs(p_hb, h_info.get("bottom_label", ""), font_size=6.2, color=DARK)

        # Bottom Storyline Takeaway Box
        self.add_callout(
            s,
            0.24,
            6.38,
            12.85,
            0.74,
            bottom_callout,
            bg_color=CALLOUT_BG,
            border_color=GOLD,
            font_size=8.8,
        )
        return s

    def save(self, path):
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        self.prs.save(path)

