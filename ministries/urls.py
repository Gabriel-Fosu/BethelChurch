from django.urls import path
from . import views

urlpatterns = [
    path('', views.ministries_home, name='ministries_home'),
    path('<slug:slug>/', views.ministry_detail, name='ministry_detail'),
    path('<slug:ministry_slug>/ministries/', views.group_list, name='group_list'),
    path('<slug:ministry_slug>/ministries/<slug:slug>/', views.group_detail, name='group_detail'),
]