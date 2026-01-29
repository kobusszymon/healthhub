from django.urls import path
from . import views

urlpatterns = [
    path('rejestracja/', views.rejestracja, name = 'rejestracja'),
    path('profil/', views.profil_list, name = 'profil-list'),
    path('profil/<int:pk>/', views.profil_detail, name = 'profil-detail'),
    path('pomiar/', views.pomiar_list, name ='pomiar-list'),
    path('pomiar/<int:pk>/', views.pomiar_detail, name = 'pomiar-detail'),
    path('pomiar/uzytkownik/', views.pomiar_uzytkownika, name ='pomiar-uzytkownika'),
    path('lek/', views.lek_list, name ='lek-list'),
    path('lek/<int:pk>/', views.lek_detail, name = 'lek-detail'),
    path('lek/uzytkownik/', views.lek_uzytkownika, name = 'lek-uzytkownika'),
    path('aktywnosc/', views.aktywnosc_list, name ='aktywnosc-list'),
    path('aktywnosc/<int:pk>/', views.aktywnosc_detail, name = 'aktywnosc-detail'),
    path('aktywnosc/uzytkownik/', views.aktywnosc_uzytkownika, name = 'aktywnosc-uzytkownika'),
    path('lokalizacja/', views.lokalizacja_list, name ='lokalizacja-list'),
    path('lokalizacja/create', views.lokalizacja_create, name ='lokalizacja-create'),
    path('lokalizacja/<int:pk>/', views.lokalizacja_detail, name = 'lokalizacja-detail'),
    path('lokalizacja/update_delete/<int:pk>/', views.lokalizacja_update_delete, name = 'lokalizacja_update_delete'),
    path('termin/', views.termin_list_admin, name ='termin-list'),
    path('termin/przyszle/uzytkownik/', views.przyszle_wizyty_uzytkownika, name = 'przyszle-wizyty-uzytkownka'),
    path('termin/wolne/', views.wolne_terminy, name = 'wolne-terminy'),
    path('termin/wolne/specjalizacja', views.wolne_terminy_specjalizacja),
    path('termin/<int:pk>/', views.termin_detail, name = 'termin-detail'),
    path('termin/wolne/<int:pk>/rezerwuj/', views.rezerwuj_termin, name = 'rezerwuj-termin'),
]