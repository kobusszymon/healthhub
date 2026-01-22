from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ProfilUzytkownika, Pomiar, Lek, Aktywnosc
from .serializers import ProfilUzytkownikaSerializer, PomiarSerializer, LekSerializer, AktywnoscSerializer

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