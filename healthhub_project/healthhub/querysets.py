from django.utils import timezone
from django.db.models import Q
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
    
    def liczba(self):
        return self.count()
    
    def ostatni(self):
        return self.order_by("-data").first()
    
    def srednie_cisnienie(self):
        return self.filter(
            cisnienie_skurczowe__isnull=False,
            cisnienie_rozkurczowe__isnull=False,
        ).aggregate(
            avg_skurczowe=Avg("cisnienie_skurczowe"),
            avg_rozkurczowe=Avg("cisnienie_rozkurczowe"),
        )
    
    def sredni_cukier(self):
        return self.filter(pomiar_cukru__isnull=False).aggregate(
            avg_cukier=Avg("pomiar_cukru")
        )

    def srednie_tetno(self):
        return self.filter(tetno__isnull=False).aggregate(
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

    def wysokie_cisnienie(self):
        return self.filter(
            Q(cisnienie_skurczowe__gte=140) | 
            Q(cisnienie_rozkurczowe__gte=90)
        )

    def w_normie(self):
            return self.filter(
            cisnienie_skurczowe__lt=130,
            cisnienie_rozkurczowe__lt=85
            ) 
    
    def wysokie_tetno(self, prog=100):
            return self.filter(tetno__gte=prog)
    

class AktywnoscQuerySet(models.QuerySet):
    def dla_uzytkownika(self, user):
        return self.filter(uzytkownik=user)

    def typu(self, rodzaj):
        return self.filter(rodzaj_aktywnosci=rodzaj)

    def w_zakresie_dat(self, od, do):
        return self.filter(data__range=(od, do))
    
    def liczba(self):
        return self.count()

    def ostatni(self):
        return self.order_by("-data").first()
    
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


class LokalizacjaQuerySet(models.QuerySet):
    def po_nazwie(self, fraza):
        return self.filter(nazwa__icontains=fraza)

    def po_adresie(self, fraza):
        return self.filter(adres__icontains=fraza)

    def w_miescie(self, miasto):
        return self.filter(miasto__iexact=miasto)

    def szukaj(self, fraza):
        return self.filter(
            Q(nazwa__icontains=fraza) |
            Q(adres__icontains=fraza) |
            Q(miasto__icontains=fraza)
        )  


class TerminWizytyQuerySet(models.QuerySet):
    def dla_uzytkownika(self, user):
        return self.filter(uzytkownik=user)

    def wolne(self):
        return self.filter(uzytkownik__isnull=True)

    def po_lekarzu(self, fraza):
        return self.filter(imie_nazwisko_lekarza__icontains=fraza)

    def po_specjalizacji(self, fraza):
        return self.filter(specjalizacja__icontains=fraza)

    def w_dniu(self, dzien):
        return self.filter(data_wizyty__date=dzien)

    def w_zakresie_dat(self, od, do):
        return self.filter(data_wizyty__range=(od, do))

    def przyszle(self):
        return self.filter(data_wizyty__gte=timezone.now())

    def przeszle(self):
        return self.filter(data_wizyty__lt=timezone.now())

    def szukaj(self, fraza):
        if not fraza:
            return self
        return self.filter(
            Q(imie_nazwisko_lekarza__icontains=fraza) |
            Q(specjalizacja__icontains=fraza) |
            Q(lokalizacja__nazwa__icontains=fraza) |
            Q(lokalizacja__miasto__icontains=fraza)
        )      
    
