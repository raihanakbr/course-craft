from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('pricing/', views.pricing_page, name='pricing'),
]
