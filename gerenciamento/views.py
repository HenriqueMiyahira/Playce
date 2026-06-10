from django.shortcuts import render
from home.models import Quadra

def gerenciamento(request):
    quadras_do_banco = Quadra.objects.all()
    contexto = {
        'lista_de_quadras': quadras_do_banco
    }
    return render(request, 'gerenciamento/gerenciamento.html', contexto)
# Create your views here.
