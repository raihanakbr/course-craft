from django.core.management.base import BaseCommand
from payment.models import SubscriptionPlan, PaymentMethod

class Command(BaseCommand):
    help = 'Populate database with subscription plans and payment methods'

    def handle(self, *args, **options):
        # Create subscription plans
        plans_data = [
            {
                'name': '1 Bulan',
                'display_name': 'Paket 1 Bulan',
                'duration_months': 1,
                'original_price': 300000,
                'discounted_price': 125000,
                'discount_percentage': 58,
                'features': [
                    'Akses semua kursus premium',
                    'Download materi offline',
                    'Sertifikat resmi',
                    'Live session dengan mentor',
                    'Forum diskusi eksklusif'
                ],
                'is_popular': False,
                'savings': 175000,
                'badge': ''
            },
            {
                'name': '3 Bulan',
                'display_name': 'Paket 3 Bulan',
                'duration_months': 3,
                'original_price': 900000,
                'discounted_price': 375000,
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
                'savings': 525000,
                'badge': 'Penawaran Terbaik'
            },
            {
                'name': '6 Bulan',
                'display_name': 'Paket 6 Bulan',
                'duration_months': 6,
                'original_price': 1800000,
                'discounted_price': 750000,
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
                'savings': 1050000,
                'badge': ''
            }
        ]

        for plan_data in plans_data:
            plan, created = SubscriptionPlan.objects.get_or_create(
                name=plan_data['name'],
                defaults=plan_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created plan "{plan.name}"')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Plan "{plan.name}" already exists')
                )

        # Create payment methods
        payment_methods_data = [
            {
                'code': 'BCA',
                'name': 'BCA Virtual Account',
                'payment_type': 'VIRTUAL_ACCOUNT',
                'icon': 'fab fa-cc-visa',
                'min_amount': 10000,
                'max_amount': 50000000
            },
            {
                'code': 'BNI',
                'name': 'BNI Virtual Account',
                'payment_type': 'VIRTUAL_ACCOUNT',
                'icon': 'fas fa-university',
                'min_amount': 10000,
                'max_amount': 50000000
            },
            {
                'code': 'BRI',
                'name': 'BRI Virtual Account',
                'payment_type': 'VIRTUAL_ACCOUNT',
                'icon': 'fas fa-university',
                'min_amount': 10000,
                'max_amount': 50000000
            },
            {
                'code': 'MANDIRI',
                'name': 'Mandiri Virtual Account',
                'payment_type': 'VIRTUAL_ACCOUNT',
                'icon': 'fas fa-university',
                'min_amount': 10000,
                'max_amount': 50000000
            },
            {
                'code': 'PERMATA',
                'name': 'Permata Virtual Account',
                'payment_type': 'VIRTUAL_ACCOUNT',
                'icon': 'fas fa-university',
                'min_amount': 10000,
                'max_amount': 50000000
            },
            {
                'code': 'OVO',
                'name': 'OVO',
                'payment_type': 'EWALLET',
                'icon': 'fas fa-mobile-alt',
                'min_amount': 10000,
                'max_amount': 10000000
            },
            {
                'code': 'DANA',
                'name': 'DANA',
                'payment_type': 'EWALLET',
                'icon': 'fas fa-mobile-alt',
                'min_amount': 10000,
                'max_amount': 10000000
            },
            {
                'code': 'LINKAJA',
                'name': 'LinkAja',
                'payment_type': 'EWALLET',
                'icon': 'fas fa-mobile-alt',
                'min_amount': 10000,
                'max_amount': 10000000
            },
            {
                'code': 'GOPAY',
                'name': 'GoPay',
                'payment_type': 'EWALLET',
                'icon': 'fas fa-mobile-alt',
                'min_amount': 10000,
                'max_amount': 10000000
            },
            {
                'code': 'SHOPEEPAY',
                'name': 'ShopeePay',
                'payment_type': 'EWALLET',
                'icon': 'fas fa-mobile-alt',
                'min_amount': 10000,
                'max_amount': 10000000
            },
            {
                'code': 'QRIS',
                'name': 'QRIS',
                'payment_type': 'QR_CODE',
                'icon': 'fas fa-qrcode',
                'min_amount': 1500,
                'max_amount': 10000000
            },
            {
                'code': 'INDOMARET',
                'name': 'Indomaret',
                'payment_type': 'RETAIL_OUTLET',
                'icon': 'fas fa-store',
                'min_amount': 10000,
                'max_amount': 5000000
            },
            {
                'code': 'ALFAMART',
                'name': 'Alfamart',
                'payment_type': 'RETAIL_OUTLET',
                'icon': 'fas fa-store',
                'min_amount': 10000,
                'max_amount': 5000000
            }
        ]

        for method_data in payment_methods_data:
            method, created = PaymentMethod.objects.get_or_create(
                code=method_data['code'],
                defaults=method_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created payment method "{method.name}"')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Payment method "{method.name}" already exists')
                )

        self.stdout.write(
            self.style.SUCCESS('Database population completed!')
        )
