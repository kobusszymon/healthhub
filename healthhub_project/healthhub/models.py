from django.db import models

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