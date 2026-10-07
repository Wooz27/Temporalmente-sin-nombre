from rest_framework import serializers
from .models import Animal, Owner

class AnimalSerializer( serializers.ModelSerializer):
    # Modelo al cual estoy conectando el json parser
    class Meta:
        model = (
            Animal
        )

        fields = [
            "public_id",
            "name",
            "age",
            "race",
            "state",
            "visual1"
        ]

class CollarOwnerSerializer( serializers.ModelSerializer):
    class Meta:
        model = (
            Owner
        )

        fields = [
            "number",
            "name"
        ]

class AnimalCollarSerializer ( serializers.ModelSerializer):

    owner = CollarOwnerSerializer(read_only=True)

    class Meta:
        model = (
            Animal
        )

        fields = [
            "public_id",
            "name", 
            "age",
            "race",
            "state",
            "visual1",
            "owner"
        ]

