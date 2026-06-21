from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from usuarios.services import nome_usuario, reservas_do_usuario

from .models import Participante, Quadra, Reserva


def quadras(request):
    """Lista quadras disponiveis e partidas publicas abertas."""
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
    partidas_abertas = [reserva for reserva in partidas_abertas if reserva.eh_partida_aberta]

    contexto = {
        'lista_de_quadras': lista_quadras,
        'tipos': Quadra.TIPOS_ESPORTE,
        'filtro_tipo': filtro_tipo,
        'partidas_abertas': partidas_abertas,
        'meu_nome': nome_usuario(request.user) if request.user.is_authenticated else request.session.get('nome_jogador', ''),
    }
    return render(request, 'quadras/quadras.html', contexto)


def reservar(request, quadra_id):
    """Abre o formulario de reserva e processa o envio."""
    quadra = get_object_or_404(Quadra, pk=quadra_id, disponivel=True)

    if request.method == 'POST':
        nome_cliente = request.POST.get('nome_cliente', '').strip()
        contato_cliente = request.POST.get('contato_cliente', '').strip()
        data_reserva = request.POST.get('data')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fim = request.POST.get('hora_fim')
        visibilidade = request.POST.get('visibilidade', 'PRI')

        if request.user.is_authenticated:
            nome_cliente = nome_cliente or nome_usuario(request.user)
            contato_cliente = request.user.email or contato_cliente

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
                    f"({reserva.vagas_totais} vagas) em {data_reserva}, das {hora_inicio} as {hora_fim}!",
                )
            else:
                messages.success(
                    request,
                    f"Reserva da {quadra.nome} feita com sucesso para {data_reserva}, das {hora_inicio} as {hora_fim}!",
                )

            return redirect('quadras')
        except ValidationError as erro:
            for mensagens_erro in erro.message_dict.values():
                for msg in mensagens_erro:
                    messages.error(request, msg)

    contexto = {
        'quadra': quadra,
        'hoje': datetime.now().date().isoformat(),
        'vagas_publica_padrao': quadra.vagas_publica_padrao,
        'nome_padrao': nome_usuario(request.user) if request.user.is_authenticated else '',
        'contato_padrao': request.user.email if request.user.is_authenticated else '',
    }
    return render(request, 'quadras/reservar.html', contexto)


@login_required
def minhas_reservas(request):
    """Lista reservas associadas ao usuario autenticado."""
    reservas = reservas_do_usuario(request.user)

    contexto = {
        'reservas': reservas,
        'nome_usuario': nome_usuario(request.user),
        'total_confirmadas': reservas.filter(status='CON').count(),
        'total_passadas': reservas.filter(data__lt=date.today()).count(),
        'total_canceladas': reservas.filter(status='CAN').count(),
    }
    return render(request, 'quadras/minhas_reservas.html', contexto)


@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id)

    if not reservas_do_usuario(request.user).filter(pk=reserva.pk).exists():
        messages.error(request, "Essa reserva nao pertence ao seu login.")
        return redirect('minhas_reservas')

    if request.method == 'POST':
        reserva.status = 'CAN'
        reserva.save()
        messages.success(request, "Reserva cancelada.")

    return redirect('minhas_reservas')


def entrar_partida(request, reserva_id):
    """Adiciona a pessoa como participante de uma partida publica."""
    reserva = get_object_or_404(Reserva, pk=reserva_id, visibilidade='PUB')

    if request.method == 'POST':
        nome = nome_usuario(request.user) if request.user.is_authenticated else request.POST.get('nome', '').strip()

        if not nome:
            messages.error(request, "Digite seu nome para entrar na partida.")
            return redirect('quadras')

        if not request.session.session_key:
            request.session.save()
        chave_sessao = request.session.session_key

        request.session['nome_jogador'] = nome

        ja_participa = Participante.objects.filter(reserva=reserva, chave_sessao=chave_sessao).exists()

        if ja_participa:
            messages.error(request, "Voce ja esta nessa partida.")
        elif reserva.esta_lotada:
            messages.error(request, "Essa partida ja esta com as vagas completas.")
        else:
            Participante.objects.create(reserva=reserva, nome=nome, chave_sessao=chave_sessao)
            messages.success(request, f"Voce entrou na partida em {reserva.quadra.nome}! Bom jogo!")

    return redirect('quadras')


def sair_partida(request, reserva_id):
    """Remove a pessoa da lista de participantes da partida publica."""
    reserva = get_object_or_404(Reserva, pk=reserva_id, visibilidade='PUB')

    if request.method == 'POST':
        chave_sessao = request.session.session_key
        participante = Participante.objects.filter(reserva=reserva, chave_sessao=chave_sessao).first()

        if participante:
            participante.delete()
            messages.success(request, "Voce saiu da partida.")
        else:
            messages.error(request, "Voce nao estava nessa partida.")

    return redirect('quadras')
