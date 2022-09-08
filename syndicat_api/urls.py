from rest_framework.routers import DefaultRouter
from .views import ProduitList, CommandeList, DoleanceEluList, InfoList, UserCreate, BlacklistTokenUpdateView

app_name = 'syndicat_api'

router = DefaultRouter()
router.register('produits', ProduitList, basename='produits')
router.register('commandes', CommandeList, basename='commandes')
router.register('doleanceElus', DoleanceEluList, basename='doleanceElu')
router.register('infos', InfoList, basename='info')
router.register('userCreate', UserCreate, basename='user-create')
urlpatterns = router.urls
