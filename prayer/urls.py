from django.urls import path
from . import views

urlpatterns = [
    path('', views.prayer_wall, name='prayer_wall'),
    path('<int:pk>/pray/', views.pray_for, name='pray_for'),
]