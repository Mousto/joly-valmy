from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from syndicat.models import Produit

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'