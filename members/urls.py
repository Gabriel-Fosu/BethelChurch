from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.member_register, name='member_register'),
    path('login/', views.member_login, name='member_login'),
    path('logout/', views.member_logout, name='member_logout'),
    path('dashboard/', views.member_dashboard, name='member_dashboard'),
    path('profile/', views.member_profile, name='member_profile'),
]