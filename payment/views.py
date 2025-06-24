from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.conf import settings
from django.db import models
from datetime import datetime, timedelta
import json
import uuid
import xendit
from xendit.apis import InvoiceApi
from xendit.invoice.model.create_invoice_request import CreateInvoiceRequest
from xendit.invoice.model.customer_object import CustomerObject
from xendit.invoice.model.notification_preference import NotificationPreference
from xendit.invoice.model.notification_channel import NotificationChannel
from xendit.invoice.model.invoice_item import InvoiceItem
from pprint import pprint
from .models import SubscriptionPlan, PaymentMethod, Invoice

# Initialize Xendit
xendit.set_api_key(getattr(settings, 'XENDIT_SECRET_KEY', 'your-xendit-secret-key'))

def package_selection(request, plan_id):
    """Display selected package with available payment methods"""
    try:
        # Get the subscription plan by ID
        plan = get_object_or_404(SubscriptionPlan, id=plan_id)
        
        # Get active payment methods
        payment_methods = PaymentMethod.objects.filter(
            is_active=True,
            min_amount__lte=plan.discounted_price
        )
        if plan.discounted_price and payment_methods.exists():
            payment_methods = payment_methods.filter(
                models.Q(max_amount__isnull=True) | 
                models.Q(max_amount__gte=plan.discounted_price)
            )
        
        context = {
            'plan': plan,
            'payment_methods': payment_methods,
            'app_name': 'CourseCraft'
        }
        
        return render(request, 'payment/package_selection.html', context)
        
    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {str(e)}')
        return redirect('pricing')

def create_invoice_view(request):
    print("Creating invoice view")
    """Create Xendit invoice for selected package and payment method"""
    if request.method != 'POST':
        return HttpResponseBadRequest('Method not allowed')
    
    try:
        # Get form data
        plan_id = request.POST.get('plan_id')
        payment_method_id = request.POST.get('payment_method_id')
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone', '')
        
        # Validate required fields
        if not all([plan_id, payment_method_id, customer_name, customer_email]):
            messages.error(request, 'Semua field wajib diisi.')
            return redirect('payment:package_selection', plan_id=plan_id)
        
        # Get plan and payment method
        plan = get_object_or_404(SubscriptionPlan, id=plan_id)
        payment_method = get_object_or_404(PaymentMethod, id=payment_method_id)
        
        # Generate unique external ID
        external_id = f"coursecraft-{uuid.uuid4().hex[:8]}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create invoice record in database
        invoice = Invoice.objects.create(
            external_id=external_id,
            subscription_plan=plan,
            payment_method=payment_method,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            amount=plan.discounted_price,
            description=f"CourseCraft {plan.display_name} Subscription",
            success_redirect_url=request.build_absolute_uri('/payment/success/'),
            failure_redirect_url=request.build_absolute_uri('/payment/failure/')
        )
        
        # Create Xendit invoice
        api_client = xendit.ApiClient()
        api_instance = InvoiceApi(api_client)
        
        # Prepare invoice items
        invoice_items = [
            InvoiceItem(
                name=f"CourseCraft {plan.display_name}",
                price=float(plan.discounted_price),
                quantity=1.0,
                reference_id=str(plan.id),
                category="subscription"
            )
        ]
        
        # Create invoice request
        create_invoice_request = CreateInvoiceRequest(
            external_id=external_id,
            amount=float(invoice.amount),
            payer_email=customer_email,
            description=invoice.description,
            invoice_duration=float(24*60*60),  # 24 hours in seconds
            should_send_email=True,
            customer=CustomerObject(
                given_names=customer_name.split()[0] if customer_name.split() else customer_name,
                surname=' '.join(customer_name.split()[1:]) if len(customer_name.split()) > 1 else '',
                email=customer_email,
                mobile_number=customer_phone if customer_phone else None,
            ),
            success_redirect_url=invoice.success_redirect_url,
            failure_redirect_url=invoice.failure_redirect_url,
            payment_methods=[payment_method.code],
            currency=invoice.currency,
            items=invoice_items,
            customer_notification_preference=NotificationPreference(
                invoice_created=[NotificationChannel("email")],
                invoice_reminder=[NotificationChannel("email")],
                invoice_paid=[NotificationChannel("email")],
            )
        )
        
        # Call Xendit API
        api_response = api_instance.create_invoice(create_invoice_request)
        pprint(api_response)
        print(f"Xendit Invoice Created: {api_response.id} - {api_response.invoice_url}")
        
        # Update invoice with Xendit response
        invoice.xendit_invoice_id = api_response.id
        invoice.invoice_url = api_response.invoice_url
        invoice.save()
        
        # Redirect to invoice URL
        return redirect(api_response.invoice_url)
        
    except Exception as e:
        print(f"Error creating invoice: {str(e)}")
        messages.error(request, f'Gagal membuat invoice: {str(e)}')
        return redirect('payment:package_selection', plan_id=request.POST.get('plan_id', 1))

def payment_success(request):
    """Handle successful payment"""
    external_id = request.GET.get('external_id')
    invoice = None
    
    if external_id:
        try:
            invoice = Invoice.objects.get(external_id=external_id)
            invoice.status = 'PAID'
            invoice.paid_at = datetime.now()
            invoice.save()
        except Invoice.DoesNotExist:
            pass
    
    context = {
        'invoice': invoice,
        'app_name': 'CourseCraft'
    }
    
    return render(request, 'payment/success.html', context)

def payment_failure(request):
    """Handle failed payment"""
    external_id = request.GET.get('external_id')
    invoice = None
    
    if external_id:
        try:
            invoice = Invoice.objects.get(external_id=external_id)
        except Invoice.DoesNotExist:
            pass
    
    context = {
        'invoice': invoice,
        'app_name': 'CourseCraft'
    }
    
    return render(request, 'payment/failure.html', context)

@csrf_exempt
def webhook_handler(request):
    """Handle Xendit webhook callbacks"""
    print("Handling webhook callback")
    if request.method != 'POST':
        return HttpResponseBadRequest('Method not allowed')
    
    try:
        # Parse webhook data
        webhook_data = json.loads(request.body)
        print(f"Webhook data received: {webhook_data}")
        
        # Get webhook event type
        event_type = webhook_data.get('event_type', webhook_data.get('status'))
        external_id = webhook_data.get('external_id')
        
        if not external_id:
            print("No external_id found in webhook data")
            return JsonResponse({'status': 'error', 'message': 'No external_id'}, status=400)
        
        # Find invoice
        try:
            invoice = Invoice.objects.get(external_id=external_id)
            print(f"Found invoice: {invoice.id}")
        except Invoice.DoesNotExist:
            print(f"Invoice with external_id {external_id} not found")
            return JsonResponse({'status': 'error', 'message': 'Invoice not found'}, status=404)
        
        # Handle different webhook events
        if event_type in ['PAID', 'invoice.paid']:
            invoice.status = 'PAID'
            paid_at = webhook_data.get('paid_at')
            if paid_at:
                try:
                    # Handle different datetime formats
                    if paid_at.endswith('Z'):
                        paid_at = paid_at.replace('Z', '+00:00')
                    invoice.paid_at = datetime.fromisoformat(paid_at)
                except ValueError:
                    invoice.paid_at = datetime.now()
            else:
                invoice.paid_at = datetime.now()
            print(f"Invoice {invoice.id} marked as PAID")
            
        elif event_type in ['EXPIRED', 'invoice.expired']:
            invoice.status = 'EXPIRED'
            invoice.expired_at = datetime.now()
            print(f"Invoice {invoice.id} marked as EXPIRED")
            
        elif event_type in ['PENDING', 'invoice.created']:
            invoice.status = 'PENDING'
            print(f"Invoice {invoice.id} status updated to PENDING")
        
        # Save invoice
        invoice.save()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Webhook processed for invoice {invoice.id}'
        })
        
    except json.JSONDecodeError:
        print("Invalid JSON in webhook data")
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
