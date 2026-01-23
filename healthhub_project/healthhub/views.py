from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ProfilUzytkownika, Pomiar, Lek, Aktywnosc, Lokalizacja, TerminWizyty
from .serializers import ProfilUzytkownikaSerializer, PomiarSerializer, LekSerializer, AktywnoscSerializer, LokalizacjaSerializer, TerminWizytySerializer

@api_view(['GET', 'POST'])
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
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = ProfilUzytkownikaSerializer(profil, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        profil.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
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
    
@api_view(["GET", "POST"])
def pomiar_list(request):
    qs = Pomiar.objects.dla_uzytkownika(request.user)

    if request.method == "GET":
        dni = request.query_params.get("dni")
        if dni:
            qs = qs.z_ostatnich_dni(int(dni))

        return Response({
            "count": qs.liczba(),
            "ostatni": PomiarSerializer(qs.ostatni()).data if qs.ostatni() else None,
            "srednie_cisnienie": qs.srednie_cisnienie(),
            "srednie_tetno": qs.srednie_tetno(),
            "sredni_cukier": qs.sredni_cukier(),
            "zakres_cisnienia": qs.zakres_cisnienia(),
            "zakres_tetna": qs.zakres_tetna(),
            "zakres_cukru": qs.zakres_cukru(),
            "wyniki": PomiarSerializer(qs, many=True).data,
        })

    elif request.method == "POST":
        serializer = PomiarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uzytkownik=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
   

@api_view(['GET', 'PUT', 'DELETE'])
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
    
@api_view(["GET", "PUT", "DELETE"])
def pomiar_detail(request, pk):
    try:
        pomiar = Pomiar.objects.dla_uzytkownika(request.user).get(pk=pk)
    except Pomiar.DoesNotExist:
        return Response(status=404)

    if request.method == "GET":
        return Response(PomiarSerializer(pomiar).data)

    elif request.method == "PUT":
        serializer = PomiarSerializer(pomiar, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == "DELETE":
        pomiar.delete()
        return Response(status=204)
   

@api_view(['GET', 'POST'])
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
    
@api_view(["GET", "POST"])
def lek_list(request):
    qs = Lek.objects.dla_uzytkownika(request.user)

    if request.method == "GET":
        fraza = request.query_params.get("q")
        if fraza:
            qs = qs.szukaj(fraza)

        return Response(LekSerializer(qs, many=True).data)

    elif request.method == "POST":
        serializer = LekSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uzytkownik=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
   

@api_view(['GET', 'PUT', 'DELETE'])
def lek_detail(request, pk):
    try:
        lek = Lek.objects.get(pk = pk)
    except Lek.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = LekSerializer(lek)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = LekSerializer(lek, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        lek.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
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
    
@api_view(["GET", "POST"])
def aktywnosc_list(request):
    qs = Aktywnosc.objects.dla_uzytkownika(request.user)

    if request.method == "GET":
        rodzaj = request.query_params.get("rodzaj")
        if rodzaj:
            qs = qs.typu(rodzaj)

        return Response({
            "count": qs.liczba(),
            "ostatni": AktywnoscSerializer(qs.ostatni()).data if qs.ostatni() else None,
            "sredni_czas": qs.sredni_czas(),
            "laczny_czas": qs.laczny_czas(),
            "wyniki": AktywnoscSerializer(qs, many=True).data,
        })

    elif request.method == "POST":
        serializer = AktywnoscSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uzytkownik=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
   

@api_view(['GET', 'PUT', 'DELETE'])
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
def lokalizacja_list(request):
    if request.method == 'GET':
        lokalizacje = Lokalizacja.objects.all()
        serializer = LokalizacjaSerializer(lokalizacje, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = LokalizacjaSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
def lokalizacja_list(request):
    qs = Lokalizacja.objects.all()

    fraza = request.query_params.get("q")
    if fraza:
        qs = qs.szukaj(fraza)

    return Response(LokalizacjaSerializer(qs, many=True).data)
   

@api_view(['GET', 'PUT', 'DELETE'])
def lokalizacja_detail(request, pk):
    try:
        lokalizacja = Lokalizacja.objects.get(pk = pk)
    except Lokalizacja.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = LokalizacjaSerializer(lokalizacja)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
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
def termin_list(request):
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
    
@api_view(["GET"])
def termin_list(request):
    qs = TerminWizyty.objects.przyszle()

    fraza = request.query_params.get("q")
    if fraza:
        qs = qs.szukaj(fraza)

    return Response(TerminWizytySerializer(qs, many=True).data)


@api_view(['GET', 'PUT', 'DELETE'])
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