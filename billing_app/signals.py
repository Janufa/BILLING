"""
Django signals for billing app.
Handles automatic bill generation when payment is successful.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import Payment, Bill
from .utils.email_sender import send_bill_email


@receiver(post_save, sender=Payment)
def generate_bill_on_payment(sender, instance, created, **kwargs):
    """
    Signal handler to automatically generate bill when payment is completed.
    """
    
    if created and instance.status == 'completed':
        try:
            # Create bill for the enrollment
            bill, bill_created = Bill.objects.get_or_create(
                enrollment=instance.enrollment,
                defaults={
                    'amount': instance.amount,
                    'tax': (instance.amount * Decimal('0.05')).quantize(Decimal('0.01')),
                    'total_amount': (instance.amount * Decimal('1.05')).quantize(Decimal('0.01')),
                    'due_date': timezone.now() + timedelta(days=30),
                    'status': 'issued'
                }
            )
            
            if bill_created:
                # Send bill email
                try:
                    send_bill_email(bill)
                except Exception as e:
                    print(f"Error sending bill email: {str(e)}")
        
        except Exception as e:
            print(f"Error generating bill: {str(e)}")
