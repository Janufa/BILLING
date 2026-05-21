"""
Email Notification Utility.
"""
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .pdf_generator import generate_bill_pdf
from django.utils import timezone


def send_bill_email(bill):
    """
    Send bill via email to the student.
    
    Args:
        bill: Bill model instance
    
    Returns:
        Number of messages sent (1 if successful, 0 if failed)
    """
    try:
        student = bill.enrollment.student
        course = bill.enrollment.course
        
        # Prepare email context
        context = {
            'student_name': student.user.get_full_name(),
            'student_id': student.student_id,
            'course_name': course.title,
            'course_code': course.code,
            'bill_number': bill.bill_number,
            'bill_date': bill.bill_date.strftime('%Y-%m-%d'),
            'due_date': bill.due_date.strftime('%Y-%m-%d'),
            'amount': f"${bill.amount:,.2f}",
            'tax': f"${bill.tax:,.2f}",
            'total_amount': f"${bill.total_amount:,.2f}",
            'status': bill.get_status_display(),
        }
        
        # Render HTML email template
        html_content = render_to_string('emails/bill.html', context)
        text_content = strip_tags(html_content)
        
        # Create email
        email = EmailMultiAlternatives(
            subject=f'Bill {bill.bill_number} - {course.title}',
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[student.user.email],
        )
        
        # Attach HTML version
        email.attach_alternative(html_content, "text/html")
        
        # Generate and attach PDF if not already generated
        if not bill.pdf_file:
            generate_bill_pdf(bill)
            bill.save()
        
        # Attach PDF file
        if bill.pdf_file:
            pdf_file = bill.pdf_file.open('rb')
            email.attach(
                f'bill_{bill.bill_number}.pdf',
                pdf_file.read(),
                'application/pdf'
            )
            pdf_file.close()
        
        # Send email
        sent = email.send(fail_silently=False)
        
        # Update bill email status
        if sent:
            bill.is_email_sent = True
            bill.email_sent_date = timezone.now()
            bill.save(update_fields=['is_email_sent', 'email_sent_date'])
        
        return sent
    
    except Exception as e:
        print(f"Error sending bill email: {str(e)}")
        return 0


def send_enrollment_confirmation_email(enrollment):
    """
    Send enrollment confirmation email to the student.
    
    Args:
        enrollment: Enrollment model instance
    
    Returns:
        Number of messages sent
    """
    try:
        student = enrollment.student
        course = enrollment.course
        
        context = {
            'student_name': student.user.get_full_name(),
            'course_name': course.title,
            'course_code': course.code,
            'amount': f"${enrollment.amount:,.2f}",
            'enrollment_date': enrollment.enrollment_date.strftime('%Y-%m-%d'),
        }
        
        # For now, just use basic text email
        message = f"""
        Dear {student.user.get_full_name()},
        
        Your enrollment in {course.title} ({course.code}) has been confirmed.
        
        Enrollment Details:
        - Student ID: {student.student_id}
        - Course: {course.title}
        - Amount: ${enrollment.amount:,.2f}
        - Enrollment Date: {enrollment.enrollment_date.strftime('%Y-%m-%d')}
        
        Please proceed to payment to complete your registration.
        
        Thank you,
        Billing System
        """
        
        email = EmailMultiAlternatives(
            subject=f'Enrollment Confirmation - {course.title}',
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[student.user.email],
        )
        
        return email.send(fail_silently=False)
    
    except Exception as e:
        print(f"Error sending enrollment confirmation email: {str(e)}")
        return 0


def send_payment_confirmation_email(payment):
    """
    Send payment confirmation email to the student.
    
    Args:
        payment: Payment model instance
    
    Returns:
        Number of messages sent
    """
    try:
        enrollment = payment.enrollment
        student = enrollment.student
        course = enrollment.course
        
        message = f"""
        Dear {student.user.get_full_name()},
        
        Your payment has been successfully processed.
        
        Payment Details:
        - Transaction ID: {payment.transaction_id}
        - Course: {course.title}
        - Amount: ${payment.amount:,.2f}
        - Payment Method: {payment.get_payment_method_display()}
        - Date: {payment.payment_date.strftime('%Y-%m-%d %H:%M:%S')}
        
        Your bill has been generated and will be sent to you separately.
        
        Thank you,
        Billing System
        """
        
        email = EmailMultiAlternatives(
            subject=f'Payment Confirmation - Transaction ID: {payment.transaction_id}',
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[student.user.email],
        )
        
        return email.send(fail_silently=False)
    
    except Exception as e:
        print(f"Error sending payment confirmation email: {str(e)}")
        return 0
