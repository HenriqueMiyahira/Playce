# lojas/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Produto, Loja

def lista_lojas(request):
    # Tela principal que mostra os parceiros/lojas
    lojas = Loja.objects.all()
    categorias = Categoria.objects.all()
    
    # Mantém o contador do topo atualizado na sessão
    carrinho_sessao = request.session.get('carrinho', {})
    total_itens = sum(carrinho_sessao.values())
    
    return render(request, 'lojas/lojas.html', {
        'lojas': lojas,
        'categorias': categorias,
        'total_itens': total_itens,
    })

def produtos_por_categoria(request, categoria_slug):
    categoria = get_object_or_404(Categoria, slug=categoria_slug)
    produtos = Produto.objects.filter(categoria=categoria)
    
    # --- LOGICA DO CARRINHO MINIMALISTA POR URL ---
    prod_id_add = request.GET.get('adicionar')
    if prod_id_add:
        carrinho = request.session.get('carrinho', {})
        carrinho[prod_id_add] = carrinho.get(prod_id_add, 0) + 1
        request.session['carrinho'] = carrinho
        return redirect(request.path + '?abrir=true')

    prod_id_rem = request.GET.get('remover')
    if prod_id_rem:
        carrinho = request.session.get('carrinho', {})
        if prod_id_rem in carrinho:
            carrinho[prod_id_rem] -= 1
            if carrinho[prod_id_rem] <= 0:
                del carrinho[prod_id_rem]
        request.session['carrinho'] = carrinho
        return redirect(request.path + '?abrir=true')

    if request.GET.get('finalizar') == 'true':
        request.session['carrinho'] = {}
        return redirect(request.path)

    # Buscar dados atualizados para renderizar a barra lateral
    carrinho_sessao = request.session.get('carrinho', {})
    itens_carrinho = []
    total_carrinho = 0
    total_itens = 0

    for prod_id, qtd in carrinho_sessao.items():
        try:
            prod = Produto.objects.get(id=prod_id)
            subtotal = prod.preco * qtd
            total_carrinho += subtotal
            total_itens += qtd
            itens_carrinho.append({'produto': prod, 'quantidade': qtd, 'subtotal': subtotal})
        except Produto.DoesNotExist:
            continue

    metodo_pagamento = request.GET.get('metodo', 'debito')
    abrir_carrinho = request.GET.get('abrir') == 'true'
    # ----------------------------------------------

    return render(request, 'lojas/categoria.html', {
        'categoria': categoria, 
        'produtos': produtos,
        'itens_carrinho': itens_carrinho,
        'total_carrinho': total_carrinho,
        'total_itens': total_itens,
        'metodo_pagamento': metodo_pagamento,
        'abrir_carrinho': abrir_carrinho,
    })