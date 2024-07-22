from django.db.models import Sum
from django.shortcuts import render
from django.views import View

from DonationCore.models import Donation, Institution, Category


class LandingPageView(View):
    def get(self, request):
        institutions = Institution.objects.prefetch_related('categories')
        total_quantity = Donation.objects.aggregate(total=Sum('quantity'))['total']
        institutions_number = Institution.objects.count()
        return render(request, 'index.html', {'total_quantity': total_quantity,
                                              'institutions_number': institutions_number,
                                              'institutions': institutions})


class RegisterPageView(View):
    def get(self, request):
        return render(request, 'register.html')


class LoginPageView(View):
    def get(self, request):
        return render(request, 'login.html')


class AddDonationPageView(View):
    def get(self, request):
        return render(request, 'form.html')