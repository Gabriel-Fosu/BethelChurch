from django.urls import path
from . import views

urlpatterns = [
    path('', views.sermon_list, name='sermon_list'),
    path('results/', views.sermon_results, name='sermon_results'),
    path('<slug:slug>/', views.sermon_detail, name='sermon_detail'),
]