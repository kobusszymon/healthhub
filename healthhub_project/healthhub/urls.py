from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profil_list, name = 'profil-list'),
    path('profile/<int:pk>/', views.profil_detail, name = 'profil-detail'),
    path('pomiar/', views.pomiar_list, name ='pomiar-list'),
    path('pomiar/<int:pk>/', views.pomiar_detail, name = 'pomiar-detail'),
]