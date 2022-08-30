from django.urls import path
from .views import ProduitList, ProduitDetail, CommandeList, CommandeDetail, DoleanceEluList, DoleanceEluDetail, InfoList, InfoDetail, CustumUserCreate

app_name = 'syndicat_api'

urlpatterns = [
    path('register/', CustumUserCreate.as_view(), name='create_user'),
    path('<int:pk>/', ProduitDetail.as_view(), name='detailcreate'),
    path('produits/', ProduitList.as_view(), name='produitlistcreate'),
    path('infos/', InfoList.as_view(), name='infolistcreate'),
    path('infos/<int:pk>/', InfoDetail.as_view(), name='infodetail'),
    path('commandes/<int:pk>/', CommandeDetail.as_view(), name='commandedetailcreate'),
    path('commandes/', CommandeList.as_view(), name='commandecreate'),
    path('doleanceElu/<int:pk>/', DoleanceEluDetail.as_view(), name='doleanceEludetailcreate'),
    path('doleanceElu/', DoleanceEluList.as_view(), name='commandecreate'),
]