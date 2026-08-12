import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from typing import Dict, List, Any
from config import RESPONSIBLE_AI_NOTICE, SCORE_EXPLANATION

def generate_pdf_report(
    filename: str,
    categorized_skills: Dict[str, List[str]],
    top_recommendations: List[Dict[str, Any]],
    target_role_analysis: Dict[str, Any],
    roadmap: List[Dict[str, str]]
) -> bytes:
    """
    Generates a professional PDF analysis report using ReportLab.
    Returns the PDF content as a bytes object.
    """
    buffer = io.BytesIO()
    
    # Page setup
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    # Modifying existing styles or adding unique names to avoid collisions
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#1A365D"),
        alignment=0, # Left-aligned
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#4A5568"),
        spaceAfter=25
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2D3748"),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2D3748")
    )
    
    bullet_style = ParagraphStyle(
        'BulletItem',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2D3748"),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    notice_style = ParagraphStyle(
        'DisclaimerNotice',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=12,
        textColor=colors.HexColor("#718096")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.white
    )

    table_body_style = ParagraphStyle(
        'TableBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#2D3748")
    )

    story = []
    
    # 1. Header Block
    story.append(Paragraph("AI Resume Analysis Report", title_style))
    story.append(Paragraph(
        f"Analyzed File: <b>{filename}</b> &nbsp;&nbsp;|&nbsp;&nbsp; Date: <b>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</b>",
        subtitle_style
    ))
    
    # 2. Responsible AI Alert
    notice_text = f"<b>Responsible AI Notice:</b> {RESPONSIBLE_AI_NOTICE}"
    notice_table = Table([[Paragraph(notice_text, table_body_style)]], colWidths=[530])
    notice_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EDF2F7")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(notice_table)
    story.append(Spacer(1, 15))
    
    # 3. Top Recommended Roles
    story.append(Paragraph("Top Recommended Roles", h1_style))
    
    rec_data = [[
        Paragraph("Rank", table_header_style),
        Paragraph("Job Role", table_header_style),
        Paragraph("Match Score", table_header_style),
        Paragraph("Match Category", table_header_style)
    ]]
    
    for idx, rec in enumerate(top_recommendations[:3], 1):
        score = rec['combined_score']
        match_cat = "Strong" if score >= 80 else ("Good" if score >= 60 else ("Moderate" if score >= 40 else "Low"))
        rec_data.append([
            Paragraph(str(idx), table_body_style),
            Paragraph(rec['role_name'], table_body_style),
            Paragraph(f"<b>{score}%</b>", table_body_style),
            Paragraph(f"{match_cat} Match", table_body_style)
        ])
        
    rec_table = Table(rec_data, colWidths=[40, 240, 100, 150])
    rec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('TOPPADDING', (0,0), (-1,0), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(rec_table)
    story.append(Spacer(1, 15))
    
    # 4. Extracted Skills Summary
    story.append(Paragraph("Detected Skills by Category", h1_style))
    if not categorized_skills:
        story.append(Paragraph("No technical skills could be extracted from this resume.", body_style))
    else:
        for category, skill_list in categorized_skills.items():
            skills_str = ", ".join(skill_list)
            story.append(Paragraph(f"• <b>{category}:</b> {skills_str}", bullet_style))
            
    story.append(Spacer(1, 15))
    
    # Page Break for clean Target Analysis section
    story.append(PageBreak())
    
    # 5. Selected Target Role Analysis
    role_name = target_role_analysis["role_name"]
    score = target_role_analysis["combined_score"]
    skill_score = target_role_analysis["skill_score"]
    tfidf_score = target_role_analysis["tfidf_score"]
    
    story.append(Paragraph(f"Target Role Analysis: {role_name}", h1_style))
    
    # Match Scores Grid Table
    score_data = [
        [
            Paragraph("Combined Score", table_header_style),
            Paragraph("Skill Match Score (70% Wt)", table_header_style),
            Paragraph("TF-IDF Semantic Score (30% Wt)", table_header_style)
        ],
        [
            Paragraph(f"<font size=14><b>{score}%</b></font>", table_body_style),
            Paragraph(f"{skill_score}%", table_body_style),
            Paragraph(f"{tfidf_score}%", table_body_style)
        ]
    ]
    score_table = Table(score_data, colWidths=[176, 177, 177])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2D3748")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(score_table)
    
    explanation_text = f"<i>Note: {SCORE_EXPLANATION}</i>"
    story.append(Spacer(1, 5))
    story.append(Paragraph(explanation_text, notice_style))
    story.append(Spacer(1, 15))
    
    # Skill Gaps
    story.append(Paragraph("Skill Gap Analysis", h2_style))
    
    matched_req = target_role_analysis["matched_required_skills"]
    missing_req = target_role_analysis["missing_required_skills"]
    
    matched_text = ", ".join(matched_req) if matched_req else "None detected"
    missing_text = ", ".join(missing_req) if missing_req else "None missing!"
    
    gap_data = [
        [Paragraph("<b>Matched Required Skills:</b>", table_body_style), Paragraph(matched_text, table_body_style)],
        [Paragraph("<b>Missing Required Skills:</b>", table_body_style), Paragraph(f"<font color='red'>{missing_text}</font>", table_body_style)]
    ]
    gap_table = Table(gap_data, colWidths=[150, 380])
    gap_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#EDF2F7")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(gap_table)
    story.append(Spacer(1, 15))
    
    # 6. Learning Roadmap
    story.append(Paragraph("Personalized Learning Roadmap", h1_style))
    if not roadmap or (len(roadmap) == 1 and "Continuous Enhancement" in roadmap[0]["topic"]):
        story.append(Paragraph(roadmap[0]["activity"], body_style))
    else:
        roadmap_data = [[
            Paragraph("Week", table_header_style),
            Paragraph("Topic", table_header_style),
            Paragraph("Recommended Learning Activity", table_header_style)
        ]]
        for rm in roadmap:
            roadmap_data.append([
                Paragraph(f"<b>{rm['week']}</b>", table_body_style),
                Paragraph(rm['topic'], table_body_style),
                Paragraph(rm['activity'], table_body_style)
            ])
        rm_table = Table(roadmap_data, colWidths=[60, 130, 340])
        rm_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#4A5568")),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
            ('PADDING', (0,0), (-1,-1), 6),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(rm_table)
        
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Disclaimer:</b> Match scores are statistical estimates for educational guidance and do not represent recruiter decisions.", notice_style))
    
    # Build document
    doc.build(story)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
