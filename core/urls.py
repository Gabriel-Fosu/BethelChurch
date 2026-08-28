from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('visit/', views.visit, name='visit'),
    path('live/', views.live, name='live'),
#    path('ministries/', views.ministries, name='ministries'),
    path('project/', views.project, name='project'),
    path('gallery/', views.gallery, name='gallery'),
    path('error404/', views.error_404, name='error_404'),
    path('error500/', views.error_500, name='error_500'),
]