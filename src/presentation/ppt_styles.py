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
    Parse lightweight inline tags `<b>...</b>` and `<i>...</i>` into pptx runs.
    """
    tokens = re.split(r"(</?[bi]>)", str(text))
    b_state = bold
    i_state = italic
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
        run = p.add_run()
        run.text = tok
        run.font.name = font_name
        run.font.size = Pt(font_size)
        run.font.bold = b_state
        run.font.italic = i_state
        run.font.color.rgb = color


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

    def save(self, path):
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        self.prs.save(path)

