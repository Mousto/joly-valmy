from email import message
from urllib import response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
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
from syndicat.models import Produit, Commande, DoleanceElu, Info
from .serializers import ProduitSerializer, CommandeSerializer, DoleanceEluSerializer, InfoSerializer, RegisterUserSerializer

# Création d'un utilisateur
class CustumUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_seralizer = RegisterUserSerializer(data=request.data)
        if reg_seralizer.is_valid():
            newuser = reg_seralizer.save()
            if newuser:
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_seralizer.errors, status=status.HTTP_400_BAD_REQUEST)

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

class ProduitList(generics.ListCreateAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

class ProduitDetail(generics.RetrieveDestroyAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    
class CommandeList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer

class CommandeDetail(generics.RetrieveUpdateDestroyAPIView, CommandeUserPermission):
    permission_classes = [CommandeUserPermission]
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer

class DoleanceEluList(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = DoleanceElu.objects.all()
    serializer_class = DoleanceEluSerializer

class DoleanceEluDetail(generics.RetrieveUpdateDestroyAPIView, DoleanceEluPermission):
    permission_classes = [DoleanceEluPermission]
    queryset = DoleanceElu.objects.all()
    serializer_class = DoleanceEluSerializer

class InfoList(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Info.infoObjects.all()
    serializer_class = InfoSerializer

class InfoDetail(generics.RetrieveUpdateDestroyAPIView, InfoPermission):
    permission_classes = [InfoPermission]
    queryset = Info.objects.all()
    serializer_class = InfoSerializer

