from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import permission_required
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from .permission import IsUzytkownik
from .models import ProfilUzytkownika, Pomiar, Lek, Aktywnosc, Lokalizacja, TerminWizyty
from .serializers import ProfilUzytkownikaSerializer, PomiarSerializer, LekSerializer, AktywnoscSerializer, LokalizacjaSerializer, TerminWizytySerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def profil_list(request):
    if request.method == 'GET':
        profile = ProfilUzytkownika.objects.all()
        serializer = ProfilUzytkownikaSerializer(profile, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = ProfilUzytkownikaSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def profil_detail(request, pk):
    try:
        profil = ProfilUzytkownika.objects.get(pk = pk)
    except ProfilUzytkownika.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProfilUzytkownikaSerializer(profil)
        if not (
            IsUzytkownik().has_object_permission(request, None, profil)
            or IsAdminUser().has_permission(request, None)
        ):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = ProfilUzytkownikaSerializer(profil, data = request.data)
        if not (
            IsUzytkownik().has_object_permission(request, None, profil)
            or IsAdminUser().has_permission(request, None)
        ):
            return Response(status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if not IsAdminUser().has_permission(request, None):
            return Response(status=status.HTTP_403_FORBIDDEN)
        profil.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def pomiar_list(request):
    if request.method == 'GET':
        pomiary = Pomiar.objects.all()
        serializer = PomiarSerializer(pomiary, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = PomiarSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST'])
def pomiar_uzytkownika(request):
    if request.method == 'GET':
        pomiary = Pomiar.objects.filter(uzytkownik=request.user)
        serializer = PomiarSerializer(pomiary, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = PomiarSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(uzytkownik = request.user)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def pomiar_detail(request, pk):
    try:
        pomiar = Pomiar.objects.get(pk = pk)
    except Pomiar.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PomiarSerializer(pomiar)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = PomiarSerializer(pomiar, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        pomiar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def lek_list(request):
    if request.method == 'GET':
        leki = Lek.objects.all()
        serializer = LekSerializer(leki, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = LekSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def lek_detail(request, pk):
    try:
        lek = Lek.objects.get(pk = pk)
    except Lek.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = LekSerializer(lek)
        if not (
            IsUzytkownik().has_object_permission(request, None, lek)
            or IsAdminUser().has_permission(request, None)
        ):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = LekSerializer(lek, data = request.data)
        if not (
            IsUzytkownik().has_object_permission(request, None, lek)
            or IsAdminUser().has_permission(request, None)
        ):
            return Response(status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if not (
            IsUzytkownik().has_object_permission(request, None, lek)
            or IsAdminUser().has_permission(request, None)
        ):
            return Response(status=status.HTTP_403_FORBIDDEN)
        lek.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def aktywnosc_list(request):
    if request.method == 'GET':
        aktywnosci = Aktywnosc.objects.all()
        serializer = AktywnoscSerializer(aktywnosci, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = AktywnoscSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def aktywnosc_detail(request, pk):
    try:
        aktywnosc = Aktywnosc.objects.get(pk = pk)
    except Aktywnosc.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = AktywnoscSerializer(aktywnosc)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = AktywnoscSerializer(aktywnosc, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        aktywnosc.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def aktywnosc_uzytkownika(request):
    if request.method == 'GET':
        aktywnosci = Aktywnosc.objects.filter(uzytkownik=request.user)
        serializer = AktywnoscSerializer(aktywnosci, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = AktywnoscSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(uzytkownik = request.user)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def lokalizacja_list(request):
    lokalizacje = Lokalizacja.objects.all()
    serializer = LokalizacjaSerializer(lokalizacje, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def lokalizacja_create(request):
    serializer = LokalizacjaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def lokalizacja_detail(request, pk):
    try:
        lokalizacja = Lokalizacja.objects.get(pk = pk)
    except Lokalizacja.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    serializer = LokalizacjaSerializer(lokalizacja)
    return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def lokalizacja_update_delete(request, pk):
    try:
        lokalizacja = Lokalizacja.objects.get(pk = pk)
    except Lokalizacja.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = LokalizacjaSerializer(lokalizacja, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        lokalizacja.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
        
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def termin_list_admin(request):
    if request.method == 'GET':
        terminy = TerminWizyty.objects.all()
        serializer = TerminWizytySerializer(terminy, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = TerminWizytySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def wolne_terminy(request):
    if request.method == 'GET':
        terminy = TerminWizyty.objects.filter(uzytkownik__isnull = True, data_wizyty__gte = timezone.now())
        serializer = TerminWizytySerializer(terminy, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(['GET'])
def wolne_terminy_specjalizacja(request):
    if request.method == 'GET':
        specjalizacja = request.query_params.get('specialty', None)
        terminy = TerminWizyty.objects.filter(uzytkownik__isnull = True, data_wizyty__gte = timezone.now(), specjalizacja__icontains = specjalizacja)
        serializer = TerminWizytySerializer(terminy, many = True)
        if specializacja is not None:
            return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(['GET'])
def przyszle_wizyty_uzytkownika(request):
    if request.method == 'GET':
        terminy = TerminWizyty.objects.filter(uzytkownik__isnull = True, data_wizyty__gte = timezone.now())
        serializer = TerminWizytySerializer(terminy, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def termin_detail(request, pk):
    try:
        termin = TerminWizyty.objects.get(pk = pk)
    except TerminWizyty.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TerminWizytySerializer(termin)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = TerminWizytySerializer(termin, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        termin.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def rezerwuj_termin(request, pk):
    try:
        termin = TerminWizyty.objects.get(pk = pk)
    except TerminWizyty.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        if termin.uzytkownik is not None:
            return Response({"detail": "Ten termin jest już zajęty przez inną osobę."},
            status=status.HTTP_400_BAD_REQUEST)
        serializer = TerminWizytySerializer(termin, data = request.data)
        if serializer.is_valid():
            serializer.save(uzytkownik=request.user)
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)