from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import Customer

from django.contrib import messages

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('home:home')
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        phone = request.POST['phone']
        print(phone)
        for p in phone:
            if not (p =='+' or p =='-' or p.isdigit()):
                messages.error(request, "Invalid phone number")
                return render(request, 'create-account.html', {'error': 'Username already exists'})
        try:

            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        except:
            messages.error(request, "Username already exists")
            return render(request, 'create-account.html', {'error': 'Username already exists'})
        user.save()
        customer = Customer(user=user, phone=phone, address=address)
        customer.save()
        messages.success(request, "New account created successfully!")

        login(request, user)
        return redirect('home:home')
    return render(request, 'create-account.html')

def loginView(request):
    if request.user.is_authenticated:
        return redirect('home:home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home:home')
        else:
            print("Inccorect user name or password")
            messages.info(request, "Invalid username or password.")
            return redirect('loginView')
    return render(request, 'login.html')

def logoutView(request):
    logout(request)
    messages.success(request, "Suucessfully logged out!")
    return redirect('home:home')