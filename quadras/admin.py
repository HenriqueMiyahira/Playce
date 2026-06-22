from django.contrib import admin
from .models import Quadra, Reserva, Participante


@admin.register(Quadra)
class QuadraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'preco_hora', 'disponivel')
    list_filter = ('tipo', 'disponivel')
    search_fields = ('nome',)


class ParticipanteInline(admin.TabularInline):
    model = Participante
    extra = 0


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('quadra', 'nome_cliente', 'data', 'hora_inicio', 'hora_fim', 'status', 'visibilidade', 'vagas_totais')
    list_filter = ('status', 'visibilidade', 'quadra')
    search_fields = ('nome_cliente', 'contato_cliente')
    date_hierarchy = 'data'
    inlines = [ParticipanteInline]


@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'reserva', 'entrou_em')
    search_fields = ('nome',)
