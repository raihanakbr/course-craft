from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('pricing/', views.pricing_page, name='pricing'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # Course URLs
    path('courses/', views.course_list, name='course_list'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path('course/<slug:slug>/enroll/', views.enroll_course, name='enroll_course'),
    path('course/<slug:course_slug>/video/<slug:video_slug>/', views.video_detail, name='video_detail'),
]
