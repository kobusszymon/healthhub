from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Avg, Sum
from django.db.models import Min, Max

class PomiarQuerySet(models.QuerySet):
    def dla_uzytkownika(self, user):
        return self.filter(uzytkownik=user)

    def z_dnia(self, dzien):
        return self.filter(data__date=dzien)

    def w_zakresie_dat(self, od, do):
        return self.filter(data__range=(od, do))

    def z_ostatnich_dni(self, dni):
        return self.filter(
            data__gte=timezone.now() - timezone.timedelta(days=dni)
        )
    
    def srednie_cisnienie(self):
        return self.aggregate(
            avg_skurczowe=Avg("cisnienie_skurczowe"),
            avg_rozkurczowe=Avg("cisnienie_rozkurczowe"),
        )
    
    def sredni_cukier(self):
        return self.aggregate(
            avg_cukier=Avg("pomiar_cukru")
        )

    def srednie_tetno(self):
        return self.aggregate(
            avg_tetno=Avg("tetno")
        )
    
    def zakres_tetna(self):
        return self.aggregate(
            min_tetno=Min("tetno"),
            max_tetno=Max("tetno")
        )
    
    def zakres_cukru(self):
        return self.aggregate(
            min_cukier=Min("pomiar_cukru"),
            max_cukier=Max("pomiar_cukru")
        )
    
    def zakres_cisnienia(self):
        return self.aggregate(
            skurcz_min=Min("cisnienie_skurczowe"),
            skurcz_max=Max("cisnienie_skurczowe"),
            rozkurcz_min=Min("cisnienie_rozkurczowe"),
            rozkurcz_max=Max("cisnienie_rozkurczowe"),
        )
    
class AktywnoscQuerySet(models.QuerySet):
    def dla_uzytkownika(self, user):
        return self.filter(uzytkownik=user)

    def typu(self, rodzaj):
        return self.filter(rodzaj_aktywnosci=rodzaj)

    def w_zakresie_dat(self, od, do):
        return self.filter(data__range=(od, do))
    
    def sredni_czas(self):
        return self.aggregate(
            avg_czas=Avg("czas_trwania_minuty")
        )

    def sredni_czas_typu(self, rodzaj):
        return self.filter(
            rodzaj_aktywnosci=rodzaj
        ).aggregate(
            avg_czas=Avg("czas_trwania_minuty")
        )

    def laczny_czas(self):
        return self.aggregate(
            suma_minut=Sum("czas_trwania_minuty")
        )
    
class LekQuerySet(models.QuerySet):
    def dla_uzytkownika(self, user):
        return self.filter(uzytkownik=user)

    def szukaj(self, fraza):
        return self.filter(nazwa__icontains=fraza)   
    
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

        class Meta:
              verbose_name = "Profil użytkownika"
              verbose_name_plural = "Profile użytkowników"

        def __str__(self):
              return f"{self.uzytkownik.first_name} {self.uzytkownik.last_name}"

class Pomiar(models.Model):
        uzytkownik = models.ForeignKey(User, on_delete = models.CASCADE)
        data = models.DateTimeField(auto_now_add = True)
        cisnienie_skurczowe = models.PositiveIntegerField(null = True, blank = True)
        cisnienie_rozkurczowe = models.PositiveIntegerField(null = True, blank = True)
        tetno = models.PositiveIntegerField(null = True, blank = True)
        pomiar_cukru = models.DecimalField(max_digits = 5, decimal_places = 2, null = True, blank = True)

        objects = PomiarQuerySet.as_manager()

        class Meta:
              ordering = ["-data"]
              indexes = [
                    models.Index(fields=["uzytkownik", "data"]),
                ]
              verbose_name = "Pomiar"
              verbose_name_plural = "Pomiary"

        def __str__(self):
              return f"Pomiar {self.uzytkownik.first_name} {self.uzytkownik.last_name} ({self.data.date()})"

class Aktywnosc(models.Model):
        uzytkownik = models.ForeignKey(User, on_delete = models.CASCADE)
        rodzaj_aktywnosci = models.CharField(max_length =50, choices=RodzajAktywnosci.choices)
        czas_trwania_minuty = models.PositiveIntegerField()
        data = models.DateField()

        objects = AktywnoscQuerySet.as_manager() 

        class Meta:
              ordering = ["-data"]
              indexes = [
                    models.Index(fields=["uzytkownik", "data"]),
                ]
              verbose_name = "Aktywność"
              verbose_name_plural = "Aktywności"

        def clean(self):
              if self.czas_trwania_minuty is not None and self.czas_trwania_minuty <= 15:
                    raise ValidationError({
                          "czas_trwania_minuty": "Czas trwania musi być większy niż 15 minut."
                          })

        def __str__(self):
              return f"{self.get_rodzaj_aktywnosci_display()} - {self.uzytkownik.first_name} {self.uzytkownik.last_name}"
    
class Lek(models.Model):
        uzytkownik = models.ForeignKey(User, on_delete = models.CASCADE)
        nazwa = models.CharField(max_length = 100)
        dawka = models.CharField(max_length = 100)

        objects = LekQuerySet.as_manager()  

        class Meta:
              ordering = ["nazwa"]
              verbose_name = "Lek"
              verbose_name_plural = "Leki"

        def __str__(self):
              return f"{self.nazwa} - {self.uzytkownik.first_name} {self.uzytkownik.last_name}"

class Lokalizacja(models.Model):
      nazwa = models.CharField(max_length = 150)
      adres = models.CharField(max_length = 200)
      miasto = models.CharField(max_length = 100)
      
      class Meta:
        ordering = ["nazwa", "miasto"]
        verbose_name = "Lokalizacja"
        verbose_name_plural = "Lokalizacje"

      def __str__(self):
        return f"{self.nazwa} | {self.adres}, {self.miasto}"

class TerminWizyty(models.Model):
      imie_nazwisko_lekarza = models.CharField(max_length=100)
      specjalizacja = models.CharField(max_length=100)
      data_wizyty = models.DateTimeField()
      lokalizacja = models.ForeignKey(Lokalizacja, on_delete = models.PROTECT)
      uzytkownik = models.ForeignKey(User, null = True, blank = True, on_delete = models.SET_NULL)
      
      class Meta:
        ordering = ["data_wizyty"]
        indexes = [
              models.Index(fields = ["uzytkownik", "data_wizyty"]),
              models.Index(fields = ["data_wizyty"]),
        ]
        verbose_name = "Termin wizyty"
        verbose_name_plural = "Terminy wizyt"
        constraints = [
              models.UniqueConstraint(
                    fields=["imie_nazwisko_lekarza", "data_wizyty", "lokalizacja"],
                    name="unique_termin",
                    )
                ]
    
        def __str__(self):
              if self.uzytkownik:
                    return (f"Termin wizyty u {self.imie_nazwisko_lekarza}: {self.uzytkownik.first_name} {self.uzytkownik.last_name}")
              return f"Termin wizyty u {self.imie_nazwisko_lekarza}: wolny"