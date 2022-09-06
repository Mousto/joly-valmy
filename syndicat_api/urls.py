from rest_framework.routers import DefaultRouter
from .views import ProduitList, CommandeList, DoleanceEluList, InfoList, CustumUserCreate, BlacklistTokenUpdateView

app_name = 'syndicat_api'

router = DefaultRouter()
router.register('produits', ProduitList, basename='produits-list')
router.register('commandes', CommandeList, basename='commandes-list')
router.register('doleanceElus', DoleanceEluList, basename='doleanceElu-list')
router.register('infos', InfoList, basename='info-list')
urlpatterns = router.urls
