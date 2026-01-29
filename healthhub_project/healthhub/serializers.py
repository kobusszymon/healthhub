from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from .models import ProfilUzytkownika, Pomiar, Aktywnosc, Lek, Lokalizacja, TerminWizyty

class RejestracjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
    
    def validate_username(self, value):
        if User.objects.filter(username = value).exists():
            raise serializers.ValidationError("Nie mozna utworzyć konta o istniejącej nazwie uzytkownika.")
        return value
    
    def validate_email(self, value):
        if value and User.objects.filter(email = value).exists():
            raise serializers.ValidationError("Nie mozna utworzyć konta o podanym juz adresie e-mail.")
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ProfilUzytkownikaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilUzytkownika
        fields = "__all__"
        read_only_fields = ["id"]

    def validate_telefon(self, value):
        if value:
            if not value.isdigit():
                raise serializers.ValidationError("Telefon może zawierać tylko cyfry.")
            if len(value) != 9:
                raise serializers.ValidationError("Telefon musi mieć 9 cyfr.")
        return value
    
    def validate_data_urodzenia(self, value):
        if value > timezone.now():
            raise serializers.ValidationError("Data urodzenia nie może być z przyszłości.")
        return value

class PomiarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pomiar
        fields = "__all__"
        read_only_fields = ["id", "data"]
        
    def validate_pomiar_cukru(self, value):
        if value is None:
            return value
        if value <= 0:
            raise serializers.ValidationError("Pomiar cukru musi być większy od 0.")
        return value

    def validate(self, data):
        skurczowe = data.get("cisnienie_skurczowe")
        rozkurczowe = data.get("cisnienie_rozkurczowe")
        if skurczowe is not None and rozkurczowe is not None and rozkurczowe >= skurczowe:
            raise serializers.ValidationError(
                {"cisnienie_rozkurczowe": "Ciśnienie rozkurczowe musi być mniejsze niż skurczowe."}
            )
        return data

class AktywnoscSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aktywnosc
        fields = "__all__"
        read_only_fields = ["id"]

    def validate_czas_trwania_minuty(self, value):
        if value <= 15:
            raise serializers.ValidationError("Czas trwania musi być większy niż 15 minut.")
        return value
    
    def validate_data(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Data aktywności nie może być z przeszłości.")
        return value

class LekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lek
        fields = "__all__"
        read_only_fields = ["id"]

class LokalizacjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lokalizacja
        fields = "__all__"
        read_only_fields = ["id"]

    def validate(self, data):
        if not data["nazwa"]:
            raise serializers.ValidationError({"nazwa": "Nazwa placówki nie może być pusta."})
        if not data["adres"]:
            raise serializers.ValidationError({"adres": "Adres musi być uzupełniony."})
        if not data["miasto"]:
            raise serializers.ValidationError({"miasto": "Miasto musi być uzupełnione."})
        return data

class TerminWizytySerializer(serializers.ModelSerializer):
    class Meta:
        model = TerminWizyty
        fields = "__all__"
        read_only_fields = ["id"]
    
    def validate_data_wizyty(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Nie można utworzyć terminu wizyty w przeszłości.")
        return value
    
class RezerwacjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TerminWizyty
        fields = ["uzytkownik"]