from django.urls import path
from django.views.generic import TemplateView

app_name = 'syndicat'

urlpatterns = [
    path('', TemplateView.as_view(template_name='syndicat/index.html')),
]