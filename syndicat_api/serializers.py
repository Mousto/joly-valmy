from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from syndicat.models import Produit, Commande, DoleanceElu, Info, Personnel, Clinique, Service, Elu



class RegisterPersonnelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Personnel
        fields = ('email', 'user_name', 'first_name', 'civilite', 
            'phone', 'la_clinique', 'le_service', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def quelleInstance(self, instance, donnees):
        if instance == True:
            return RegisterEluSerializer(data=donnees)
       
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class RegisterEluSerializer(RegisterPersonnelSerializer):

    class Meta:
        model = Elu
        fields = RegisterPersonnelSerializer.Meta.fields + ('syndicat', 'photo', 'fonction', 'message_aux_collègues', 'disponible', )
        #extra_kwargs = {'password': {'write_only': True}}
        #extra_kwargs = RegisterPersonnelSerializer.Meta.extra_kwargs


class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = ('id', 'nom', 'prix_adulte', 'prix_enfant', 'disponible', 'photo')

class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = ['produit', 'billet_adulte', 'billet_enfant', 'valeur_totale', 'date_retrait', 'lieu_retrait', 'commanditaire']

class DoleanceEluSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoleanceElu
        fields = '__all__'
class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = ('id', 'titre', 'auteur', 'extrait', 'contenu', 'status')
class PersonnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personnel
        fields = ('civilite', 'user_name', 'first_name', 'phone', 'email', 'apropos', 'la_clinique', 'le_service')
class CliniqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinique
        fields = '__all__'
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

