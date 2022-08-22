from django.urls import path
from .views import ProduitList, ProduitDetail, CommandeList, CommandeDetail

app_name = 'syndicat_api'

urlpatterns = [
    path('<int:pk>/', ProduitDetail.as_view(), name='detailcreate'),
    path('', ProduitList.as_view(), name='listcreate'),
    path('commandes/<int:pk>/', CommandeDetail.as_view(), name='commandedetailcreate'),
    path('commandes/', CommandeList.as_view(), name='commandecreate'),
]