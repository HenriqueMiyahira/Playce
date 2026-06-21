from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.usuarios,
        name='usuarios'
    ),

    path(
        'login/',
        views.login_usuario,
        name='login'
    ),

    path(
        'cadastro/',
        views.cadastro,
        name='cadastro'
    ),

    path(
        'logout/',
        views.logout_usuario,
        name='logout'
    ),

    path(
        'perfil/',
        views.perfil,
        name='perfil'
    ),

    path(
        'perfil/editar/',
        views.editar_perfil,
        name='editar_perfil'
    ),
]
