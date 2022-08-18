from rest_framework import generics
from syndicat.models import Produit
from .serializers import ProduitSerializer

class ProduitList(generics.ListCreateAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

class ProduitDetail(generics.RetrieveDestroyAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer