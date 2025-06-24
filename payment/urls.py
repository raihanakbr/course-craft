from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('package/<int:plan_id>/', views.package_selection, name='package_selection'),
    path('create-invoice/', views.create_invoice_view, name='create_invoice'),
    path('success/', views.payment_success, name='success'),
    path('failure/', views.payment_failure, name='failure'),
    path('webhook/', views.webhook_handler, name='webhook'),
]
