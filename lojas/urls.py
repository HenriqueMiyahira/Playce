from django.urls import path
from . import views

urlpatterns = [
    path('', views.lojas, name='lojas')
]