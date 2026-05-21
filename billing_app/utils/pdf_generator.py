"""
PDF Bill Generator Utility.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from io import BytesIO
from django.core.files.base import ContentFile
from datetime import datetime


def generate_bill_pdf(bill):
    """
    Generate a PDF bill for the given Bill instance.
    
    Args:
        bill: Bill model instance
    
    Returns:
        ContentFile object with PDF content
    """
    # Create PDF buffer
    buffer = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
    )
    
    # Container for PDF elements
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=30,
        alignment=1,  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=12,
    )
    
    # Title
    title = Paragraph("INVOICE", title_style)
    elements.append(title)
    
    # Header information
    student = bill.enrollment.student
    course = bill.enrollment.course
    
    header_data = [
        ['Bill Number:', bill.bill_number],
        ['Bill Date:', bill.bill_date.strftime('%Y-%m-%d')],
        ['Due Date:', bill.due_date.strftime('%Y-%m-%d')],
        ['Status:', bill.get_status_display()],
    ]
    
    header_table = Table(header_data, colWidths=[2*inch, 4*inch])
    header_table.setStyle(TableStyle([
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
        ('FONT', (1, 0), (1, -1), 'Helvetica', 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    
    elements.append(header_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Student Information
    elements.append(Paragraph("BILL TO", heading_style))
    
    student_info = [
        [f"Name:", student.user.get_full_name()],
        [f"Student ID:", student.student_id],
        [f"Email:", student.user.email],
        [f"Phone:", student.phone or 'N/A'],
        [f"Address:", student.address or 'N/A'],
        [f"City:", f"{student.city}, {student.state} {student.zipcode}"],
    ]
    
    student_table = Table(student_info, colWidths=[1.5*inch, 4.5*inch])
    student_table.setStyle(TableStyle([
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 9),
        ('FONT', (1, 0), (1, -1), 'Helvetica', 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    
    elements.append(student_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Course Information
    elements.append(Paragraph("COURSE DETAILS", heading_style))
    
    course_data = [
        ['Course Code:', course.code],
        ['Course Title:', course.title],
        ['Level:', course.get_level_display()],
        ['Duration:', f"{course.duration_weeks} weeks"],
        ['Instructor:', course.instructor],
    ]
    
    course_table = Table(course_data, colWidths=[2*inch, 4*inch])
    course_table.setStyle(TableStyle([
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
        ('FONT', (1, 0), (1, -1), 'Helvetica', 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    
    elements.append(course_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Bill Details
    elements.append(Paragraph("BILLING SUMMARY", heading_style))
    
    billing_data = [
        ['Description', 'Amount'],
        ['Course Fee', f"${bill.amount:,.2f}"],
        ['Tax (5%)', f"${bill.tax:,.2f}"],
        ['Total Amount Due', f"${bill.total_amount:,.2f}"],
    ]
    
    billing_table = Table(billing_data, colWidths=[4*inch, 2*inch])
    billing_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 12),
        ('FONT', (0, 1), (-1, -2), 'Helvetica', 10),
        ('FONT', (0, -1), (-1, -1), 'Helvetica-Bold', 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f0f7')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    
    elements.append(billing_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_text = Paragraph(
        f"<b>Payment Status:</b> {bill.get_status_display()}<br/>"
        f"<b>Generated on:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>"
        f"<i>Thank you for your enrollment!</i>",
        styles['Normal']
    )
    elements.append(footer_text)
    
    # Build PDF
    doc.build(elements)
    
    # Save PDF to bill
    pdf_content = buffer.getvalue()
    buffer.close()
    
    filename = f"bill_{bill.bill_number}.pdf"
    bill.pdf_file.save(
        filename,
        ContentFile(pdf_content),
        save=False
    )
    
    return pdf_content
