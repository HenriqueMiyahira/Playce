from django.shortcuts import render, redirect
from .models import Produto
# APENAS ENTENDENDO ESSE BAGULHO, DEPOIS EU FAÇO O RESTO KKKK
def home(request):
    # Inicializa o carrinho se ele não existir na sessão do usuário
    if 'carrinho' not in request.session:
        request.session['carrinho'] = []

    # Se o usuário clicou no botão "Adicionar ao Carrinho"
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        
        if produto_id:
            produto = Produto.objects.get(id=produto_id)
            
            # Adiciona o item na lista do Python (Sessão)
            item = {
                'id': produto.id,
                'nome': produto.nome,
                'preco': float(produto.preco)
            }
            
            carrinho_atual = request.session['carrinho']
            carrinho_atual.append(item)
            request.session['carrinho'] = carrinho_atual
            
        return redirect('home')

    # Busca os produtos para exibir no catálogo padrão
    produtos_do_catalogo = Produto.objects.all()
    itens_do_carrinho = request.session['carrinho']
    
    # Cálculos feitos no Python
    total_carrinho = sum(item['preco'] for item in itens_do_carrinho)
    quantidade_itens = len(itens_do_carrinho)

    contexto = {
        'produtos': produtos_do_catalogo,
        'carrinho': itens_do_carrinho,
        'total': total_carrinho,
        'quantidade': quantidade_itens
    }
    
    return render(request, 'views.html', contexto)