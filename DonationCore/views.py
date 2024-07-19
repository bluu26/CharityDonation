from django.db.models import Sum
from django.shortcuts import render
from django.views import View

from DonationCore.models import Donation


class LandingPageView(View):
    def get(self, request):
        total_quantity = Donation.objects.aggregate(total=Sum('quantity'))['total']
        return render(request, 'index.html', {'total_quantity': total_quantity})


class RegisterPageView(View):
    def get(self, request):
        return render(request, 'register.html')


class LoginPageView(View):
    def get(self, request):
        return render(request, 'login.html')


class AddDonationPageView(View):
    def get(self, request):
        return render(request, 'form.html')