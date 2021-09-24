from django.urls import path

from .views import index, cliente, lancamentos, geracsv


urlpatterns = [
    path('', index, name='index'),
    path('cliente/<int:pk>', cliente, name='cliente'),
    path('lancamentos', lancamentos, name='lancamentos'),
    path('geracsv', geracsv, name='geracsv'),
]
