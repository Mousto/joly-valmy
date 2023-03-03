from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import ProduitList, PanierList, DoleanceEluList, InfoList, UserCreate, BlacklistTokenUpdateView, Cliniques, Services, ListServicesByCliniqueIdView

app_name = 'syndicat_api'

router = DefaultRouter()
router.register('produits', ProduitList, basename='produits')
router.register('panier', PanierList, basename='panier')
router.register('doleanceElus', DoleanceEluList, basename='doleanceElu')
router.register('infos', InfoList, basename='info')
router.register('userCreate', UserCreate, basename='user-create')
router.register('cliniques', Cliniques, basename='cliniques')
router.register('services', Services, basename='services')
urlpatterns = [
    path('', include(router.urls)),
    path('serviceParClinique-list/<pk>/', ListServicesByCliniqueIdView.as_view(), name='serviceParClinique'),
    path('user/logout/blacklist/', BlacklistTokenUpdateView.as_view(), name='blacklistToken'),
]
#urlpatterns = router.urls
