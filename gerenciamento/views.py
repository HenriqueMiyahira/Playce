from django.shortcuts import render
from home.models import Quadra
from .models import Artigo, ItemUnitario

def gerenciamento(request):
    quadras_do_banco = Quadra.objects.all()
    contexto = {
        'lista_de_quadras': quadras_do_banco,
        'lista_de_artigos': Artigo.objects.all(),
        'lista_de_itemunitarios': ItemUnitario.objects.all(),
    }
    return render(request, 'gerenciamento/gerenciamento.html', contexto)
# Create your views here.
