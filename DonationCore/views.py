import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse
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
        user = request.user

        if request.user.is_authenticated:
            return render(request, 'index.html', {'total_quantity': total_quantity,
                                                 'institutions_number': institutions_number,
                                                 'institutions': institutions,
                                                 'page_obj': page_obj})

        else:
            return render(request, 'index.html', {'total_quantity': total_quantity,
                                                  'institutions_number': institutions_number,
                                                  'institutions': institutions,
                                                  'page_obj': page_obj,
                                                  'user': user})


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


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


import json
from django.http import JsonResponse
from django.views import View
from .models import Donation, Category, Institution

class DonationPageView(View):
    def get(self, request):
        print('penis')
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, 'form.html', {'categories': categories, 'institutions': institutions})

    def post(self, request):
        print(request.body)
        try:
            data = json.loads(request.body)
            print(data)
            categories_ids = data.get('categories', [])
            bags = data.get('bags', 0)
            institution_name = data.get('institution', '')
            address = data.get('address', {})

            categories = Category.objects.filter(id__in=categories_ids)
            institution = Institution.objects.get(name=institution_name)

            donation = Donation(
                quantity=bags,
                institution=institution,
                address=address['street'],
                phone_number=address['phone'],
                city=address['city'],
                zip_code=address['zipCode'],
                pick_up_date=address['date'],
                pick_up_time=address['time'],
                pick_up_comment=address['comments'],
                user=request.user
            )
            donation.save()
            donation.categories.set(categories)

            return JsonResponse({'status': 'success', 'message': 'Donation created successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)



class DonationConfirmationPageView(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')
