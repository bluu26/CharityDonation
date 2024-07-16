from django.contrib import admin
from django.urls import path, include

from DonationCore import views

urlpatterns = [
    path('home/', views.LandingPageView.as_view(), name='home'),
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('register/', views.RegisterPageView.as_view(), name='register'),
    path('adddonation/', views.AddDonationPageView.as_view(), name='adddonation'),
]
