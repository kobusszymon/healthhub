from django.contrib import admin

from .models import ProfilUzytkownika, Pomiary, Aktywnosc, Leki, Wizyty

admin.site.register(ProfilUzytkownika)
admin.site.register(Pomiary)
admin.site.register(Aktywnosc)
admin.site.register(Leki)
admin.site.register(Wizyty)
