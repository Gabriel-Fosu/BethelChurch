from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def prayer_wall(request):
    return render(request, 'prayer/prayer_wall.html')

def pray_for(request):
    return JsonResponse({'prayer_count': 0})