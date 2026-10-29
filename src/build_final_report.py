"""
Build the submission-ready QM640 Final Report (APA 7 student paper).

All numbers are read programmatically from `data/interim/`, `data/final/`,
`outputs/interim/`, and `outputs/final/`.

Usage:
    python src/build_final_report.py

Outputs:
    final/QM_640_Final_Report_Sandeep_Surnella.docx
    final/QM_640_Final_Report_Sandeep_Surnella.pdf
"""

import argparse
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from report.docx_apa import APADoc  # noqa: E402
from report.final_context import BASENAME, OUT_DIR, load_all_context  # noqa: E402
from report.final_sections_part1 import build_part1  # noqa: E402
from report.final_sections_part2 import build_part2  # noqa: E402


def build(ctx, toc_pages=None):
    D = APADoc()
    build_part1(D, ctx, toc_pages=toc_pages)
    build_part2(D, ctx)
    return D


def convert_docx_to_pdf(docx_path, pdf_path):
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    script = f'''
    tell application "Microsoft Word"
        launch
        open POSIX file "{docx_path}"
        set activeDoc to active document
        save as activeDoc file name "{pdf_path}" file format format PDF
        close activeDoc saving no
    end tell
    '''
    res = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Word PDF conversion failed: {res.stderr}")


def _norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def find_pages(pdf_path, headings):
    import pymupdf
    pages = []
    with pymupdf.open(pdf_path) as doc:
        for pg in doc:
            bold = []
            for blk in pg.get_text("dict")["blocks"]:
                for ln in blk.get("lines", []):
                    spans = [s for s in ln["spans"] if s["text"].strip()]
                    if spans and all(("Bold" in s["font"]) or (s["flags"] & 16) for s in spans):
                        bold.append(_norm("".join(s["text"] for s in spans)))
            cands = set(bold)
            for n in (2, 3):
                cands |= {"".join(bold[i : i + n]) for i in range(len(bold) - n + 1)}
            pages.append(cands)
        total_pages = len(pages)
    start = next(i for i in range(1, len(pages)) if "abstract" in pages[i] or "introduction" in pages[i])
    result, cur = {}, start
    for idx, (lvl, txt) in enumerate(headings):
        if lvl > 2:
            continue
        key = _norm(txt)
        for i in range(cur, len(pages)):
            if key in pages[i]:
                result[idx] = str(i + 1)
                cur = i
                break
    return result, total_pages


def main(docx_only=False):
    os.makedirs(OUT_DIR, exist_ok=True)
    docx_path = os.path.join(OUT_DIR, BASENAME + ".docx")
    pdf_path = os.path.join(OUT_DIR, BASENAME + ".pdf")
    ctx = load_all_context()

    D = build(ctx)
    entries = list(D.headings)
    D = build(ctx, toc_pages=(entries, {i: "00" for i in range(len(entries))}))
    D.save(docx_path)
    n_refs, n_targets, missing_xrefs = D.xref_summary()
    print(f"Saved initial DOCX: {docx_path} (Cross-references: {n_refs} -> {n_targets} targets, missing: {len(missing_xrefs)})")

    if docx_only:
        return

    convert_docx_to_pdf(docx_path, pdf_path)
    pages, total_pages = find_pages(pdf_path, entries)
    D = build(ctx, toc_pages=(entries, pages))
    D.save(docx_path)
    convert_docx_to_pdf(docx_path, pdf_path)
    pages2, total_pages = find_pages(pdf_path, entries)
    if pages2 != pages:
        D = build(ctx, toc_pages=(entries, pages2))
        D.save(docx_path)
        convert_docx_to_pdf(docx_path, pdf_path)
        pages2, total_pages = find_pages(pdf_path, entries)

    missing = [entries[i][1] for i in range(len(entries)) if entries[i][0] <= 2 and i not in pages2]
    print(f"Saved final DOCX and PDF: {docx_path} and {pdf_path} (Total pages: {total_pages})")
    if missing:
        print("Headings not located in PDF:", missing)

    # Compute Core Page Count (Abstract through end of Section 6, before References)
    abs_idx = next(i for i, (_, t) in enumerate(entries) if t == "Abstract")
    intro_idx = next(i for i, (_, t) in enumerate(entries) if t == "Introduction")
    ref_idx = next(i for i, (_, t) in enumerate(entries) if t == "References")
    app_idx = next(i for i, (_, t) in enumerate(entries) if t == "Appendix A")
    p_abs = int(pages2[abs_idx])
    p_intro = int(pages2[intro_idx])
    p_ref = int(pages2[ref_idx])
    p_app = int(pages2[app_idx])
    print(f"Pagination Summary:")
    print(f"  - Abstract starts on page {p_abs}")
    print(f"  - Introduction starts on page {p_intro}")
    print(f"  - References starts on page {p_ref}")
    print(f"  - Appendix A starts on page {p_app}")
    print(f"  - Core Report Pages (Abstract through Section 6, excl. Title, TOC, References, Appendices): {p_ref - p_abs} pages")
    print(f"  - Core Body Pages (Introduction through Section 6): {p_ref - p_intro} pages")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--docx-only", action="store_true")
    args = ap.parse_args()
    main(docx_only=args.docx_only)
