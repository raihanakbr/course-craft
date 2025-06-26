from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
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
from .models import SubscriptionPlan, PaymentMethod, Invoice, UserSubscription
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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

@login_required
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

@login_required
def create_invoice_view(request):
    print("Creating invoice view")
    """Create Xendit invoice for selected package and payment method"""
    if request.method != 'POST':
        return HttpResponseBadRequest('Method not allowed')
    
    try:
        # Get form data
        plan_id = request.POST.get('plan_id')
        payment_method_id = request.POST.get('payment_method_id')
        
        # Validate required fields
        if not all([plan_id, payment_method_id]):
            messages.error(request, 'Semua field wajib diisi.')
            return redirect('payment:package_selection', plan_id=plan_id)
        
        # Get plan and payment method
        plan = get_object_or_404(SubscriptionPlan, id=plan_id)
        payment_method = get_object_or_404(PaymentMethod, id=payment_method_id)
        
        # Use logged in user's data
        customer_name = f"{request.user.first_name} {request.user.last_name}".strip()
        if not customer_name:
            customer_name = request.user.username
        customer_email = request.user.email
        
        # Generate unique external ID
        external_id = f"coursecraft-{uuid.uuid4().hex[:8]}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create invoice record in database
        invoice = Invoice.objects.create(
            external_id=external_id,
            user=request.user,
            subscription_plan=plan,
            payment_method=payment_method,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone='',  # Not collected anymore
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
                mobile_number=None,  # Not collecting phone number anymore
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
    
    from pprint import pprint
    print("\n=== REQUEST DEBUG ===")
    print("GET params:")
    pprint(dict(request.GET))
    print("POST params:")
    pprint(dict(request.POST))
    print("Headers:")
    pprint({k: v for k, v in request.META.items() if k.startswith('HTTP_')})
    if request.body:
        print(f"Body: {request.body}")
    print("====================\n")
    
    if external_id:
        try:
            # Only fetch the invoice for display, don't modify status
            # Status updates should only happen via webhook with proper token validation
            invoice = Invoice.objects.get(external_id=external_id)
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
    """Handle Xendit webhook callbacks with token verification"""
    print("Handling webhook callback")
    if request.method != 'POST':
        return HttpResponseBadRequest('Method not allowed')
    
    try:
        # Verify webhook token
        callback_token = request.headers.get('X-CALLBACK-TOKEN')
        webhook_verification_token = getattr(settings, 'WEBHOOK_VERIFICATION_TOKEN', None)
        
        if not webhook_verification_token:
            print("WEBHOOK_VERIFICATION_TOKEN not configured in settings")
            return JsonResponse({'status': 'error', 'message': 'Webhook verification not configured'}, status=500)
        
        if callback_token != webhook_verification_token:
            print(f"Invalid webhook token. Expected: {webhook_verification_token}, Got: {callback_token}")
            return JsonResponse({'status': 'error', 'message': 'Invalid webhook token'}, status=401)
        
        # Parse webhook data
        webhook_data = json.loads(request.body)
        print(f"Webhook data received: {webhook_data}")
        
        # Get webhook event type and external_id
        event_type = webhook_data.get('status')  # Xendit uses 'status' field
        external_id = webhook_data.get('external_id')
        
        if not external_id:
            print("No external_id found in webhook data")
            return JsonResponse({'status': 'error', 'message': 'No external_id'}, status=400)
        
        # Find invoice
        try:
            invoice = Invoice.objects.get(external_id=external_id)
            print(f"Found invoice: {invoice.id} with current status: {invoice.status}")
        except Invoice.DoesNotExist:
            print(f"Invoice with external_id {external_id} not found")
            return JsonResponse({'status': 'error', 'message': 'Invoice not found'}, status=404)
        
        # Handle different webhook events
        if event_type == 'PENDING':
            print(f"Processing PENDING webhook for invoice {invoice.id}")
            invoice.status = 'PENDING'
            # Update xendit_invoice_id if not already set
            if not invoice.xendit_invoice_id and webhook_data.get('id'):
                invoice.xendit_invoice_id = webhook_data.get('id')
            print(f"Invoice {invoice.id} status updated to PENDING")
            
        elif event_type == 'PAID':
            print(f"Processing PAID webhook for invoice {invoice.id}")
            invoice.status = 'PAID'
            
            # Set paid_at timestamp
            paid_at = webhook_data.get('paid_at')
            if paid_at:
                try:
                    # Handle different datetime formats
                    if paid_at.endswith('Z'):
                        paid_at = paid_at.replace('Z', '+00:00')
                    invoice.paid_at = datetime.fromisoformat(paid_at)
                except ValueError:
                    invoice.paid_at = timezone.now()
            else:
                invoice.paid_at = timezone.now()
            
            print(f"Invoice {invoice.id} marked as PAID at {invoice.paid_at}")
            
            # Create or update user subscription
            if invoice.user:
                try:
                    # Calculate end_date based on payment date and plan duration
                    start_date = invoice.paid_at or timezone.now()
                    end_date = start_date + relativedelta(months=invoice.subscription_plan.duration_months)
                    
                    subscription, created = UserSubscription.objects.get_or_create(
                        user=invoice.user,
                        defaults={
                            'subscription_plan': invoice.subscription_plan,
                            'invoice': invoice,
                            'start_date': start_date,
                            'end_date': end_date,
                            'status': 'ACTIVE'
                        }
                    )
                    
                    if created:
                        print(f"New subscription created for user {invoice.user.username} from {start_date} to {end_date}")
                    elif subscription.status != 'ACTIVE':
                        # Update existing subscription plan and activate
                        subscription.subscription_plan = invoice.subscription_plan
                        subscription.invoice = invoice
                        subscription.start_date = start_date
                        subscription.end_date = end_date
                        subscription.status = 'ACTIVE'
                        subscription.save()
                        print(f"Subscription updated and activated for user {invoice.user.username} from {start_date} to {end_date}")
                    else:
                        print(f"User {invoice.user.username} already has active subscription")
                        
                except Exception as e:
                    print(f"Error creating/updating subscription: {str(e)}")
                    import traceback
                    traceback.print_exc()
            
        elif event_type == 'SETTLED':
            print(f"Processing SETTLED webhook for invoice {invoice.id}")
            # SETTLED is similar to PAID but indicates final settlement
            invoice.status = 'PAID'  # We use PAID status for settled invoices
            
            # Set paid_at timestamp if not already set
            if not invoice.paid_at:
                settled_at = webhook_data.get('settled_at', webhook_data.get('paid_at'))
                if settled_at:
                    try:
                        if settled_at.endswith('Z'):
                            settled_at = settled_at.replace('Z', '+00:00')
                        invoice.paid_at = datetime.fromisoformat(settled_at)
                    except ValueError:
                        invoice.paid_at = timezone.now()
                else:
                    invoice.paid_at = timezone.now()
            
            print(f"Invoice {invoice.id} marked as SETTLED/PAID at {invoice.paid_at}")
            
            # Ensure subscription is active (in case PAID webhook was missed)
            if invoice.user:
                try:
                    # Calculate end_date based on payment date and plan duration
                    start_date = invoice.paid_at or timezone.now()
                    end_date = start_date + relativedelta(months=invoice.subscription_plan.duration_months)
                    
                    subscription, created = UserSubscription.objects.get_or_create(
                        user=invoice.user,
                        defaults={
                            'subscription_plan': invoice.subscription_plan,
                            'invoice': invoice,
                            'start_date': start_date,
                            'end_date': end_date,
                            'status': 'ACTIVE'
                        }
                    )
                    
                    if created:
                        print(f"New subscription created for user {invoice.user.username} from {start_date} to {end_date}")
                    elif subscription.status != 'ACTIVE':
                        subscription.subscription_plan = invoice.subscription_plan
                        subscription.invoice = invoice
                        subscription.start_date = start_date
                        subscription.end_date = end_date
                        subscription.status = 'ACTIVE'
                        subscription.save()
                        print(f"Subscription updated and activated for user {invoice.user.username} from {start_date} to {end_date}")
                    else:
                        print(f"User {invoice.user.username} already has active subscription")
                        
                except Exception as e:
                    print(f"Error creating/updating subscription: {str(e)}")
                    import traceback
                    traceback.print_exc()
            
        elif event_type == 'EXPIRED':
            print(f"Processing EXPIRED webhook for invoice {invoice.id}")
            invoice.status = 'EXPIRED'
            
            # Set expired_at timestamp
            expired_at = webhook_data.get('expired_at')
            if expired_at:
                try:
                    if expired_at.endswith('Z'):
                        expired_at = expired_at.replace('Z', '+00:00')
                    invoice.expired_at = datetime.fromisoformat(expired_at)
                except ValueError:
                    invoice.expired_at = timezone.now()
            else:
                invoice.expired_at = timezone.now()
            
            print(f"Invoice {invoice.id} marked as EXPIRED at {invoice.expired_at}")
            
        else:
            print(f"Unhandled webhook event type: {event_type}")
            return JsonResponse({
                'status': 'warning',
                'message': f'Unhandled event type: {event_type}'
            })
        
        # Save invoice
        invoice.save()
        print(f"Invoice {invoice.id} saved with status: {invoice.status}")
        
        return JsonResponse({
            'status': 'success',
            'message': f'Webhook processed successfully for invoice {invoice.id}',
            'event_type': event_type,
            'invoice_status': invoice.status
        })
        
    except json.JSONDecodeError:
        print("Invalid JSON in webhook data")
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
