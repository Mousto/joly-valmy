from django.http import Http404
from rest_framework import ( 
    viewsets,
    generics,
    status,)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import (
    IsAdminUser, 
    DjangoModelPermissions,
    BasePermission, 
    SAFE_METHODS, 
    IsAuthenticatedOrReadOnly, 
    IsAuthenticated,
    AllowAny,)
from django.shortcuts import get_object_or_404
import json
from datetime import datetime

from syndicat.models import Produit, Panier, DoleanceElu, Info, Utilisateur, Clinique, Service, Elu, Commande
from .serializers import ProduitSerializer, PanierSerializer, DoleanceEluSerializer, InfoSerializer, RegisterPersonnelSerializer, PersonnelSerializer, CliniqueSerializer, ServiceSerializer, RegisterEluSerializer, CommandeSerializer

""" # Création d'un utilisateur
class CustumUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_seralizer = RegisterUserSerializer(data=request.data)
        if reg_seralizer.is_valid():
            newuser = reg_seralizer.save()
            if newuser:
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_seralizer.errors, status=status.HTTP_400_BAD_REQUEST) """

# BLACKLIST
class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            print('*********** TOUT VA BIEN ******************')
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# Permission Personnalisée pour les commandes
class CommandeUserPermission(BasePermission):
    message = "La modification d'une commande n'est réservée qu'à son auteur."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        print('*******************', request.method in SAFE_METHODS)
        return obj.commanditaire == request.user

# Permission Personnalisée pour les DoleanceElu
class DoleanceEluPermission(BasePermission):
    message = "La modification d'une doléance n'est réservée qu'à son auteur."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.emeteur == request.user

# Permission Personnalisée pour les Infos
class InfoPermission(BasePermission):
    message = "La modification d'une information n'est réservée qu'à son auteur."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.auteur == request.user

# Utilisation de ModelViewSet
class ProduitList(viewsets.ViewSet):
    permission_classes = [AllowAny]
    serializer_class = ProduitSerializer
    queryset = Produit.objects.all()

    def get_object(self, pk):
        try:
            return Produit.objects.get(pk=pk)
        except Produit.DoesNotExist:
            raise Http404

    # Renvoie tous les produits
    def list(self, request):
        serializer_class = ProduitSerializer(self.queryset,many=True)
        return Response(serializer_class.data)

    # Renvoie un produit(methode get)
    def retrieve(self, request, pk=None):
        produit = get_object_or_404(self.queryset, pk=pk)
        print('*******************',produit)
        serializer_class = ProduitSerializer(produit)
        return Response(serializer_class.data)  

    # Crée un produit(methode post)
    def create(self, request):
        donnees = {
            'nom': request.data['nom'],#request.data['donnees[nom]'],
            'prix_adulte': request.data['prix_adulte'],#request.data['donnees[prix_adulte]'],
            'prix_enfant': request.data['prix_enfant'],#request.data['donnees[prix_enfant]'],
            # 'billet_adulte': request.data['donnees[billet_adulte]'],
            # 'billet_enfant': request.data['donnees[billet_enfant]'],
            #'photo': request.data['image'],
            'disponible': True,
            #'commandes':request.data['commandes']
        }
        reg_seralizer = ProduitSerializer(data=donnees)
        if reg_seralizer.is_valid():
            newProduit = reg_seralizer.save()
            if newProduit:
                # déserialisation avant retour réponse au front
                produit = ProduitSerializer(newProduit).data
                return Response(data=produit, status=status.HTTP_201_CREATED)
        return Response(reg_seralizer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Supprimer un produit(methode post)
    def destroy(self, request, pk=None):
        produit = get_object_or_404(self.queryset, pk=pk)
        produit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    #(methode patch)
    def partial_update(self, request, pk=None):
        produit = get_object_or_404(self.queryset, pk=pk)
        # Decode UTF-8 bytes to Unicode, and convert single quotes 
        # to double quotes to make it valid JSON
        my_json = request.body.decode('utf8').replace("'", '"')
        #print('************************',my_json)

        # Load the JSON to get a Python dict
        data = json.loads(my_json)
        #print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$',type(data))    
        serializer = ProduitSerializer(produit, data, partial=True) # set partial=True to update a data partially
        
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        

    # Appel de l'objet par son nom
    # def get_object(self, queryset=None, **kwargs):
    #     item = self.kwargs.get('pk')
    #     return get_object_or_404(Produit, nom=item)

    
    # Définition d'un queryset personnalisé
    # def get_queryset(self):
    #     return Produit.objects.all()

# CRUD sur utilisateur(Personnel)
class UserCreate(viewsets.ViewSet):
    permission_classes = [AllowAny]
    queryset = Utilisateur.objects.all()

    def create(self, request):
        reg_seralizer = ""
        print('**************',request.data['elu'])
        if(request.data['elu'] == True):
            reg_seralizer = RegisterEluSerializer(data=request.data)
        else:
            reg_seralizer = RegisterPersonnelSerializer(data=request.data)
        if reg_seralizer.is_valid():
            print('valid')
            newuser = reg_seralizer.save()
            if newuser:
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_seralizer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        serializer_class = PersonnelSerializer(self.queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer_class = PersonnelSerializer(post)
        return Response(serializer_class.data)


    # def list(self, request):
    #     pass

    # def create(self, request):
    #     pass

    # def retrieve(self, request, pk=None):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass


class PanierList(viewsets.ViewSet):
    #permission_classes = [CommandeUserPermission]
    permission_classes = [AllowAny]
    serializer_class = PanierSerializer
    
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user.id
        return Panier.objects.filter(commanditaire=1)

    def list(self, request):
        #print('#######################', request.user.id)
        serializer_class = PanierSerializer(self.get_queryset(), many=True)
        print('cocu')
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        post = get_object_or_404(queryset, pk=pk)
        serializer_class = PanierSerializer(post)
        return Response(serializer_class.data)
    
    
    
    def create(self, request):
        # Decode UTF-8 bytes to Unicode, and convert single quotes 
        # to double quotes to make it valid JSON
        my_json = request.body.decode('utf8').replace("'", '"')
        # Load the JSON to get a Python dict
        requete = json.loads(my_json)
        
        # format
        formateur = '%Y-%m-%d'
        
        #Fonction permettant de mapper requete['commandes'].
        def f(e):
            return {
                'produit': {
                    'id': e['id'],
                    'nom': e['nom'],
                    'prix_adulte': e['prix_adulte'],
                    'prix_enfant': e['prix_enfant'],
                    'disponible': True,
                },
                'billet_adulte': e['billet_adulte'],
                'billet_enfant': e['billet_enfant'],
                'sous_total': e['sous_total'],
                }
        commandes = map(f, requete['commandes'])
        
        #Remarque : sur les dates ci-dessous, il a fallut faire un slice pour récupérer les 10 premiers caratères, les formater avec le pattern formateur et convertir le datetime obtenu en date d'ou le date() de fin
        donnees = {
            'commandes': list(commandes),
            'valeur_totale': requete['valeur_totale'],
            "date_retrait": datetime.strptime(requete['date_retrait'][:10], formateur).date(),
            "date": datetime.strptime(requete['date'][:10], formateur).date(),
            "lieu_retrait": requete['lieu_retrait'],
            "commanditaire": requete['commanditaire']
        }
        
        reg_seralizer = PanierSerializer(data=donnees)
        if reg_seralizer.is_valid():
            panier = reg_seralizer.save()
            if panier:
                # déserialisation avant retour réponse au front
                panier = PanierSerializer(panier).data
                return Response(data=panier, status=status.HTTP_201_CREATED)
        print(reg_seralizer.errors)
        return Response(reg_seralizer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        item = Panier.objects.filter(id=pk)
        if len(item) == 1:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        commande = Panier.objects.get(id=pk)
        print(request.data)
        data = {
            "billet_adulte": request.data['billet_adulte'],
            "billet_enfant": request.data['billet_enfant'],
            "valeur_totale": request.data['valeur_totale'],
            "date_retrait": request.data['date_retrait'],
            "lieu_retrait": request.data['lieu_retrait'],
            }
        serializer = self.serializer_class(commande, data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        print('Je modifie une commande ici')
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        print('************************Partial update')
        return Response({'http_method': 'PATCH'})


class CommandeList(viewsets.ViewSet):
    #permission_classes = [CommandeUserPermission]
    permission_classes = [AllowAny]
    serializer_class = CommandeSerializer
    queryset = Commande.objects.all()

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user.id
        return Panier.objects.filter(commanditaire=1)

    def list(self, request):
        print('#######################', request.user.id)
        serializer_class = CommandeSerializer(self.queryset, many=True)
        return Response(serializer_class.data)
 
    def create(self, request):
        donnees = {
            'produit': request.data['produit'],
            'billet_adulte': request.data['billet_adulte'],
            'billet_enfant': request.data['billet_enfant'],
            'sous_total': request.data['sous_total'],
        }
        reg_seralizer = CommandeSerializer(data=donnees)
        if reg_seralizer.is_valid():
            #print('*******************', reg_seralizer.validated_data['produit'])
            newCommande = reg_seralizer.save()
            if newCommande:
                # déserialisation avant retour réponse au front
                commande = CommandeSerializer(newCommande).data
                return Response(data=commande, status=status.HTTP_201_CREATED)
        print(reg_seralizer.errors)
        return Response(reg_seralizer.errors, status=status.HTTP_400_BAD_REQUEST)



class DoleanceEluList(viewsets.ViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = DoleanceElu.objects.all()

    def list(self, request):
        serializer_class = DoleanceEluSerializer(self.queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer_class = DoleanceEluSerializer(post)
        return Response(serializer_class.data)



class InfoList(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Info.objects.all()

    def list(self, request):
        serializer_class = InfoSerializer(self.queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer_class = InfoSerializer(post)
        return Response(serializer_class.data)

class Cliniques(viewsets.ViewSet):
    permission_classes = [AllowAny]
    queryset = Clinique.objects.all()

    def list(self, request):
        serializer_class = CliniqueSerializer(self.queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer_class = CliniqueSerializer(post)
        return Response(serializer_class.data)
class Services(viewsets.ViewSet):
    permission_classes = [AllowAny]
    queryset = Service.objects.all()

    def list(self, request):
        serializer_class = ServiceSerializer(self.queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer_class = ServiceSerializer(post)
        return Response(serializer_class.data)


class ListServicesByCliniqueIdView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ServiceSerializer

    def get_queryset(self):
        clinique = self.kwargs['pk']
        return Service.objects.filter(clinique=clinique)
