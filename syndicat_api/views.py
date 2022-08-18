from rest_framework import generics
from syndicat.models import Produit
from .serializers import ProduitSerializer

class ProduitList(generics.ListCreateAPIView):
    queryset = Produit.produitdispo.all()
    serializer_class = ProduitSerializer

class ProduitDetail(generics.RetrieveDestroyAPIView):
    pass