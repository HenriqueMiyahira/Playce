#aqui é onde fica a logica do usuário, o que ele quer e o que ele clica
from django.shortcuts import render

from .models import Usuarios
from .models import Quadra

# Create your views here.
def home(request):
    quadras_do_banco = Quadra.objects.all()
    contexto = {
        'lista_de_quadras': quadras_do_banco
    }

    return render(request, 'home/index.html', contexto)