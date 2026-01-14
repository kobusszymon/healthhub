from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Plec(models.IntegerChoices):
        MEZCZYZNA = 1, "Mężczyzna"
        KOBIETA = 2, "Kobieta"
        INNA = 3, "Inna"

class Uzytkownik(models.Model):
        imie = models.CharField(max_length = 50)
        nazwisko = models.CharField(max_length = 100)
        plec = models.IntegerField(choices = Plec.choices, default = 3)
        telefon = models.CharField(max_length = 9, blank = True)
        email = models.EmailField
        data_utworzenia = models.DateTimeField (auto_now_add = True, editable = False)

class ProfilUzytkownika(models.Model):
        uzytkownik = models.OneToOneField(User, on_delete=models.CASCADE)
        data_urodzenia = models.DateField(null=True, blank=True)
        wzrost_cm = models.PositiveIntegerField(null=True, blank=True)
        waga_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

        def __str__(self):
            return f"Profil użytkownika: {self.uzytkownik.username}"


class Pomiary(models.Model):
        uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
        data = models.DateTimeField(auto_now_add=True)
        cisnienie_skurczowe = models.PositiveIntegerField(null=True, blank=True)
        cisnienie_rozkurczowe = models.PositiveIntegerField(null=True, blank=True)
        tetno = models.PositiveIntegerField(null=True, blank=True)
        pomiar_cukru = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

        def __str__(self):
            return f"Pomiar zdrowia – {self.uzytkownik.username} ({self.data.date()})"

   