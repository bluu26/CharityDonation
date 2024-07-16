from django.shortcuts import render
from django.views import View


class LandingPageView(View):
    def get(self, request):
        return render(request, 'index.html')


class RegisterPageView(View):
    def get(self, request):
        return render(request, 'register.html')


class LoginPageView(View):
    def get(self, request):
        return render(request, 'login.html')


class AddDonationPageView(View):
    def get(self, request):
        return render(request, 'form.html')