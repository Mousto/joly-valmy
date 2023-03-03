from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from syndicat.models import Produit, Panier, DoleanceElu, Info, Personnel, Clinique, Service, Elu, Commande



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
        fields = ('id','nom', 'prix_adulte', 'prix_enfant', 'photo', 'disponible')


# Voir au besoin sur github : https://github.com/beda-software/drf-writable-nested pour WritableNestedModelSerializer
class CommandeSerializer(WritableNestedModelSerializer):
    
    produit = ProduitSerializer()
    class Meta:
        model = Commande
        fields = ('id', 'produit', 'billet_adulte', 'billet_enfant', 'sous_total')


# Voir au besoin sur github : https://github.com/beda-software/drf-writable-nested pour WritableNestedModelSerializer
class PanierSerializer(WritableNestedModelSerializer):
    
    # Nous redéfinissons l'attribut 'commandes' qui porte le même nom que dans la liste des champs à afficher
    commandes = CommandeSerializer(many=True)

    class Meta:
        model = Panier
        fields = ['commandes', 'valeur_totale', 'date_retrait', 'date', 'lieu_retrait', 'commanditaire']
    

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

