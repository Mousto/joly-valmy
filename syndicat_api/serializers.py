from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from syndicat.models import Produit, Commande

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'

class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = '__all__'