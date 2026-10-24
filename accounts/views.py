from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from config.settings import ADMIN_MAILS
from .models import User
from django.conf import settings

# Create your views here.
def login_view(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate( request, email=email, password=password)

        if user:
            messages.success(request, f'Welcom Back {user.first_name} {user.last_name}')
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, f'Invalid Email({email}) or Password({password})')

        return redirect('Login')

    context = {
        "is_login" : True,
    }
    return render(request, "accounts/login.html", context=context)

def register_view(request):
    # print('admin@gamil.com' in settings.ADMIN_MAILS)
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.warning(request, f"Account with username {username} already exists.")
            return redirect('Register')

        if User.objects.filter(email=email).exists():
            messages.warning(request, f'Account with Email ID {email} already exists.')
            return render('Register')

        User.objects.create_user(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = password,
            is_admin = email in settings.ADMIN_MAILS
        )

        messages.success(request, f"New account has been created with Email ID {email}")
        return redirect('Login')

    context = {
        "is_login" : False,
    }
    return render(request, "accounts/login.html", context = context)

@login_required(login_url='Login')
def logout_view(request):
    request.session.flush() # to remove all data stored in session
    logout(request)
    messages.warning(request, f'Your Account has been Logged Out')
    return redirect("Home")