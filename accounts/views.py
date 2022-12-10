from django.contrib import messages
from django.shortcuts import redirect, render


def login(request):
    if request.method == 'POST':
        # Login User
        print('SUBMITTED LOGIN')
        return redirect('login')

    return render(request, 'accounts/login.html')


def logout(request):
    return redirect('index')


def register(request):
    if request.method == 'POST':
        # Register User
        messages.error(request, 'Testing error message')
        return redirect('register')

    return render(request, 'accounts/register.html')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')
