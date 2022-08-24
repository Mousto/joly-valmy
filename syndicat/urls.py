from django.urls import path
from django.views.generic import TemplateView
from .views import CustumUserCreate

app_name = 'syndicat'

urlpatterns = [
    path('', TemplateView.as_view(template_name='syndicat/index.html')),
    path('register/', CustumUserCreate.as_view(), name='create_user'),
]