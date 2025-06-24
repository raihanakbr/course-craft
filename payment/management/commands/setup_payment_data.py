from django.core.management.base import BaseCommand
from decimal import Decimal
from payment.models import SubscriptionPlan, PaymentMethod


class Command(BaseCommand):
    help = 'Populate initial data for subscription plans and payment methods'

    def handle(self, *args, **options):
        self.stdout.write('Setting up initial data...')
        
        # Create subscription plans
        plans = [
            {
                'id': 1,
                'name': '1 Bulan',
                'display_name': 'Paket 1 Bulan',
                'duration_months': 1,
                'original_price': Decimal('300000'),
                'discounted_price': Decimal('125000'),
                'discount_percentage': 58,
                'features': [
                    'Akses semua kursus premium',
                    'Download materi offline',
                    'Sertifikat resmi',
                    'Live session dengan mentor',
                    'Forum diskusi eksklusif'
                ],
                'is_popular': False,
                'savings': Decimal('175000'),
                'badge': ''
            },
            {
                'id': 2,
                'name': '3 Bulan',
                'display_name': 'Paket 3 Bulan',
                'duration_months': 3,
                'original_price': Decimal('900000'),
                'discounted_price': Decimal('375000'),
                'discount_percentage': 58,
                'features': [
                    'Semua fitur paket 1 bulan',
                    'Priority support 24/7',
                    'Akses early access kursus baru',
                    'Personal learning consultant',
                    'Career guidance session',
                    'Portfolio review gratis'
                ],
                'is_popular': True,
                'savings': Decimal('525000'),
                'badge': 'Penawaran Terbaik'
            },
            {
                'id': 3,
                'name': '6 Bulan',
                'display_name': 'Paket 6 Bulan',
                'duration_months': 6,
                'original_price': Decimal('1800000'),
                'discounted_price': Decimal('750000'),
                'discount_percentage': 58,
                'features': [
                    'Semua fitur paket 3 bulan',
                    'Dedicated career mentor',
                    'Job placement assistance',
                    'Industry networking events',
                    'Advanced certification',
                    '1-on-1 monthly review',
                    'Lifetime community access'
                ],
                'is_popular': False,
                'savings': Decimal('1050000'),
                'badge': ''
            }
        ]
        
        for plan_data in plans:
            plan, created = SubscriptionPlan.objects.get_or_create(
                id=plan_data['id'],
                defaults=plan_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created plan: {plan.display_name}')
                )
            else:
                self.stdout.write(f'Plan already exists: {plan.display_name}')
        
        # Create payment methods
        payment_methods = [
            {
                'code': 'BCA',
                'name': 'Bank BCA',
                'payment_type': 'VIRTUAL_ACCOUNT',
                'icon': 'fas fa-university',
                'is_active': True,
                'min_amount': Decimal('10000'),
                'max_amount': None
            },
            {
                'code': 'BNI',
                'name': 'Bank BNI',
                'payment_type': 'VIRTUAL_ACCOUNT',
                'icon': 'fas fa-university',
                'is_active': True,
                'min_amount': Decimal('10000'),
                'max_amount': None
            },
            {
                'code': 'BRI',
                'name': 'Bank BRI',
                'payment_type': 'VIRTUAL_ACCOUNT',
                'icon': 'fas fa-university',
                'is_active': True,
                'min_amount': Decimal('10000'),
                'max_amount': None
            },
            {
                'code': 'MANDIRI',
                'name': 'Bank Mandiri',
                'payment_type': 'VIRTUAL_ACCOUNT',
                'icon': 'fas fa-university',
                'is_active': True,
                'min_amount': Decimal('10000'),
                'max_amount': None
            },
            {
                'code': 'PERMATA',
                'name': 'Bank Permata',
                'payment_type': 'VIRTUAL_ACCOUNT',
                'icon': 'fas fa-university',
                'is_active': True,
                'min_amount': Decimal('10000'),
                'max_amount': None
            },
            {
                'code': 'OVO',
                'name': 'OVO',
                'payment_type': 'EWALLET',
                'icon': 'fas fa-mobile-alt',
                'is_active': True,
                'min_amount': Decimal('10000'),
                'max_amount': Decimal('2000000')
            },
            {
                'code': 'DANA',
                'name': 'DANA',
                'payment_type': 'EWALLET',
                'icon': 'fas fa-mobile-alt',
                'is_active': True,
                'min_amount': Decimal('10000'),
                'max_amount': Decimal('2000000')
            },
            {
                'code': 'LINKAJA',
                'name': 'LinkAja',
                'payment_type': 'EWALLET',
                'icon': 'fas fa-mobile-alt',
                'is_active': True,
                'min_amount': Decimal('10000'),
                'max_amount': Decimal('2000000')
            },
            {
                'code': 'SHOPEEPAY',
                'name': 'ShopeePay',
                'payment_type': 'EWALLET',
                'icon': 'fas fa-mobile-alt',
                'is_active': True,
                'min_amount': Decimal('10000'),
                'max_amount': Decimal('2000000')
            },
            {
                'code': 'GOPAY',
                'name': 'GoPay',
                'payment_type': 'EWALLET',
                'icon': 'fas fa-mobile-alt',
                'is_active': True,
                'min_amount': Decimal('10000'),
                'max_amount': Decimal('2000000')
            },
            {
                'code': 'ALFAMART',
                'name': 'Alfamart',
                'payment_type': 'RETAIL_OUTLET',
                'icon': 'fas fa-store',
                'is_active': True,
                'min_amount': Decimal('10000'),
                'max_amount': Decimal('2500000')
            },
            {
                'code': 'INDOMARET',
                'name': 'Indomaret',
                'payment_type': 'RETAIL_OUTLET',
                'icon': 'fas fa-store',
                'is_active': True,
                'min_amount': Decimal('10000'),
                'max_amount': Decimal('2500000')
            },
            {
                'code': 'CREDIT_CARD',
                'name': 'Kartu Kredit/Debit',
                'payment_type': 'CREDIT_CARD',
                'icon': 'fas fa-credit-card',
                'is_active': True,
                'min_amount': Decimal('10000'),
                'max_amount': None
            },
            {
                'code': 'QRIS',
                'name': 'QRIS',
                'payment_type': 'QR_CODE',
                'icon': 'fas fa-qrcode',
                'is_active': True,
                'min_amount': Decimal('1500'),
                'max_amount': Decimal('2000000')
            }
        ]
        
        for method_data in payment_methods:
            method, created = PaymentMethod.objects.get_or_create(
                code=method_data['code'],
                defaults=method_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created payment method: {method.name}')
                )
            else:
                self.stdout.write(f'Payment method already exists: {method.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated initial data!')
        )
