from django.shortcuts import render

def landing_page(request):
    """Landing page view for CourseCraft"""
    context = {
        'app_name': 'CourseCraft',
        'tagline': 'Master New Skills with Interactive Learning',
        'features': [
            {
                'icon': '🎯',
                'title': 'Personalized Learning Paths',
                'description': 'AI-powered recommendations tailored to your learning style and goals'
            },
            {
                'icon': '🚀',
                'title': 'Interactive Courses',
                'description': 'Hands-on projects and real-world challenges to accelerate your growth'
            },
            {
                'icon': '👥',
                'title': 'Expert Community',
                'description': 'Learn from industry professionals and connect with like-minded learners'
            },
            {
                'icon': '📊',
                'title': 'Progress Tracking',
                'description': 'Detailed analytics and insights to monitor your learning journey'
            }
        ]
    }
    return render(request, 'main/landing.html', context)

def pricing_page(request):
    """Pricing page view for CourseCraft subscription plans"""
    context = {
        'app_name': 'CourseCraft',
        'pricing_plans': [
            {
                'name': '1 Bulan',
                'duration': '1 Bulan',
                'original_price': 'Rp 300.000',
                'discounted_price': 'Rp 125.000',
                'discount_percentage': 58,
                'features': [
                    'Akses semua kursus premium',
                    'Download materi offline',
                    'Sertifikat resmi',
                    'Live session dengan mentor',
                    'Forum diskusi eksklusif'
                ],
                'popular': False,
                'savings': 'Rp 175.000'
            },
            {
                'name': '3 Bulan',
                'duration': '3 Bulan',
                'original_price': 'Rp 900.000',
                'discounted_price': 'Rp 375.000',
                'discount_percentage': 58,
                'features': [
                    'Semua fitur paket 1 bulan',
                    'Priority support 24/7',
                    'Akses early access kursus baru',
                    'Personal learning consultant',
                    'Career guidance session',
                    'Portfolio review gratis'
                ],
                'popular': True,
                'savings': 'Rp 525.000',
                'badge': 'Penawaran Terbaik'
            },
            {
                'name': '6 Bulan',
                'duration': '6 Bulan',
                'original_price': 'Rp 1.800.000',
                'discounted_price': 'Rp 750.000',
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
                'popular': False,
                'savings': 'Rp 1.050.000'
            }
        ]
    }
    return render(request, 'main/pricing.html', context)
