
from django.urls import path
from . import views

app_name = 'lojas'

urlpatterns = [
    path('', views.lista_lojas, name='lista_lojas'),
    path('categoria/<slug:categoria_slug>/', views.produtos_por_categoria, name='produtos_por_categoria'),
]