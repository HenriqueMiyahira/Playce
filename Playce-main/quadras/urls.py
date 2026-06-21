from django.urls import path
from . import views

urlpatterns = [
    path('', views.quadras, name='quadras'),
    path('<int:quadra_id>/reservar/', views.reservar, name='reservar_quadra'),
    path('minhas-reservas/', views.minhas_reservas, name='minhas_reservas'),
    path('reserva/<int:reserva_id>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),
    path('partida/<int:reserva_id>/entrar/', views.entrar_partida, name='entrar_partida'),
    path('partida/<int:reserva_id>/sair/', views.sair_partida, name='sair_partida'),
]