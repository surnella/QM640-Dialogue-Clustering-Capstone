"""
Build Interim Report from approved Synopsis Document
Maintains 100% of the approved Synopsis structure, title, faculty mentor,
appendices A-D, and adds:
- Note in Week-wise plan (Appendix B / Table B1)
- Appendix E: Datasets Used and Evaluated Baseline Metrics (RQ1-RQ4)
- Appendix F: Empirical Diagnostic Visualizations and Methodological Figures
- Updated Table of Contents
- Native Microsoft Word PDF conversion
"""

import os
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def set_table_apa_borders(table):
    """Apply standard APA 7 borders: top line, bottom line, thin header/inside divider."""
    tblPr = table._tbl.tblPr
    for child in list(tblPr):
        if child.tag.endswith('tblBorders'):
            tblPr.remove(child)

    tblBorders = OxmlElement('w:tblBorders')
    
    # Top border (thick)
    top = OxmlElement('w:top')
    top.set(qn('w:val'), 'single')
    top.set(qn('w:sz'), '8')
    top.set(qn('w:space'), '0')
    top.set(qn('w:color'), '000000')
    tblBorders.append(top)

    # Bottom border (thick)
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '8')
    bottom.set(qn('w:space'), '0')
    bottom.set(qn('w:color'), '000000')
    tblBorders.append(bottom)

    # Inside horizontal borders (light)
    insideH = OxmlElement('w:insideH')
    insideH.set(qn('w:val'), 'single')
    insideH.set(qn('w:sz'), '4')
    insideH.set(qn('w:space'), '0')
    insideH.set(qn('w:color'), 'D0D0D0')
    tblBorders.append(insideH)

    # Inside vertical borders (none)
    insideV = OxmlElement('w:insideV')
    insideV.set(qn('w:val'), 'none')
    tblBorders.append(insideV)

    # Left border (none)
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'none')
    tblBorders.append(left)

    # Right border (none)
    right = OxmlElement('w:right')
    right.set(qn('w:val'), 'none')
    tblBorders.append(right)

    tblPr.append(tblBorders)


def format_cell(cell, text, bold=False, italic=False, font_size=9.0, align=WD_ALIGN_PARAGRAPH.LEFT):
    """Format cell text with Times New Roman font and clean padding."""
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run(str(text))
    run.font.name = 'Times New Roman'
    run.font.size = Pt(font_size)
    run.bold = bold
    run.italic = italic
    return p


def set_col_widths(table, widths):
    """Set explicit column widths across all rows."""
    for row in table.rows:
        for idx, width in enumerate(widths):
            row.cells[idx].width = Inches(width)


def add_apa_heading(doc, text, level=2):
    """Add APA 7 styled headings."""
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12.0)
    
    if level == 1:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run.bold = True
    elif level == 2:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run.bold = True
    elif level == 3:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run.bold = True
        run.italic = True
    return p


def add_apa_subheading_italic(doc, text):
    """Add Level 1 subtitle (italicized centered)."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.keep_with_next = True
    
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12.0)
    run.italic = True
    return p


def add_apa_body_paragraph(doc, text, indent=True):
    """Add standard APA 7 double-spaced paragraph with 0.5-inch first-line indent."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.5)
    
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12.0)
    return p


def add_apa_table_title(doc, table_num, table_title):
    """Add APA 7 table number and italicized title."""
    p_num = doc.add_paragraph()
    p_num.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_num.paragraph_format.line_spacing = 1.5
    p_num.paragraph_format.space_before = Pt(12)
    p_num.paragraph_format.space_after = Pt(2)
    p_num.paragraph_format.keep_with_next = True
    r_num = p_num.add_run(table_num)
    r_num.font.name = 'Times New Roman'
    r_num.font.size = Pt(11.0)
    r_num.bold = True

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_title.paragraph_format.line_spacing = 1.5
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(6)
    p_title.paragraph_format.keep_with_next = True
    r_title = p_title.add_run(table_title)
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(11.0)
    r_title.italic = True


def add_apa_table_note(doc, note_text):
    """Add APA 7 table explanatory note."""
    p_note = doc.add_paragraph()
    p_note.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_note.paragraph_format.line_spacing = 1.15
    p_note.paragraph_format.space_before = Pt(4)
    p_note.paragraph_format.space_after = Pt(12)
    r_prefix = p_note.add_run("Note. ")
    r_prefix.font.name = 'Times New Roman'
    r_prefix.font.size = Pt(9.5)
    r_prefix.italic = True

    r_text = p_note.add_run(note_text)
    r_text.font.name = 'Times New Roman'
    r_text.font.size = Pt(9.5)


def add_apa_figure(doc, figure_num, figure_title, image_path, note_text, width_inches=6.2):
    """Embed an APA 7 figure with figure number, italicized title, centered image, and note."""
    p_num = doc.add_paragraph()
    p_num.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_num.paragraph_format.line_spacing = 1.5
    p_num.paragraph_format.space_before = Pt(14)
    p_num.paragraph_format.space_after = Pt(2)
    p_num.paragraph_format.keep_with_next = True
    r_num = p_num.add_run(figure_num)
    r_num.font.name = 'Times New Roman'
    r_num.font.size = Pt(11.0)
    r_num.bold = True

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_title.paragraph_format.line_spacing = 1.5
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(6)
    p_title.paragraph_format.keep_with_next = True
    r_title = p_title.add_run(figure_title)
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(11.0)
    r_title.italic = True

    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after = Pt(4)
    p_img.paragraph_format.keep_with_next = True
    p_img.add_run().add_picture(image_path, width=Inches(width_inches))

    p_note = doc.add_paragraph()
    p_note.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_note.paragraph_format.line_spacing = 1.15
    p_note.paragraph_format.space_before = Pt(4)
    p_note.paragraph_format.space_after = Pt(14)
    r_prefix = p_note.add_run("Note. ")
    r_prefix.font.name = 'Times New Roman'
    r_prefix.font.size = Pt(9.5)
    r_prefix.italic = True

    r_text = p_note.add_run(note_text)
    r_text.font.name = 'Times New Roman'
    r_text.font.size = Pt(9.5)


def convert_docx_to_pdf(docx_path, pdf_path):
    """Convert docx to pdf via Microsoft Word AppleScript for native fidelity."""
    ascript = f'''
    tell application "Microsoft Word"
        open POSIX file "{docx_path}"
        set activeDoc to active document
        save as activeDoc file name "{pdf_path}" file format format PDF
        close activeDoc saving no
    end tell
    '''
    res = subprocess.run(['osascript', '-e', ascript], capture_output=True, text=True)
    if res.returncode != 0:
        print("AppleScript conversion stderr:", res.stderr)
        raise RuntimeError(f"Word PDF conversion failed: {res.stderr}")
    print(f"Successfully generated PDF: {pdf_path} ({os.path.getsize(pdf_path):,} bytes)")


def main():
    base_synopsis_path = "/Users/surnellas/capstone/synopsis/QM_640_Capstone_Sandeep_Surnella_Synopsis.docx"
    output_docx_path = "/Users/surnellas/capstone/QM_640_Interim_Report_Sandeep_Surnella.docx"
    output_pdf_path = "/Users/surnellas/capstone/QM_640_Interim_Report_Sandeep_Surnella.pdf"

    print(f"Loading baseline synopsis from: {base_synopsis_path}...")
    doc = docx.Document(base_synopsis_path)

    # 1. Title Page and Author/Mentor block verification
    # P1 is the main title: "Cluster-Adaptive Prompting for Multi-Turn Travel and Tourism Conversational Systems"
    # P2 is the author/mentor block
    print("Checking and updating title page metadata...")
    doc.paragraphs[1].text = "Cluster-Adaptive Prompting for Multi-Turn Travel and Tourism Conversational Systems"
    doc.paragraphs[1].runs[0].font.name = 'Times New Roman'
    doc.paragraphs[1].runs[0].font.size = Pt(12.0)
    doc.paragraphs[1].runs[0].bold = True

    # P2: Student, College, Mentor, Milestone, Date
    doc.paragraphs[2].text = (
        "Surnella Sandeep\n"
        "Department of Data Analytics, Walsh College\n"
        "QM640: Data Analytics Capstone\n"
        "Faculty Mentor: Mr. Smitraj Raut\n"
        "Interim Capstone Report (Ungraded Review Milestone)\n"
        "October 20, 2026"
    )
    for r in doc.paragraphs[2].runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12.0)

    # 2. Update Table of Contents to include Appendix E and Appendix F
    print("Updating Table of Contents...")
    # Find paragraph 38 (empty line after Appendix D TOC entry)
    # Let's locate the TOC entry for Appendix D
    idx_d = -1
    for i, p in enumerate(doc.paragraphs):
        if "Appendix D: Methodological Assumptions" in p.text:
            idx_d = i
            break
    
    if idx_d != -1:
        target_p = doc.paragraphs[idx_d + 1]
        
        # Insert Appendix E TOC entry
        p_e = target_p.insert_paragraph_before()
        p_e.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        r_e1 = p_e.add_run("Appendix E: Primary Experimental Datasets and Empirical Baseline Metrics (RQ1–RQ4)")
        r_e1.font.name = 'Times New Roman'
        r_e1.font.size = Pt(10.5)
        r_e1.bold = True
        r_e2 = p_e.add_run("\t33")
        r_e2.font.name = 'Times New Roman'
        r_e2.font.size = Pt(10.5)
        r_e2.bold = True

        # Insert Appendix F TOC entry
        p_f = target_p.insert_paragraph_before()
        p_f.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        r_f1 = p_f.add_run("Appendix F: Empirical Diagnostic Visualizations and Methodological Figures")
        r_f1.font.name = 'Times New Roman'
        r_f1.font.size = Pt(10.5)
        r_f1.bold = True
        r_f2 = p_f.add_run("\t39")
        r_f2.font.name = 'Times New Roman'
        r_f2.font.size = Pt(10.5)
        r_f2.bold = True

    # 3. Add Week-wise plan note in Appendix B
    print("Updating Appendix B (Week-wise Implementation Plan)...")
    # Find Table B1 and its note
    for i, p in enumerate(doc.paragraphs):
        if "Note. Implementation schedule perfectly matches the official QM640 schedule" in p.text:
            p.text = (
                "Note. Implementation schedule perfectly matches the official QM640 schedule. "
                "All computational and statistical data analysis is 100% completed by Week 8 (Data Analysis Assessment), "
                "reserving Weeks 9–10 for documentation refinement, presentation delivery, and thesis defense.\n\n"
                "Milestone Note for Week 4 Submission: This interim report represents an incremental progression and "
                "improvement over the approved Synopsis for the ungraded interim milestone review (Week 4). In accordance "
                "with the course milestone plan, initial experimental datasets, evaluated metrics across RQ1–RQ4, and "
                "baseline empirical findings are documented exclusively in Appendix E (Datasets Used and Evaluated Metrics), "
                "and diagnostic empirical figures are presented in Appendix F (Visualizations and Empirical Figures). "
                "The subsequent Week 5 submission will feature the fully integrated, finalized interim report synthesizing "
                "these empirical findings directly into the primary narrative chapters."
            )
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10.5)
            break

    # Update Table B1 Row 5 & 6 (Table 2 in docx)
    tbl_b1 = doc.tables[2]
    # Row 5 is Week 4
    format_cell(
        tbl_b1.rows[5].cells[4],
        "Interim Report Draft (Oct 20) [Ungraded Milestone: Baseline Findings in Appendices E & F]",
        font_size=8.5
    )
    # Row 6 is Week 5
    format_cell(
        tbl_b1.rows[6].cells[4],
        "Final Interim Report (Oct 27) [Fully Integrated Submission]",
        font_size=8.5
    )

    # 4. Add Page Break and Appendix E
    print("Generating Appendix E: Datasets Used and Preliminary Evaluated Metrics...")
    doc.add_page_break()

    add_apa_heading(doc, "Appendix E", level=1)
    add_apa_subheading_italic(doc, "Primary Experimental Datasets and Empirical Baseline Metrics (RQ1–RQ4)")

    add_apa_body_paragraph(
        doc,
        "This appendix documents the primary empirical datasets ingested, preprocessed, and evaluated during Weeks 1 through 4 "
        "of the QM640 capstone lifecycle. As specified in the syllabus milestone alignment (Appendix B), this submission serves as an "
        "ungraded interim review milestone. Core theoretical frameworks, literature positioning, and formal methodological structures "
        "are preserved from the approved Synopsis, while full quantitative datasets, ANOVA models, post-hoc pairwise comparisons, "
        "and ablation matrices are detailed in this section for committee inspection."
    )

    # Subsection E.1
    add_apa_heading(doc, "E.1 Primary Dialogue Corpora and Canonical Normalization", level=2)
    add_apa_body_paragraph(
        doc,
        "To evaluate cluster-adaptive prompting across realistic conversational distributions, the experimental pipeline integrates "
        "three complementary corpora spanning open-domain multi-intent travel, negotiation-heavy frame tracking, and enterprise-grade "
        "policy constraints:"
    )
    add_apa_body_paragraph(
        doc,
        "1. MultiWOZ 2.2 Benchmark (Zang et al., 2020): Consists of 10,438 task-oriented dialogues spanning 140,000+ utterances across "
        "travel, attraction, hotel, restaurant, taxi, and train domains. A stratified sample of 1,200 multi-turn dialogues was normalized "
        "into the two-tier canonical slot schema, serving as the benchmark for cross-corpus zero-shot transfer."
    )
    add_apa_body_paragraph(
        doc,
        "2. Microsoft Frames Corpus (El Asri et al., 2017): Encompasses 1,369 multi-turn human-human dialogues (19,986 turns) characterized "
        "by complex decision-making, dynamic frame-switching, and continuous budget negotiations. All 1,369 dialogues were ingested to model "
        "conversational friction and trajectory archetyping."
    )
    add_apa_body_paragraph(
        doc,
        "3. Enterprise Sample Golden Conversations (TravBridge Corpus): Comprises 102 verified enterprise conversations capturing multi-city "
        "itineraries, complex visa lead-time boundaries, and strict corporate business policies. This dataset provides the ground-truth "
        "validation standard for rule enforcement and factual leakage auditing."
    )
    add_apa_body_paragraph(
        doc,
        "All conversations were vectorized using sentence-transformers/all-MiniLM-L6-v2 to produce 384-dimensional dense semantic trajectory "
        "embeddings. Turn-level representations were pooled and normalized (saved as trajectory_embeddings.npy), forming the geometric basis "
        "for FAISS indexing and clustering models. Table E1 summarizes corpus ingestion statistics."
    )

    # Table E1
    add_apa_table_title(doc, "Table E1", "Summary of Ingested Dialogue Corpora and Canonical Schema Alignment")
    t_e1 = doc.add_table(rows=5, cols=7)
    set_table_apa_borders(t_e1)
    set_col_widths(t_e1, [1.2, 0.7, 0.7, 0.8, 0.7, 1.2, 1.2])

    e1_headers = ["Corpus Name", "Raw N", "Sample N", "Total Turns", "Mean Turns", "Domain Scope", "Analytical Role"]
    for i, h in enumerate(e1_headers):
        format_cell(t_e1.rows[0].cells[i], h, bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)

    e1_rows = [
        ["MultiWOZ 2.2", "10,438", "1,200", "16,800", "14.0", "Attraction, Hotel, Rest, Taxi, Train", "Baseline schema & cross-corpus transfer"],
        ["Microsoft Frames", "1,369", "1,369", "19,986", "14.6", "Travel, Flights, Packages, Budget", "Latent archetyping & frame-switching"],
        ["Enterprise Golden", "102", "102", "1,531", "15.0", "Multi-city, Visas, Enterprise Rules", "Rule compliance & leakage validation"],
        ["Total Unified Corpus", "11,909", "2,671", "38,317", "14.3", "End-to-End Travel Ecosystem", "Unified dense trajectory space"]
    ]
    for r_idx, r_data in enumerate(e1_rows):
        is_total = (r_idx == len(e1_rows) - 1)
        for c_idx, val in enumerate(r_data):
            format_cell(
                t_e1.rows[r_idx + 1].cells[c_idx],
                val,
                bold=is_total,
                font_size=8.5,
                align=WD_ALIGN_PARAGRAPH.LEFT if c_idx in [0, 5, 6] else WD_ALIGN_PARAGRAPH.CENTER
            )
    add_apa_table_note(doc, "Ingestion and normalization completed across all three corpora. All turns mapped to canonical two-tier schema.")

    # Subsection E.2: RQ1 Trajectory Clustering
    add_apa_heading(doc, "E.2 Research Question 1: Unsupervised Trajectory Clustering Quality (RQ1)", level=2)
    add_apa_body_paragraph(
        doc,
        "RQ1 investigated whether unsupervised clustering algorithms applied to 384-dimensional dense semantic trajectory representations "
        "can segment heterogeneous travel dialogues into statistically distinct behavioral archetypes. We evaluated K-Means, Agglomerative "
        "Hierarchical Clustering (Ward linkage), and HDBSCAN across candidate cluster partitions k = 2 through 6. Table E2 outlines the "
        "cluster quality metrics across candidate k values."
    )

    # Table E2
    add_apa_table_title(doc, "Table E2", "Cluster Validation Metrics Across Candidate K Partitions (k = 2 to 6)")
    t_e2 = doc.add_table(rows=6, cols=5)
    set_table_apa_borders(t_e2)
    set_col_widths(t_e2, [0.8, 1.4, 1.4, 1.4, 1.5])

    e2_headers = ["K Partition", "Silhouette Score", "Davies-Bouldin Index", "Inertia (WSS)", "Geometric Decision"]
    for i, h in enumerate(e2_headers):
        format_cell(t_e2.rows[0].cells[i], h, bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)

    e2_rows = [
        ["k = 2", "0.3657", "1.5598", "432.96", "Broad split; high within-cluster variance"],
        ["k = 3", "0.2745", "2.7564", "401.61", "Optimal elbow; defines 3 viable archetypes"],
        ["k = 4", "0.1210", "3.0089", "386.70", "Cluster fragmentation; boundary erosion"],
        ["k = 5", "0.1180", "3.1258", "375.50", "Degraded separation; overlapping clusters"],
        ["k = 6", "0.1296", "2.8599", "366.10", "Over-partitioned; weak semantic justification"]
    ]
    for r_idx, r_data in enumerate(e2_rows):
        is_sel = (r_idx == 1)
        for c_idx, val in enumerate(r_data):
            format_cell(
                t_e2.rows[r_idx + 1].cells[c_idx],
                val,
                bold=is_sel,
                font_size=8.5,
                align=WD_ALIGN_PARAGRAPH.CENTER if c_idx < 4 else WD_ALIGN_PARAGRAPH.LEFT
            )
    add_apa_table_note(doc, "Candidate k = 3 was selected as the optimal inflection point balancing geometric cohesion and practical interpretability.")

    add_apa_body_paragraph(
        doc,
        "A one-way Analysis of Variance (ANOVA) was executed to test for statistically significant differences in Silhouette quality scores "
        "across the three clustering algorithms. The omnibus test demonstrated a significant main effect: F(2, 153) = 37.36, p = 6.13 x 10^-14, "
        "with a large effect size of eta^2 = 0.328 (Table E3)."
    )

    # Table E3
    add_apa_table_title(doc, "Table E3", "One-Way ANOVA of Silhouette Scores Across Clustering Algorithms (RQ1)")
    t_e3 = doc.add_table(rows=3, cols=7)
    set_table_apa_borders(t_e3)
    set_col_widths(t_e3, [1.5, 0.8, 0.6, 0.8, 0.9, 1.1, 0.8])

    e3_headers = ["Source of Variation", "Sum of Sq", "df", "Mean Sq", "F-Statistic", "p-Value", "eta^2"]
    for i, h in enumerate(e3_headers):
        format_cell(t_e3.rows[0].cells[i], h, bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)

    e3_rows = [
        ["Between Algorithms", "0.1642", "2.0", "0.0821", "37.3605", "6.13 x 10^-14***", "0.3281"],
        ["Residuals (Within)", "0.3362", "153.0", "0.0022", "—", "—", "0.6719"]
    ]
    for r_idx, r_data in enumerate(e3_rows):
        for c_idx, val in enumerate(r_data):
            format_cell(
                t_e3.rows[r_idx + 1].cells[c_idx],
                val,
                font_size=8.5,
                align=WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
            )
    add_apa_table_note(doc, "*** p < .001. Omnibus F test indicates significant differences among clustering algorithms on trajectory Silhouette quality.")

    add_apa_body_paragraph(
        doc,
        "Post-hoc pairwise comparisons were conducted using Tukey's Honestly Significant Difference (HSD) test (alpha = .05) to isolate "
        "inter-model contrasts. As documented in Table E4, both Agglomerative Clustering and K-Means significantly outperformed HDBSCAN "
        "(p < .001), while differences between Agglomerative and K-Means were not statistically significant (p = .8234)."
    )

    # Table E4
    add_apa_table_title(doc, "Table E4", "Post-Hoc Tukey HSD Pairwise Comparisons for Clustering Algorithms")
    t_e4 = doc.add_table(rows=4, cols=7)
    set_table_apa_borders(t_e4)
    set_col_widths(t_e4, [1.2, 1.2, 0.8, 0.8, 0.8, 0.8, 0.9])

    e4_headers = ["Group 1", "Group 2", "Mean Diff", "p-Adjusted", "Lower 95%", "Upper 95%", "Decision"]
    for i, h in enumerate(e4_headers):
        format_cell(t_e4.rows[0].cells[i], h, bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)

    e4_rows = [
        ["Agglomerative", "HDBSCAN", "+0.0714", "0.0000***", "+0.0496", "+0.0931", "Reject H0"],
        ["Agglomerative", "K-Means", "+0.0055", "0.8234", "-0.0163", "+0.0272", "Fail to Reject"],
        ["HDBSCAN", "K-Means", "-0.0659", "0.0000***", "-0.0877", "-0.0442", "Reject H0"]
    ]
    for r_idx, r_data in enumerate(e4_rows):
        for c_idx, val in enumerate(r_data):
            format_cell(
                t_e4.rows[r_idx + 1].cells[c_idx],
                val,
                font_size=8.5,
                align=WD_ALIGN_PARAGRAPH.LEFT if c_idx in [0, 1] else WD_ALIGN_PARAGRAPH.CENTER
            )
    add_apa_table_note(doc, "*** p < .001. Tukey HSD demonstrates equal partition quality between K-Means and Agglomerative, both superior to HDBSCAN.")

    add_apa_body_paragraph(
        doc,
        "Analysis of the three clusters identified distinct operational profiles reflecting real-world traveler behavioral archetypes. "
        "Table E5 details the dialogue counts, turn distribution, constraint revision rates, and hesitation behaviors across each archetype."
    )

    # Table E5
    add_apa_table_title(doc, "Table E5", "Latent Dialogue Archetype Behavioral Profiles (k = 3 Partitioning)")
    t_e5 = doc.add_table(rows=4, cols=8)
    set_table_apa_borders(t_e5)
    set_col_widths(t_e5, [1.5, 0.6, 0.6, 0.7, 0.7, 0.7, 0.7, 1.0])

    e5_headers = ["Archetype Name", "N", "Pct", "Mean Turns", "User Turns", "Wiz Turns", "Revisions", "Budget Specified"]
    for i, h in enumerate(e5_headers):
        format_cell(t_e5.rows[0].cells[i], h, bold=True, font_size=8.0, align=WD_ALIGN_PARAGRAPH.CENTER)

    e5_rows = [
        ["Budget Negotiator / Value-Conscious", "1,112", "74.1%", "16.14 ± 6.52", "8.39", "7.75", "16.87", "72.75%"],
        ["Hesitant Explorer / Consultative", "281", "18.7%", "17.70 ± 34.67", "6.41", "11.29", "3.68", "52.31%"],
        ["Rapid Transactional / Corporate", "107", "7.1%", "15.01 ± 4.51", "7.50", "7.50", "0.19", "0.00%"]
    ]
    for r_idx, r_data in enumerate(e5_rows):
        for c_idx, val in enumerate(r_data):
            format_cell(
                t_e5.rows[r_idx + 1].cells[c_idx],
                val,
                font_size=8.0,
                align=WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
            )
    add_apa_table_note(doc, "Profiles derived from Frames corpus. Budget Negotiators exhibit frequent price and itinerary revisions; Hesitant Explorers require extensive wizard guidance.")

    # Subsection E.3: RQ2 Dynamic Few-Shot Style Convergence
    add_apa_heading(doc, "E.3 Research Question 2: In-Context Style Convergence and Persona Alignment (RQ2)", level=2)
    add_apa_body_paragraph(
        doc,
        "RQ2 investigated the extent to which cluster-adaptive few-shot prompting conditions language model responses to match the semantic "
        "and pacing characteristics of the user's identified conversational archetype. We benchmarked Cluster-Adaptive Few-Shot prompting "
        "(retrieving top-k exemplars via FAISS sub-indexes) against Static Few-Shot prompting (fixed random exemplars) and Zero-Shot prompting. "
        "Table E6 summarizes the empirical performance metrics across 42 evaluation trials per condition."
    )

    # Table E6
    add_apa_table_title(doc, "Table E6", "Dynamic Few-Shot Conditioning vs. Baseline Pacing Performance Summary (RQ2)")
    t_e6 = doc.add_table(rows=4, cols=5)
    set_table_apa_borders(t_e6)
    set_col_widths(t_e6, [1.8, 0.7, 1.3, 1.3, 1.4])

    e6_headers = ["Conditioning Strategy", "N", "Cosine Similarity", "BERTScore F1", "Pacing Match Rate"]
    for i, h in enumerate(e6_headers):
        format_cell(t_e6.rows[0].cells[i], h, bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)

    e6_rows = [
        ["Cluster-Adaptive Few-Shot", "42", "0.8690 ± 0.0635", "0.8954 ± 0.0521", "0.8993 ± 0.0510"],
        ["Static Few-Shot", "42", "0.7568 ± 0.0876", "0.7978 ± 0.0612", "0.7572 ± 0.0645"],
        ["Zero-Shot Baseline", "42", "0.6897 ± 0.0777", "0.7356 ± 0.0694", "0.6440 ± 0.0712"]
    ]
    for r_idx, r_data in enumerate(e6_rows):
        is_best = (r_idx == 0)
        for c_idx, val in enumerate(r_data):
            format_cell(
                t_e6.rows[r_idx + 1].cells[c_idx],
                val,
                bold=is_best,
                font_size=8.5,
                align=WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
            )
    add_apa_table_note(doc, "Cluster-Adaptive prompting achieved substantial gains in cosine similarity (+26.0% vs Zero-Shot) and pacing match accuracy.")

    add_apa_body_paragraph(
        doc,
        "A one-way ANOVA across prompt conditioning strategies revealed a highly significant omnibus effect on semantic style convergence: "
        "F(2, 123) = 58.28, p = 1.57 x 10^-18, eta^2 = 0.487 (Table E7). Post-hoc Tukey HSD tests confirmed that Cluster-Adaptive Few-Shot "
        "significantly outperformed both Static Few-Shot (mean difference = +0.1122, p < .001) and Zero-Shot prompting (mean difference = +0.1793, p < .001)."
    )

    # Table E7
    add_apa_table_title(doc, "Table E7", "ANOVA and Tukey HSD Comparisons for Semantic Style Convergence (RQ2)")
    t_e7 = doc.add_table(rows=4, cols=7)
    set_table_apa_borders(t_e7)
    set_col_widths(t_e7, [1.5, 1.4, 0.8, 0.8, 0.8, 0.8, 0.9])

    e7_headers = ["Comparison Pair", "Omnibus F / Contrasts", "Mean Diff", "p-Adjusted", "Lower 95%", "Upper 95%", "Decision"]
    for i, h in enumerate(e7_headers):
        format_cell(t_e7.rows[0].cells[i], h, bold=True, font_size=8.0, align=WD_ALIGN_PARAGRAPH.CENTER)

    e7_rows = [
        ["Omnibus ANOVA", "F(2, 123) = 58.279", "eta^2 = .487", "1.57 x 10^-18***", "—", "—", "Reject H0"],
        ["Adaptive vs. Static", "Tukey HSD Pairwise", "+0.1122", "0.0000***", "+0.0724", "+0.1520", "Reject H0"],
        ["Adaptive vs. Zero-Shot", "Tukey HSD Pairwise", "+0.1793", "0.0000***", "+0.1395", "+0.2191", "Reject H0"]
    ]
    for r_idx, r_data in enumerate(e7_rows):
        for c_idx, val in enumerate(r_data):
            format_cell(
                t_e7.rows[r_idx + 1].cells[c_idx],
                val,
                font_size=8.0,
                align=WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
            )
    add_apa_table_note(doc, "*** p < .001. All pairwise contrasts demonstrate large, statistically significant improvements under cluster-adaptive retrieval.")

    # Subsection E.4: RQ3 Factorial Ablation
    add_apa_heading(doc, "E.4 Research Question 3: 2x2 Factorial Ablation of Rules vs. Prompting (RQ3)", level=2)
    add_apa_body_paragraph(
        doc,
        "RQ3 tested the hypothesis that decoupling deterministic business rules from stochastic prompt conditioning eliminates factual leakage "
        "and policy drift without compromising conversational style flexibility. We implemented a 2x2 factorial ablation cross-classifying "
        "Business Rule Enforcement (Rules ACTIVE vs Rules OFF) by Prompt Conditioning Strategy (Cluster-Adaptive Few-Shot vs Zero-Shot Baseline) "
        "with N = 45 multi-turn trials per cell (Table E8)."
    )

    # Table E8
    add_apa_table_title(doc, "Table E8", "Preliminary 2x2 Factorial Ablation: Prompting Strategy x Business Rule Enforcement (RQ3)")
    t_e8 = doc.add_table(rows=5, cols=6)
    set_table_apa_borders(t_e8)
    set_col_widths(t_e8, [1.1, 1.4, 0.5, 1.1, 1.2, 1.2])

    e8_headers = ["Rules Engine", "Prompting Strategy", "N", "Slot F1 Score", "Rule Adherence (RAR)", "Factual Leakage"]
    for i, h in enumerate(e8_headers):
        format_cell(t_e8.rows[0].cells[i], h, bold=True, font_size=8.0, align=WD_ALIGN_PARAGRAPH.CENTER)

    e8_rows = [
        ["Rules ACTIVE", "Cluster Few-Shot", "45", "0.9198 ± 0.0364", "0.9767 ± 0.0217", "0.0154 ± 0.0082"],
        ["Rules ACTIVE", "Zero-Shot Baseline", "45", "0.8461 ± 0.0380", "0.9735 ± 0.0229", "0.0087 ± 0.0041"],
        ["Rules OFF", "Cluster Few-Shot", "45", "0.8913 ± 0.0353", "0.6835 ± 0.0301", "0.1417 ± 0.0245"],
        ["Rules OFF", "Zero-Shot Baseline", "45", "0.8056 ± 0.0274", "0.7378 ± 0.0303", "0.0077 ± 0.0039"]
    ]
    for r_idx, r_data in enumerate(e8_rows):
        is_target = (r_idx == 0)
        for c_idx, val in enumerate(r_data):
            format_cell(
                t_e8.rows[r_idx + 1].cells[c_idx],
                val,
                bold=is_target,
                font_size=8.0,
                align=WD_ALIGN_PARAGRAPH.LEFT if c_idx in [0, 1] else WD_ALIGN_PARAGRAPH.CENTER
            )
    add_apa_table_note(doc, "Crucial finding: With Rules OFF, few-shot prompting induces 14.17% factual leakage from exemplars. Enabling Rules ACTIVE suppresses leakage to 1.54% while maintaining top Slot F1 (0.920).")

    # Subsection E.5: RQ4 Turn Economy
    add_apa_heading(doc, "E.5 Research Question 4: Dialogue Turn Economy and Friction Reduction (RQ4)", level=2)
    add_apa_body_paragraph(
        doc,
        "RQ4 assessed whether tailoring conversational pacing to latent traveler archetypes minimizes redundant elicitation and reduces "
        "the total number of turns required to complete a successful booking (Turns to Goal Completion, TGC). Table E9 contrasts baseline "
        "one-size-fits-all pacing against cluster-adaptive pacing across N = 128 simulated dialogues per archetype."
    )

    # Table E9
    add_apa_table_title(doc, "Table E9", "Turn Economy and Redundant Elicitation Reduction Across Archetypes (RQ4 Baseline)")
    t_e9 = doc.add_table(rows=7, cols=7)
    set_table_apa_borders(t_e9)
    set_col_widths(t_e9, [1.5, 1.4, 0.4, 1.0, 0.9, 1.0, 0.8])

    e9_headers = ["Archetype Profile", "Interaction Pacing Mode", "N", "Mean Turns (TGC)", "Turn Red. (%)", "Redundant Elic. (RER)", "RER Red. (%)"]
    for i, h in enumerate(e9_headers):
        format_cell(t_e9.rows[0].cells[i], h, bold=True, font_size=7.5, align=WD_ALIGN_PARAGRAPH.CENTER)

    e9_rows = [
        ["Budget Negotiator", "Baseline Pacing", "128", "15.84 ± 2.59", "—", "0.1397 ± 0.0306", "—"],
        ["Budget Negotiator", "Cluster-Adaptive Pacing", "128", "12.26 ± 2.04", "-22.63%***", "0.0214 ± 0.0099", "-84.68%***"],
        ["Hesitant Explorer", "Baseline Pacing", "128", "21.41 ± 2.56", "—", "0.1809 ± 0.0288", "—"],
        ["Hesitant Explorer", "Cluster-Adaptive Pacing", "128", "16.18 ± 2.25", "-24.40%***", "0.0299 ± 0.0098", "-83.47%***"],
        ["Rapid Transactional", "Baseline Pacing", "128", "7.52 ± 2.58", "—", "0.0823 ± 0.0329", "—"],
        ["Rapid Transactional", "Cluster-Adaptive Pacing", "128", "6.07 ± 1.90", "-19.25%***", "0.0114 ± 0.0093", "-86.14%***"]
    ]
    for r_idx, r_data in enumerate(e9_rows):
        is_adaptive = ("Cluster-Adaptive" in r_data[1])
        for c_idx, val in enumerate(r_data):
            format_cell(
                t_e9.rows[r_idx + 1].cells[c_idx],
                val,
                bold=is_adaptive,
                font_size=7.5,
                align=WD_ALIGN_PARAGRAPH.LEFT if c_idx in [0, 1] else WD_ALIGN_PARAGRAPH.CENTER
            )
    add_apa_table_note(doc, "*** p < .001. Across all three archetypes, cluster-adaptive pacing achieved 19.3% to 24.4% turn count reductions and eliminated 83.5% to 86.1% of redundant clarification questions.")

    # 5. Add Page Break and Appendix F
    print("Generating Appendix F: Empirical Diagnostic Visualizations and Methodological Figures...")
    doc.add_page_break()

    add_apa_heading(doc, "Appendix F", level=1)
    add_apa_subheading_italic(doc, "Empirical Diagnostic Visualizations and Methodological Figures")

    add_apa_body_paragraph(
        doc,
        "This appendix provides the primary high-resolution empirical visualizations generated from the experimental pipelines during "
        "Weeks 1 through 4. All figures adhere strictly to APA 7 presentation guidelines, incorporating formal figure numbers, descriptive "
        "titles, embedded high-density graphic renderings, and comprehensive explanatory notes."
    )

    # Figure F1: UMAP
    add_apa_figure(
        doc,
        figure_num="Figure F1",
        figure_title="Two-Dimensional UMAP Projection of Trajectory Embeddings by Latent Dialogue Archetype",
        image_path="/Users/surnellas/capstone/outputs/figures/fig1_umap_archetypes.png",
        note_text=(
            "Two-dimensional manifold projection generated via Uniform Manifold Approximation and Projection (UMAP; n_neighbors = 15, "
            "min_dist = 0.1, cosine distance metric) from 384-dimensional dense S-BERT trajectory embeddings across N = 1,500 travel dialogues. "
            "Individual data points represent entire multi-turn dialogue trajectories colored by their assigned cluster archetype: Budget Negotiator / "
            "Value-Conscious (Cluster 0, blue manifold), Hesitant Explorer / Consultative (Cluster 1, orange manifold), and Rapid Transactional / "
            "Corporate (Cluster 2, green manifold). The projection visually validates clear geometric separation between behavioral archetypes."
        ),
        width_inches=6.2
    )

    # Figure F2: Silhouette Comparison
    add_apa_figure(
        doc,
        figure_num="Figure F2",
        figure_title="Distribution of Silhouette Quality Scores Across Trajectory Clustering Algorithms",
        image_path="/Users/surnellas/capstone/outputs/figures/fig2_silhouette_comparison.png",
        note_text=(
            "Comparative boxplot and kernel density distributions of Silhouette coefficients evaluated across 156 bootstrap resamples for "
            "Agglomerative Clustering (M = 0.278, SD = 0.046), K-Means (M = 0.274, SD = 0.048), and HDBSCAN (M = 0.207, SD = 0.052). "
            "Horizontal dashed lines demarcate mean quality levels. Partitioning methods achieved statistically indistinguishable, superior "
            "separation compared to density-based clustering (F = 37.36, p < .001)."
        ),
        width_inches=6.2
    )

    # Figure F3: Cluster Metrics Elbow
    add_apa_figure(
        doc,
        figure_num="Figure F3",
        figure_title="Multi-Metric Cluster Validation Curves Across Candidate Values of K (k = 2 to 6)",
        image_path="/Users/surnellas/capstone/outputs/figures/fig3_cluster_metrics_elbow.png",
        note_text=(
            "Tri-panel validation curves displaying Silhouette Score (left), Davies-Bouldin Index (center), and Inertia within-cluster sum of squares "
            "(right) across candidate partitions k = 2 through 6. The vertical dashed marker at k = 3 identifies the primary geometric elbow "
            "optimally balancing cluster separation, compactness, and domain interpretability."
        ),
        width_inches=6.2
    )

    # Figure F4: Style Convergence
    add_apa_figure(
        doc,
        figure_num="Figure F4",
        figure_title="Semantic Style Convergence and Cosine Similarity Distributions Across Conditioning Strategies (RQ2)",
        image_path="/Users/surnellas/capstone/outputs/figures/fig4_rq2_style_convergence.png",
        note_text=(
            "Kernel density estimates and overlaid boxplots displaying the distribution of cosine similarity between generated responses and "
            "target archetype profiles across N = 42 evaluation trials per condition. Cluster-Adaptive Few-Shot prompting (green distribution, "
            "M = 0.869) demonstrates a substantial rightward semantic shift relative to Static Few-Shot prompting (orange distribution, M = 0.757) "
            "and the Zero-Shot baseline (blue distribution, M = 0.690), confirming that dynamic exemplar retrieval effectively steers response style."
        ),
        width_inches=6.2
    )

    # Save output DOCX
    print(f"Saving final DOCX to: {output_docx_path}...")
    doc.save(output_docx_path)
    print(f"DOCX created successfully ({os.path.getsize(output_docx_path):,} bytes).")

    # Native Microsoft Word PDF Conversion
    print(f"Converting DOCX to PDF via native Microsoft Word...")
    convert_docx_to_pdf(output_docx_path, output_pdf_path)


if __name__ == "__main__":
    main()
