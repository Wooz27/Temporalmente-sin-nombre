from django.shortcuts import render
from rest_framework import generics
from .models import Animal, Owner
from .serializers import AnimalSerializer, AnimalCollarSerializer


class AnimalListView (generics.ListAPIView):
    serializer_class = AnimalSerializer

    def get_queryset(self):
        return Animal.objects.filter (state = "disponible")


class AnimalCollarRetrieveView (generics.RetrieveAPIView ):
    serializer_class = AnimalCollarSerializer
    lookup_field = "public_id"

    def get_queryset(self):
        return Animal.objects.all()
