from django.db.models import Q

from quadras.models import Reserva


def nome_usuario(user):
    if not user or not user.is_authenticated:
        return ''

    return user.get_full_name().strip() or user.username


def filtro_reservas_usuario(user):
    nome = nome_usuario(user)
    filtros = Q(nome_cliente__iexact=user.username)

    if nome:
        filtros |= Q(nome_cliente__iexact=nome)

    if user.email:
        filtros |= Q(contato_cliente__iexact=user.email.strip())

    return filtros


def reservas_do_usuario(user):
    if not user or not user.is_authenticated:
        return Reserva.objects.none()

    return (
        Reserva.objects
        .select_related('quadra')
        .filter(filtro_reservas_usuario(user))
        .distinct()
        .order_by('-data', '-hora_inicio')
    )
