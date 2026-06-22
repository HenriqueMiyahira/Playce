from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Artigo, ItemUnitario
from quadras.models import Quadra, Reserva
from datetime import date
from django.db.models import Count

def gerenciamento(request):
    if request.method == 'POST':
        tipo_form = request.POST.get('tipo_form')

        if tipo_form == 'quadra':
            #Define a lógica para salvar uma nova quadra
            nome = request.POST.get('nome')
            tipo = request.POST.get('tipo')
            preco_hora = request.POST.get('preco_hora')
            disponivel = request.POST.get('disponivel') == 'on'

            Quadra.objects.create(
                nome=nome,
                tipo=tipo,
                preco_hora=preco_hora,
                disponivel=disponivel
            )
            messages.success(request, f"Quadra '{nome}' cadastrada com sucesso!")

        elif tipo_form == 'artigo':
            #Define a lógica para salvar um novo Artigo
            nome = request.POST.get('nome')
            codigo_base = request.POST.get('codigo_base', '000000')
            categoria = request.POST.get('categoria')
            preco = request.POST.get('preco')
            quantidade = int(request.POST.get('total_em_estoque', 0))

            novo_artigo = Artigo.objects.create(
                nome=nome,
                categoria=categoria,
                preco=preco,
                codigo_base=codigo_base,
            )

            for _ in range(quantidade):
                ItemUnitario.objects.create(artigo=novo_artigo)

            messages.success(request, f"{quantidade} items '{nome}' cadastrados com sucesso!")

        elif tipo_form == 'editar_item_unitario':
            #Define a lógica de edição de cada item unitário
            item_id = request.POST.get('item_id')
            novo_codigo = request.POST.get('codigo')
            novo_status = request.POST.get('status')

            try:
                item = ItemUnitario.objects.get(id=item_id)
                item.codigo = novo_codigo
                if hasattr(item, 'status'):
                    item.status = novo_status
                elif hasattr(item, 'condicao'):
                    item.condicao = novo_status

                item.save()
                messages.success(request, f"Item '{novo_codigo}' atualizado com sucesso!")
            except ItemUnitario.DoesNotExist:
                messages.error(request, "Erro ao tentar atualizar o item.")

        elif tipo_form == 'deletar_quadra':
            #Define o botão de deletar quadra
            quadra_id = request.POST.get('quadra_id')
            try:
                quadra = Quadra.objects.get(id=quadra_id)
                nome_deletado = quadra.nome
                quadra.delete()
                messages.success(request, f"Quadra '{nome_deletado}' e todos os seus agendamentos foram excluídos!")
            except Quadra.DoesNotExist:
                messages.error(request, "A quadra que você tentou excluir não foi encontrada.")

        elif tipo_form == 'deletar_artigo':
            #Define o botão de apagar artigo
            artigo_id = request.POST.get('artigo_id')

            try:
                artigo = Artigo.objects.get(id=artigo_id)
                nome_deletado = artigo.nome
                artigo.delete()
                messages.success(request,f"Artigo '{nome_deletado}' e todos os seus itens unitários foram excluídos!")
            except Artigo.DoesNotExist:
                messages.error(request, "O artigo que você tentou excluir não foi encontrado.")

        return redirect('gerenciamento')

    reservas_hoje_qtd = Reserva.objects.filter(data=date.today()).count() #Filtra apenas as quadras agendadas para o dia de hoje
    artigos = Artigo.objects.prefetch_related('unidades').all()
    artigos_baixa_qtd = 0

    for artigo in artigos:
        total_itens = artigo.unidades.count()
        if total_itens < 5:
            artigos_baixa_qtd += 1
    contexto = {
        'lista_de_quadras': Quadra.objects.prefetch_related('reservas').all(),
        'lista_de_artigos': artigos,
        'reservas_hoje_qtd': reservas_hoje_qtd,
        'estoque_baixo': artigos_baixa_qtd,
    }
    return render(request, 'gerenciamento/gerenciamento.html', contexto)