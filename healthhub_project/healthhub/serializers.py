from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (ProfilUzytkownika, Pomiar, Aktywnosc, Lek, Lokalizacja, TerminWizyty)

class ProfilUzytkownikaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilUzytkownika
        fields = "__all__"
        read_only_fields = ["id"]

class PomiarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pomiar
        fields = "__all__"
        read_only_fields = ["id", "data"]

class AktywnoscSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aktywnosc
        fields = "__all__"
        read_only_fields = ["id"]

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

class TerminWizytySerializer(serializers.ModelSerializer):
    class Meta:
        model = TerminWizyty
        fields = "__all__"
        read_only_fields = ["id"]