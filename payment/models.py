from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
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

class UserSubscription(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    
    # Auto-renewal settings
    auto_renewal = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.subscription_plan.display_name} ({self.status})"
    
    @property
    def is_active(self):
        return self.status == 'ACTIVE' and self.end_date > timezone.now()
    
    @property
    def days_remaining(self):
        if self.is_active:
            delta = self.end_date - timezone.now()
            return max(0, delta.days)
        return 0
    
    def activate_subscription(self):
        """Activate the subscription"""
        self.status = 'ACTIVE'
        self.start_date = timezone.now()
        # Calculate end date based on plan duration
        from dateutil.relativedelta import relativedelta
        self.end_date = self.start_date + relativedelta(months=self.subscription_plan.duration_months)
        self.save()
    
    def expire_subscription(self):
        """Expire the subscription"""
        self.status = 'EXPIRED'
        self.save()
    
    def cancel_subscription(self):
        """Cancel the subscription"""
        self.status = 'CANCELLED'
        self.save()
