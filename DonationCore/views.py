import json

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
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


class DonationPageView(View):
    def get(self, request):
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


class UserPageView(View):
    def get(self, request):
        user = request.user
        donations = Donation.objects.filter(user=user)
        return render(request, 'user_temp.html', {'donations': donations})


class UserEditPageView(View):
    def get(self, request):
        user = request.user
        return render(request, 'user_edit.html', {'user': user})

    def post(self, request):
        user = request.user
        username = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        print(f"Received POST data - first_name: {first_name}, last_name: {last_name}, email: {email}")
        if not first_name or not last_name or not email:
            return render(request, 'user_edit.html', {'user': user, 'error': 'Wszystkie pola muszą być wypełnione.'})

        # Aktualizacja danych użytkownika
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        return redirect('user')


class PasswordConfView(View):
    def get(self, request):
        user = request.user
        return render(request, 'password_conf.html')

    def post(self, request):
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            return redirect('user_edit')
        else:
            return render(request, 'password_conf.html', {'error': 'Błędne hasło.'})


class ChangePassView(View):
    def get(self, request):
        return render(request, 'password_change.html')

    def post(self, request):
        curr_pass = request.POST.get('curr_pass')
        new_pass = request.POST.get('new_pass')
        conf_pass = request.POST.get('conf_pass')
        print(f" 1{curr_pass}, 2{new_pass}, 3{conf_pass}")
        if new_pass != conf_pass:
            return render(request, 'password_change.html', {'error': 'Nowe hasła nie są zgodne.'})

        user = request.user
        if user.check_password(curr_pass):
            user.set_password(new_pass)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('user_edit')
        else:
            return render(request, 'password_change.html', {'error': 'Błędne hasło.'})
