from django.contrib import admin

from .models import ProfilUzytkownika, Pomiar, Aktywnosc, Lek, Lokalizacja, TerminWizyty

admin.site.register(ProfilUzytkownika)
admin.site.register(Pomiar)
admin.site.register(Aktywnosc)
admin.site.register(Lek)
admin.site.register(Lokalizacja)
admin.site.register(TerminWizyty)
