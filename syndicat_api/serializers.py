from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from syndicat.models import Produit, Commande, DoleanceElu, Info

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'

class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = '__all__'

class DoleanceEluSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoleanceElu
        fields = '__all__'
class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = ('id', 'titre', 'auteur', 'extrait', 'contenu', 'status')