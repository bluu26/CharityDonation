from django.contrib import admin
from django.urls import path, include

from DonationCore import views

urlpatterns = [
    path('home/', views.LandingPageView.as_view(), name='home'),
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterPageView.as_view(), name='register'),
    path('donation/', views.DonationPageView.as_view(), name='donation'),
]
