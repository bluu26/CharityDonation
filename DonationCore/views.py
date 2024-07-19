from django.shortcuts import render
from django.views import View

from DonationCore.models import Donation


class LandingPageView(View):
    def get(self, request):
        donations = Donation.objects.all()
        return render(request, 'index.html', {'donations': donations})


class RegisterPageView(View):
    def get(self, request):
        return render(request, 'register.html')


class LoginPageView(View):
    def get(self, request):
        return render(request, 'login.html')


class AddDonationPageView(View):
    def get(self, request):
        return render(request, 'form.html')