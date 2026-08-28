from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('<slug:category_slug>/', views.gallery_category, name='gallery_category'),
]