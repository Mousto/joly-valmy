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

from syndicat.models import Produit, Commande, DoleanceElu, Info, Utilisateur, Clinique, Service, Elu
from .serializers import ProduitSerializer, CommandeSerializer, DoleanceEluSerializer, InfoSerializer, RegisterPersonnelSerializer, PersonnelSerializer, CliniqueSerializer, ServiceSerializer, RegisterEluSerializer

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
    serializer_class = ProduitSerializer(many=True)
    queryset = Produit.objects.all()

    def get_object(self, pk):
        try:
            return Produit.objects.get(pk=pk)
        except Produit.DoesNotExist:
            raise Http404

    # Renvoie tous les produits
    def list(self, request):
        serializer_class = ProduitSerializer(self.queryset, many=True)
        return Response(serializer_class.data)

    # Renvoie un produit
    def retrieve(self, request, pk=None):
        produit = get_object_or_404(self.queryset, pk=pk)
        print('*******************',produit)
        serializer_class = ProduitSerializer(produit)
        return Response(serializer_class.data)  

    # Crée un produit
    def create(self, request):
        donnees = {
            'nom': request.data['donnees[nom]'],
            'prix_adulte': request.data['donnees[prix_adulte]'],
            'prix_enfant': request.data['donnees[prix_enfant]'],
            'photo': request.data['image'],
            'disponible': True,
        }
        reg_seralizer = ProduitSerializer(data=donnees)
        if reg_seralizer.is_valid():
            newProduit = reg_seralizer.save()
            if newProduit:
                # déserialisation avant retour réponse au front
                produit = ProduitSerializer(newProduit).data
                return Response(data=produit, status=status.HTTP_201_CREATED)
        return Response(reg_seralizer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Supprimer un produit
    def destroy(self, request, pk=None):
        produit = get_object_or_404(self.queryset, pk=pk)
        produit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class CommandeList(viewsets.ViewSet):
    #permission_classes = [CommandeUserPermission]
    permission_classes = [AllowAny]
    serializer_class = CommandeSerializer
    
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user.id
        return Commande.objects.filter(commanditaire=1)

    def list(self, request):
        print('#######################', request.user.id)
        serializer_class = CommandeSerializer(self.get_queryset(), many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        post = get_object_or_404(queryset, pk=pk)
        serializer_class = CommandeSerializer(post)
        return Response(serializer_class.data)
    
    def create(self, request):
        # Decode UTF-8 bytes to Unicode, and convert single quotes 
        # to double quotes to make it valid JSON
        my_json = request.body.decode('utf8').replace("'", '"')
        # Load the JSON to get a Python dict
        data = json.loads(my_json)
        
        #produit_id = request.data['produit']  # or however you are sending the id
        if isinstance(data, dict):
            print('#####################################', data['produits'])
            reg_seralizer = CommandeSerializer(data=request.data, many=True)
        else:
            reg_seralizer = CommandeSerializer(data=request.data)
        print('#####################################@',reg_seralizer.is_valid())
        if reg_seralizer.is_valid():
            produit_instance = get_object_or_404(Produit, id=produit_id)
            newcommande = reg_seralizer.save(produit=produit_instance)
            if newcommande:
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_seralizer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        item = Commande.objects.filter(id=pk)
        if len(item) == 1:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        commande = Commande.objects.get(id=pk)
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

 
class DoleanceEluList(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
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
