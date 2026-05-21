"""
Payment Gateway Mock Implementation.
"""
import uuid
import random
from datetime import datetime


def process_mock_payment(amount):
    """
    Mock payment processing function.
    Simulates payment gateway response.
    
    Args:
        amount: Payment amount in decimal
    
    Returns:
        str: Transaction ID if payment is successful
    
    Raises:
        Exception: If payment fails
    """
    
    # Generate transaction ID
    transaction_id = f"TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8].upper()}"
    
    # Simulate payment processing (90% success rate)
    success_rate = random.random()
    
    if success_rate < 0.9:
        # Payment successful
        return transaction_id
    else:
        # Payment failed
        raise Exception("Payment processing failed. Please try again.")


def validate_card(card_number, expiry, cvv):
    """
    Validate credit card details (mock implementation).
    
    Args:
        card_number: Credit card number (string)
        expiry: Expiry date in MM/YY format
        cvv: CVV number
    
    Returns:
        bool: True if card is valid
    """
    
    # Basic validation
    if not card_number or len(card_number) < 13:
        raise ValueError("Invalid card number")
    
    if not expiry or len(expiry) != 5 or expiry[2] != '/':
        raise ValueError("Invalid expiry date format (use MM/YY)")
    
    if not cvv or len(cvv) < 3:
        raise ValueError("Invalid CVV")
    
    return True


def verify_payment_status(transaction_id):
    """
    Verify payment status from gateway (mock implementation).
    
    Args:
        transaction_id: Transaction ID to verify
    
    Returns:
        dict: Payment status information
    """
    
    return {
        'transaction_id': transaction_id,
        'status': 'completed',
        'timestamp': datetime.now().isoformat(),
    }


def refund_payment(transaction_id, amount):
    """
    Request refund for a payment (mock implementation).
    
    Args:
        transaction_id: Transaction ID to refund
        amount: Amount to refund
    
    Returns:
        str: Refund transaction ID
    """
    
    refund_id = f"REFUND-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8].upper()}"
    return refund_id


class StripePaymentGateway:
    """
    Stripe payment gateway integration (placeholder for future implementation).
    """
    
    def __init__(self, api_key):
        self.api_key = api_key
    
    def process_payment(self, amount, token):
        """Process payment via Stripe."""
        # TODO: Implement Stripe integration
        pass


class PayPalPaymentGateway:
    """
    PayPal payment gateway integration (placeholder for future implementation).
    """
    
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
    
    def process_payment(self, amount, payer_email):
        """Process payment via PayPal."""
        # TODO: Implement PayPal integration
        pass


class RazorpayPaymentGateway:
    """
    Razorpay payment gateway integration (placeholder for future implementation).
    """
    
    def __init__(self, key_id, key_secret):
        self.key_id = key_id
        self.key_secret = key_secret
    
    def process_payment(self, amount, customer_email):
        """Process payment via Razorpay."""
        # TODO: Implement Razorpay integration
        pass
