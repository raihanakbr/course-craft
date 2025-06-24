from django.db import models
from django.contrib.auth.models import User
import uuid

class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('1 Bulan', '1 Bulan'),
        ('3 Bulan', '3 Bulan'),
        ('6 Bulan', '6 Bulan'),
    ]
    
    name = models.CharField(max_length=50, choices=PLAN_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    duration_months = models.IntegerField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.IntegerField()
    features = models.JSONField(default=list)
    is_popular = models.BooleanField(default=False)
    savings = models.DecimalField(max_digits=10, decimal_places=2)
    badge = models.CharField(max_length=100, blank=True, default='')
    
    def __str__(self):
        return self.display_name

class PaymentMethod(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('VIRTUAL_ACCOUNT', 'Virtual Account'),
        ('EWALLET', 'E-Wallet'),
        ('RETAIL_OUTLET', 'Retail Outlet'),
        ('CREDIT_CARD', 'Credit Card'),
        ('QR_CODE', 'QR Code'),
    ]
    
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    icon = models.CharField(max_length=100)  # Icon class or URL
    is_active = models.BooleanField(default=True)
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('EXPIRED', 'Expired'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    external_id = models.CharField(max_length=100, unique=True)
    xendit_invoice_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    
    # Customer information
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)
    
    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='IDR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    description = models.TextField()
    
    # Xendit URLs
    invoice_url = models.URLField(null=True, blank=True)
    success_redirect_url = models.URLField(null=True, blank=True)
    failure_redirect_url = models.URLField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    expired_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Invoice {self.external_id} - {self.customer_name}"
