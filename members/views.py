from django.shortcuts import render, redirect

# Create your views here.
def member_register(request, slug):
    return render(request, 'members/register.html')

def member_login(request):
    return render(request, 'members/login.html')

def member_logout(request):
    return redirect('home')

def member_dashboard(request):
    return render(request, 'members/dashboard.html')

def member_profile(request):
    return render(request, 'members/profile.html')