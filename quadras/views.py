from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from datetime import datetime, date

from .models import Quadra, Reserva, Participante


def quadras(request):
    """Lista todas as quadras disponíveis para reserva, e as partidas
    públicas com vagas abertas para quem quiser entrar para jogar."""
    filtro_tipo = request.GET.get('tipo')

    lista_quadras = Quadra.objects.filter(disponivel=True)
    if filtro_tipo:
        lista_quadras = lista_quadras.filter(tipo=filtro_tipo)

    partidas_abertas = (
        Reserva.objects
        .select_related('quadra')
        .filter(visibilidade='PUB', status='CON', data__gte=date.today())
        .prefetch_related('participantes')
    )
    # eh_partida_aberta também garante que vagas ainda não lotaram
    partidas_abertas = [r for r in partidas_abertas if r.eh_partida_aberta]

    contexto = {
        'lista_de_quadras': lista_quadras,
        'tipos': Quadra.TIPOS_ESPORTE,
        'filtro_tipo': filtro_tipo,
        'partidas_abertas': partidas_abertas,
        'meu_nome': request.session.get('nome_jogador', ''),
    }
    return render(request, 'quadras/quadras.html', contexto)


def reservar(request, quadra_id):
    """Abre o formulário de reserva para uma quadra e processa o envio."""
    quadra = get_object_or_404(Quadra, pk=quadra_id, disponivel=True)

    if request.method == 'POST':
        nome_cliente = request.POST.get('nome_cliente', '').strip()
        contato_cliente = request.POST.get('contato_cliente', '').strip()
        data_reserva = request.POST.get('data')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fim = request.POST.get('hora_fim')
        visibilidade = request.POST.get('visibilidade', 'PRI')

        reserva = Reserva(
            quadra=quadra,
            nome_cliente=nome_cliente,
            contato_cliente=contato_cliente,
            data=data_reserva,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim,
            visibilidade=visibilidade,
        )

        try:
            reserva.full_clean()
            reserva.save()
            if visibilidade == 'PUB':
                messages.success(
                    request,
                    f"Reserva da {quadra.nome} feita e aberta para outras pessoas entrarem "
                    f"({reserva.vagas_totais} vagas) em {data_reserva}, das {hora_inicio} às {hora_fim}!"
                )
            else:
                messages.success(
                    request,
                    f"Reserva da {quadra.nome} feita com sucesso para {data_reserva}, das {hora_inicio} às {hora_fim}!"
                )
            return redirect('quadras')
        except ValidationError as erro:
            for campo, mensagens_erro in erro.message_dict.items():
                for msg in mensagens_erro:
                    messages.error(request, msg)

    contexto = {
        'quadra': quadra,
        'hoje': datetime.now().date().isoformat(),
        'vagas_publica_padrao': quadra.vagas_publica_padrao,
    }
    return render(request, 'quadras/reservar.html', contexto)


def minhas_reservas(request):
    """
    Lista reservas filtrando por contato informado, já que o login de
    usuário ainda não está disponível. Quando o sistema de usuários
    estiver pronto, isso passa a filtrar por request.user automaticamente.
    """
    contato = request.GET.get('contato', '').strip()
    reservas = Reserva.objects.select_related('quadra')

    if contato:
        reservas = reservas.filter(contato_cliente=contato)
    else:
        reservas = reservas.none()

    contexto = {
        'reservas': reservas,
        'contato': contato,
    }
    return render(request, 'quadras/minhas_reservas.html', contexto)


def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id)

    if request.method == 'POST':
        reserva.status = 'CAN'
        reserva.save()
        messages.success(request, "Reserva cancelada.")

    contato = reserva.contato_cliente
    return redirect(f"/quadras/minhas-reservas/?contato={contato}")


def entrar_partida(request, reserva_id):
    """
    Adiciona a pessoa como participante de uma partida pública.
    Como ainda não há login, pedimos o nome uma vez e guardamos na
    sessão do navegador (cookie) para identificar a pessoa nas próximas
    vezes, sem precisar digitar de novo.
    """
    reserva = get_object_or_404(Reserva, pk=reserva_id, visibilidade='PUB')

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()

        if not nome:
            messages.error(request, "Digite seu nome para entrar na partida.")
            return redirect('quadras')

        if not request.session.session_key:
            request.session.save()
        chave_sessao = request.session.session_key

        request.session['nome_jogador'] = nome

        ja_participa = Participante.objects.filter(reserva=reserva, chave_sessao=chave_sessao).exists()

        if ja_participa:
            messages.error(request, "Você já está nessa partida.")
        elif reserva.esta_lotada:
            messages.error(request, "Essa partida já está com as vagas completas.")
        else:
            Participante.objects.create(reserva=reserva, nome=nome, chave_sessao=chave_sessao)
            messages.success(request, f"Você entrou na partida em {reserva.quadra.nome}! Bom jogo!")

    return redirect('quadras')


def sair_partida(request, reserva_id):
    """Remove a pessoa (identificada pela sessão) da lista de participantes."""
    reserva = get_object_or_404(Reserva, pk=reserva_id, visibilidade='PUB')

    if request.method == 'POST':
        chave_sessao = request.session.session_key
        participante = Participante.objects.filter(reserva=reserva, chave_sessao=chave_sessao).first()

        if participante:
            participante.delete()
            messages.success(request, "Você saiu da partida.")
        else:
            messages.error(request, "Você não estava nessa partida.")

    return redirect('quadras')
