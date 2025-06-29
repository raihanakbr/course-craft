from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from payment.models import SubscriptionPlan
from .forms import CustomUserCreationForm
from payment.models import UserSubscription  # Import UserSubscription model
from .models import Category, Course, Video, UserProgress, CourseEnrollment

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

def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('landing')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Akun berhasil dibuat untuk {username}. Silakan login.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form': form,
        'app_name': 'CourseCraft'
    }
    return render(request, 'main/register.html', context)

def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('landing')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_page = request.GET.get('next', 'landing')
            return redirect(next_page)
        else:
            messages.error(request, 'Username atau password salah.')
    
    context = {
        'app_name': 'CourseCraft'
    }
    return render(request, 'main/login.html', context)

@login_required
def profile_view(request):
    """User profile view showing subscription status"""
    try:
        subscription = UserSubscription.objects.get(user=request.user)
    except UserSubscription.DoesNotExist:
        subscription = None
    
    context = {
        'app_name': 'CourseCraft',
        'subscription': subscription
    }
    return render(request, 'main/profile.html', context)

# Course Views
def course_list(request):
    """Display list of all published courses"""
    courses = Course.objects.filter(is_published=True).select_related('category')
    categories = Category.objects.filter(is_active=True)
    
    # Filter by category if specified
    category_filter = request.GET.get('category')
    if category_filter:
        courses = courses.filter(category__slug=category_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )
    
    context = {
        'courses': courses,
        'categories': categories,
        'current_category': category_filter,
        'search_query': search_query,
        'app_name': 'CourseCraft'
    }
    
    return render(request, 'main/course_list.html', context)

def course_detail(request, slug):
    """Display course detail with video list"""
    course = get_object_or_404(Course, slug=slug, is_published=True)
    videos = course.videos.filter(is_published=True).order_by('order')
    
    # Check if user has access to this course
    has_access = False
    user_enrollment = None
    user_subscription = None
    
    if request.user.is_authenticated:
        # Check if course is free or user has subscription
        if not course.is_premium:
            has_access = True
        else:
            try:
                user_subscription = UserSubscription.objects.get(user=request.user)
                if user_subscription.is_active:
                    has_access = True
            except UserSubscription.DoesNotExist:
                pass
        
        # Get enrollment info
        try:
            user_enrollment = CourseEnrollment.objects.get(user=request.user, course=course)
        except CourseEnrollment.DoesNotExist:
            pass
    
    # Get preview videos (always accessible)
    preview_videos = videos.filter(is_preview=True)
    
    context = {
        'course': course,
        'videos': videos,
        'preview_videos': preview_videos,
        'has_access': has_access,
        'user_enrollment': user_enrollment,
        'user_subscription': user_subscription,
        'app_name': 'CourseCraft'
    }
    
    return render(request, 'main/course_detail.html', context)

@login_required
def enroll_course(request, slug):
    """Enroll user in a course"""
    course = get_object_or_404(Course, slug=slug, is_published=True)
    
    # Check if course requires subscription
    if course.is_premium:
        try:
            user_subscription = UserSubscription.objects.get(user=request.user)
            if not user_subscription.is_active:
                messages.error(request, 'Anda memerlukan subscription aktif untuk mengakses course premium.')
                return redirect('pricing')
        except UserSubscription.DoesNotExist:
            messages.error(request, 'Anda memerlukan subscription untuk mengakses course premium.')
            return redirect('pricing')
    
    # Create enrollment
    enrollment, created = CourseEnrollment.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={'is_active': True}
    )
    
    if created:
        messages.success(request, f'Berhasil mendaftar ke course {course.title}!')
    else:
        messages.info(request, f'Anda sudah terdaftar di course {course.title}.')
    
    return redirect('course_detail', slug=course.slug)

@login_required
def video_detail(request, course_slug, video_slug):
    """Display video player and track progress"""
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    video = get_object_or_404(Video, course=course, slug=video_slug, is_published=True)
    
    # Handle POST requests for progress tracking
    if request.method == 'POST':
        if request.user.is_authenticated:
            import json
            try:
                data = json.loads(request.body)
                action = data.get('action')
                
                # Get or create user progress
                user_progress, created = UserProgress.objects.get_or_create(
                    user=request.user,
                    video=video,
                    course=course
                )
                
                if action == 'mark_completed':
                    user_progress.mark_completed()
                    return JsonResponse({'success': True, 'message': 'Video marked as completed'})
                
                elif action == 'update_progress':
                    watch_time = data.get('watch_time', 0)
                    percentage = data.get('percentage', 0)
                    
                    user_progress.watch_time_seconds = watch_time
                    user_progress.completion_percentage = min(percentage, 100)
                    
                    # Auto-complete if watched more than 90%
                    if percentage >= 90 and not user_progress.is_completed:
                        user_progress.mark_completed()
                    
                    user_progress.save()
                    return JsonResponse({'success': True, 'progress': percentage})
                
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'error': 'Invalid JSON'})
        
        return JsonResponse({'success': False, 'error': 'Authentication required'})
    
    # Check access function
    def user_has_video_access(user, target_video):
        """Check if user has access to a specific video"""
        if target_video.is_preview:
            return True
        elif not course.is_premium:
            return True
        elif user.is_authenticated:
            try:
                user_subscription = UserSubscription.objects.get(user=user)
                return user_subscription.is_active
            except UserSubscription.DoesNotExist:
                pass
        return False
    
    # Check access to current video
    has_access = user_has_video_access(request.user, video)
    
    if not has_access:
        messages.error(request, 'Anda tidak memiliki akses ke video ini.')
        return redirect('course_detail', slug=course.slug)
    
    # Get or create user progress
    user_progress = None
    if request.user.is_authenticated:
        user_progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            video=video,
            course=course
        )
    
    # Get all videos for navigation with access information
    course_videos = course.videos.filter(is_published=True).order_by('order')
    
    # Add access information to each video
    for course_video in course_videos:
        course_video.user_has_access = user_has_video_access(request.user, course_video)
    
    context = {
        'course': course,
        'video': video,
        'user_progress': user_progress,
        'course_videos': course_videos,
        'app_name': 'CourseCraft'
    }
    
    return render(request, 'main/video_detail.html', context)

@login_required
def my_courses(request):
    """Display user's enrolled courses"""
    enrollments = CourseEnrollment.objects.filter(
        user=request.user, 
        is_active=True
    ).select_related('course').order_by('-enrolled_at')
    
    context = {
        'enrollments': enrollments,
        'app_name': 'CourseCraft'
    }
    
    return render(request, 'main/my_courses.html', context)
