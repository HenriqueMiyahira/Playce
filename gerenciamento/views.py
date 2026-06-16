from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Artigo, ItemUnitario
from home.models import Quadra


def gerenciamento(request):
    if request.method == 'POST':
        tipo_form = request.POST.get('tipo_form')

        # === LÓGICA PARA SALVAR A QUADRA ===
        if tipo_form == 'quadra':
            nome = request.POST.get('nome')
            tipo = request.POST.get('tipo')
            preco_hora = request.POST.get('preco_hora')
            disponivel = request.POST.get('disponivel') == 'on'  # Checkbox retorna 'on' se marcado

            Quadra.objects.create(
                nome=nome,
                tipo=tipo,
                preco_hora=preco_hora,
                disponivel=disponivel
            )
            messages.success(request, f"Quadra '{nome}' cadastrada com sucesso!")


        elif tipo_form == 'artigo':
            nome = request.POST.get('nome')
            codigo_base = request.POST.get('codigo_base', '000000')
            categoria = request.POST.get('categoria')
            preco = request.POST.get('preco')
            quantidade = int(request.POST.get('total_em_estoque', 0))

            # 1. Cria o modelo pai (o catálogo)
            novo_artigo = Artigo.objects.create(
                nome=nome,
                categoria=categoria,
                preco=preco,
                codigo_base=codigo_base,
            )

            for _ in range(quantidade):
                ItemUnitario.objects.create(artigo=novo_artigo)

            messages.success(request, f"{quantidade} items '{nome}' cadastrados com sucesso!")

    contexto = {
        'lista_de_quadras': Quadra.objects.all(),
        'lista_de_artigos': Artigo.objects.all(),
    }
    return render(request, 'gerenciamento/gerenciamento.html', contexto)