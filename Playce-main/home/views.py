#aqui é onde fica a logica do usuário, o que ele quer e o que ele clica
from django.shortcuts import render
from .models import Usuarios
from .models import Quadra

# Create your views here.
def home(request):
    tipos_no_banco = Quadra.objects.values_list('tipo', flat=True).distinct()
    categorias_map = dict(Quadra.TIPOS_ESPORTE)
    quadras_do_banco = Quadra.objects.all()
    esportes_disponiveis = []
    for codigo in tipos_no_banco:
        if codigo in categorias_map:
            esportes_disponiveis.append({
                'codigo': codigo,
                'nome': categorias_map[codigo]
            })
    contexto = {
        'esportes': esportes_disponiveis
    }

    return render(request, 'home/index.html', contexto)