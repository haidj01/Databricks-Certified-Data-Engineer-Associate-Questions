#!/usr/bin/env python3
"""
Convert Markdown to PDF using reportlab
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
import re

def parse_markdown_to_pdf(md_file, pdf_file):
    """Convert markdown file to PDF"""

    # Read markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Create PDF
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )

    # Container for the 'Flowable' objects
    elements = []

    # Define styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )

    h3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor('#7f8c8d'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )

    h4_style = ParagraphStyle(
        'CustomH4',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#95a5a6'),
        spaceAfter=6,
        spaceBefore=6,
        fontName='Helvetica-Bold'
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=9,
        textColor=colors.HexColor('#c7254e'),
        backColor=colors.HexColor('#f9f2f4'),
        fontName='Courier'
    )

    # Split content into lines
    lines = content.split('\n')

    in_table = False
    table_data = []

    for i, line in enumerate(lines):
        line = line.rstrip()

        # Skip empty lines in tables
        if in_table and not line.strip():
            continue

        # Headers
        if line.startswith('# ') and not line.startswith('## '):
            text = line[2:].strip()
            if i == 0:  # First heading as title
                elements.append(Paragraph(text, title_style))
            else:
                elements.append(Spacer(1, 0.2*inch))
                elements.append(Paragraph(text, h1_style))
        elif line.startswith('## '):
            text = line[3:].strip()
            elements.append(Spacer(1, 0.15*inch))
            elements.append(Paragraph(text, h2_style))
        elif line.startswith('### '):
            text = line[4:].strip()
            elements.append(Paragraph(text, h3_style))
        elif line.startswith('#### '):
            text = line[5:].strip()
            elements.append(Paragraph(text, h4_style))

        # Horizontal rule
        elif line.strip() == '---':
            elements.append(Spacer(1, 0.1*inch))
            elements.append(PageBreak())

        # Table detection
        elif '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_data = []

            # Skip separator line
            if re.match(r'^\|[\s\-:]+\|', line):
                continue

            # Parse table row
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            table_data.append(cells)

        # End of table
        elif in_table and not line.strip().startswith('|'):
            if table_data:
                # Create table
                t = Table(table_data)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]))
                elements.append(t)
                elements.append(Spacer(1, 0.2*inch))
            in_table = False
            table_data = []

        # Bullet points
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            text = line.strip()[2:]
            # Handle bold text **text**
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            # Handle code `text`
            text = re.sub(r'`(.*?)`', r'<font face="Courier" color="#c7254e">\1</font>', text)
            elements.append(Paragraph(f"• {text}", normal_style))

        # Regular paragraphs
        elif line.strip():
            text = line.strip()
            # Handle bold text **text**
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            # Handle code `text`
            text = re.sub(r'`(.*?)`', r'<font face="Courier" color="#c7254e" backColor="#f9f2f4">\1</font>', text)
            elements.append(Paragraph(text, normal_style))

        # Empty lines
        else:
            elements.append(Spacer(1, 0.1*inch))

    # Build PDF
    doc.build(elements)
    print(f"PDF created successfully: {pdf_file}")

if __name__ == '__main__':
    md_file = 'Notes/Databricks_Data_Engineering_Concepts.md'
    pdf_file = 'Notes/Databricks_Data_Engineering_Concepts.pdf'

    parse_markdown_to_pdf(md_file, pdf_file)
