from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views import View

from DonationCore.models import Donation, Institution, Category


class LandingPageView(View):
    def get(self, request):
        institutions = Institution.objects.prefetch_related('categories')
        total_quantity = Donation.objects.aggregate(total=Sum('quantity'))['total']
        institutions_number = Institution.objects.count()

        paginator = Paginator(institutions, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'index.html', {'total_quantity': total_quantity,
                                              'institutions_number': institutions_number,
                                              'institutions': institutions,
                                              'page_obj': page_obj})


class RegisterPageView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if not email or not password:
            return render(request, 'register.html', {'error': 'Email i hasło są wymagane'})

        if password != '' and password == password2:
            u = User.objects.create_user(username=email, first_name=first_name, last_name=last_name,
                                         email=email, password=password)
            return redirect('login')
        return render(request, 'register.html', {'error': "Hasła się nie zgadzają"})


class LoginPageView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            redirect_url = request.GET.get('next', 'home')

            return redirect(redirect_url)
        else:
            return render(request, 'register.html', {'error': "Nie ma takiego użytkownika"})

class AddDonationPageView(View):
    def get(self, request):
        return render(request, 'form.html')