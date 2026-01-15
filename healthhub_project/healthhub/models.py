from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Plec(models.IntegerChoices):
        MEZCZYZNA = 1, "Mężczyzna"
        KOBIETA = 2, "Kobieta"
        INNA = 3, "Inna"

class RodzajAktywnosci(models.TextChoices):
        BIEGANIE = "bieganie", "Bieganie"
        JAZDA_ROWEREM = "jazda_rowerem", "Jazda rowerem"
        PLYWANIE = "plywanie", "Pływanie"
        SILOWNIA = "silownia", "Siłownia"
        INNA = "inna", "Inna"

class ProfilUzytkownika(models.Model):
        uzytkownik = models.OneToOneField(User, on_delete=models.CASCADE)
        plec = models.IntegerField(choices = Plec.choices, default = 3)
        telefon = models.CharField(max_length = 9, blank = True)
        data_urodzenia = models.DateField(null=True, blank=True)
        wzrost_cm = models.PositiveIntegerField(null=True, blank=True)
        waga_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

        def __str__(self):
                return f"{self.uzytkownik.first_name} {self.uzytkownik.last_name}"

class Pomiary(models.Model):
        uzytkownik = models.ForeignKey(User, on_delete = models.CASCADE)
        data = models.DateTimeField(auto_now_add = True)
        cisnienie_skurczowe = models.PositiveIntegerField(null = True, blank = True)
        cisnienie_rozkurczowe = models.PositiveIntegerField(null = True, blank = True)
        tetno = models.PositiveIntegerField(null = True, blank = True)
        pomiar_cukru = models.DecimalField(max_digits = 5, decimal_places = 2, null = True, blank = True)

        class Meta:
            ordering = ["-data"]
            indexes = [
            models.Index(fields=["uzytkownik", "data"]),
            ]
            verbose_name = "Pomiar"
            verbose_name_plural = "Pomiary"

        def __str__(self):
                return f"Pomiar zdrowia – {self.uzytkownik.first_name} {self.uzytkownik.last_name} ({self.data.date()})"

class Aktywnosc(models.Model):
        uzytkownik = models.ForeignKey(User, on_delete = models.CASCADE)
        rodzaj_aktywnosci = models.CharField(max_length =50, choices=RodzajAktywnosci.choices)
        czas_trwania_minuty = models.PositiveIntegerField()
        data = models.DateField()

        class Meta:
            ordering = ["-data"]
            indexes = [
            models.Index(fields=["uzytkownik", "data"]),
            ]
            verbose_name = "Aktywność"
            verbose_name_plural = "Aktywności"

        def __str__(self):
                return f"{self.get_rodzaj_aktywnosci_display()} - {self.uzytkownik.first_name} {self.uzytkownik.last_name}"

class Leki(models.Model):
        uzytkownik = models.ForeignKey(User, on_delete = models.CASCADE)
        nazwa = models.CharField(max_length = 100)
        dawka = models.CharField(max_length = 100)

        class Meta:
            ordering = ["nazwa"]
            verbose_name = "Lek"
            verbose_name_plural = "Leki"

        def __str__(self):
                return f"{self.nazwa} – {self.uzytkownik.first_name} {self.uzytkownik.last_name}"
        
class Wizyty(models.Model):
        uzytkownik = models.ForeignKey(User, on_delete = models.CASCADE)
        imie_nazwisko_lekarza = models.CharField(max_length = 100)
        specjalizacja = models.CharField(max_length = 100)
        data_wizyty = models.DateTimeField()
        lokalizacja = models.CharField(max_length = 200)
        notatki = models.TextField(blank = True)

        class Meta:
            ordering = ["-data_wizyty"]
            indexes = [
            models.Index(fields=["uzytkownik", "data_wizyty"]),
            ]
            verbose_name = "Wizyta"
            verbose_name_plural = "Wizyty"
    
        def __str__(self):
                return f"Wizyta u {self.imie_nazwisko_lekarza} – {self.uzytkownik.first_name} {self.uzytkownik.last_name}"   

