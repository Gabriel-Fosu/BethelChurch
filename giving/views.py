from django.shortcuts import render, redirect

# Create your views here.
def give(request):
    return render(request, 'giving/give.html')

def verify_payment(request):
    return redirect('give')