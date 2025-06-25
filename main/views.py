from django.shortcuts import render
from payment.models import SubscriptionPlan

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
    # Get plans from database
    subscription_plans = SubscriptionPlan.objects.all().order_by('duration_months')
    
    # Convert to format expected by template
    pricing_plans = []
    for plan in subscription_plans:
        pricing_plans.append({
            'id': plan.id,  # This will be the UUID or database ID
            'name': plan.name,
            'duration': plan.name,
            'original_price': f'Rp {plan.original_price:,.0f}'.replace(',', '.'),
            'discounted_price': f'Rp {plan.discounted_price:,.0f}'.replace(',', '.'),
            'discount_percentage': plan.discount_percentage,
            'features': plan.features,
            'popular': plan.is_popular,
            'savings': f'Rp {plan.savings:,.0f}'.replace(',', '.'),
            'badge': plan.badge if plan.badge else ''
        })
    
    context = {
        'app_name': 'CourseCraft',
        'pricing_plans': pricing_plans
    }
    return render(request, 'main/pricing.html', context)
