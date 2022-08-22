from email import message
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions, BasePermission, SAFE_METHODS
from syndicat.models import Produit, Commande
from .serializers import ProduitSerializer, CommandeSerializer

# Permission Personnalisée
class CommandeUserPermission(BasePermission):
    message = "La modification d'une commande n'est réservée qu'à son auteur."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.commanditaire.username == request.user.username

class ProduitList(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

class ProduitDetail(generics.RetrieveDestroyAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    
class CommandeList(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer

class CommandeDetail(generics.RetrieveUpdateDestroyAPIView, CommandeUserPermission):
    permission_classes = [CommandeUserPermission]
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer