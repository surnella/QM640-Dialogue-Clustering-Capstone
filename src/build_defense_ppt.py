"""
Build the exhaustive 42-slide Widescreen (16:9) QM640 Capstone Defense PowerPoint Presentation.

Usage:
    python src/build_defense_ppt.py

Output:
    final/QM_640_Defense_Presentation_Sandeep_Surnella.pptx
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from presentation.ppt_styles import DefenseDeck  # noqa: E402
from presentation.slides_part1 import build_slides_part1  # noqa: E402
from presentation.slides_part2 import build_slides_part2  # noqa: E402
from report.final_context import OUT_DIR, load_all_context  # noqa: E402

PPT_OUT = os.path.join(OUT_DIR, "QM_640_Defense_Presentation_Sandeep_Surnella.pptx")


def main():
    ctx = load_all_context()
    deck = DefenseDeck(total_slides_est=42)
    build_slides_part1(deck, ctx)
    build_slides_part2(deck, ctx)
    deck.save(PPT_OUT)
    print(f"Saved Defense Presentation: {PPT_OUT} (Total slides: {deck.slide_num})")


if __name__ == "__main__":
    main()

