from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


def login(request):
    if request.method == 'POST':
        # Get form values
        username = request.POST['username'].strip()
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if not user:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

        # Login User
        auth.login(request, user)
        return redirect('index')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
    return redirect('index')


def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name'].strip()
        last_name = request.POST['last_name'].strip()
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check user doesn't exist
        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, 'Username already exists')

        # Check email doesn't exist
        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'Email already exists')

        # Check passwords match
        if password != password2:
            messages.error(request, 'Passwords do not match')

        if messages.get_messages(request):
            return redirect('register')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )
        # Login after register
        # auth.login(request, user)
        # messages.success(request, 'You are now logged in')
        # return redirect('index')

        # Have user login after registration
        user.save()
        messages.success(request, 'You are now registered and can log in')
        return redirect('login')

    else:
        return render(request, 'accounts/register.html')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')
