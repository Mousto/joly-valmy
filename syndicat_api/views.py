from rest_framework import ( 
    viewsets,
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
from syndicat.models import Produit, Commande, DoleanceElu, Info, Personnel
from .serializers import ProduitSerializer, CommandeSerializer, DoleanceEluSerializer, InfoSerializer, RegisterUserSerializer, PersonnelSerializer

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
class ProduitList(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ProduitSerializer

    # Appel de l'objet par son nom
    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Produit, nom=item)

    # Définition d'un queryset personnalisé
    def get_queryset(self):
        return Produit.objects.all()

# CRUD sur utilisateur(Personnel)
class UserCreate(viewsets.ViewSet):
    permission_classes = [AllowAny]
    queryset = Personnel.objects.all()


    def create(self, request):
        reg_seralizer = RegisterUserSerializer(data=request.data)
        if reg_seralizer.is_valid():
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


""" class ProduitList(generics.ListCreateAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

class ProduitDetail(generics.RetrieveDestroyAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer """

""" Concrete View Classes
# CreateAPIView
Used for create-only endpoints.
# ListAPIView
Used for read-only endpoints to represent a collection of model instances.
# RetrieveAPIView
Used for read-only endpoints to represent a single model instance.
# DestroyAPIView
Used for delete-only endpoints for a single model instance.
# UpdateAPIView
Used for update-only endpoints for a single model instance.
# ListCreateAPIView
Used for read-write endpoints to represent a collection of model instances.
RetrieveUpdateAPIView
Used for read or update endpoints to represent a single model instance.
# RetrieveDestroyAPIView
Used for read or delete endpoints to represent a single model instance.
# RetrieveUpdateDestroyAPIView
Used for read-write-delete endpoints to represent a single model instance.
"""

class CommandeList(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Commande.objects.all()

    def list(self, request):
        serializer_class = CommandeSerializer(self.queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer_class = CommandeSerializer(post)
        return Response(serializer_class.data)

 
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
    permission_classes = [AllowAny]
    queryset = Info.objects.all()

    def list(self, request):
        serializer_class = InfoSerializer(self.queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer_class = InfoSerializer(post)
        return Response(serializer_class.data)



