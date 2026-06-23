from django.db import models
from django.core.exceptions import ValidationError


class Quadra(models.Model):
    TIPOS_ESPORTE = [
        ('FUT', 'Futebol'),
        ('VOL', 'Vôlei'),
        ('BAS', 'Basquete'),
        ('TEN', 'Tênis'),
    ]

    VAGAS_POR_ESPORTE = {
        'FUT': 10,  # 5 vs 5
        'VOL': 12,  # 6 vs 6
        'BAS': 10,  # 5 vs 5
        'TEN': 2,   # 1 vs 1
    }

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=3, choices=TIPOS_ESPORTE)
    preco_hora = models.DecimalField(max_digits=6, decimal_places=2)
    disponivel = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Quadra"
        verbose_name_plural = "Quadras"
        ordering = ['nome']

    def __str__(self):
        return self.nome

    @property
    def vagas_publica_padrao(self):
        return self.VAGAS_POR_ESPORTE.get(self.tipo, 10)


class Reserva(models.Model):
    STATUS_CHOICES = [
        ('PEN', 'Pendente'),
        ('CON', 'Confirmada'),
        ('CAN', 'Cancelada'),
    ]

    VISIBILIDADE_CHOICES = [
        ('PUB', 'Pública'),
        ('PRI', 'Privada'),
    ]

    quadra = models.ForeignKey(Quadra, on_delete=models.CASCADE, related_name='reservas')

    usuario = models.ForeignKey(
        'home.Usuarios',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reservas',
    )

    nome_cliente = models.CharField(max_length=100, verbose_name="Nome do responsável")
    contato_cliente = models.CharField(max_length=30, verbose_name="Telefone/Contato")

    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='PEN')

    visibilidade = models.CharField(max_length=3, choices=VISIBILIDADE_CHOICES, default='PRI')

    vagas_totais = models.PositiveSmallIntegerField(null=True, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['data', 'hora_inicio']

    def __str__(self):
        return f"{self.quadra.nome} - {self.data} ({self.hora_inicio}-{self.hora_fim})"

    def clean(self):
        if self.hora_inicio and self.hora_fim and self.hora_inicio >= self.hora_fim:
            raise ValidationError("O horário de início deve ser antes do horário de fim.")

        if self.quadra_id and self.data and self.hora_inicio and self.hora_fim:
            conflitos = Reserva.objects.filter(
                quadra=self.quadra,
                data=self.data,
                status__in=['PEN', 'CON'],
            ).exclude(pk=self.pk)

            for reserva in conflitos:
                if self.hora_inicio < reserva.hora_fim and self.hora_fim > reserva.hora_inicio:
                    raise ValidationError(
                        f"Essa quadra já está reservada de {reserva.hora_inicio} às {reserva.hora_fim} nesse dia."
                    )

    def save(self, *args, **kwargs):
        if self.visibilidade == 'PUB' and not self.vagas_totais:
            self.vagas_totais = self.quadra.vagas_publica_padrao
        if self.visibilidade == 'PRI':
            self.vagas_totais = None
        super().save(*args, **kwargs)

    @property
    def vagas_ocupadas(self):
        return self.participantes.count()

    @property
    def vagas_disponiveis(self):
        if not self.vagas_totais:
            return 0
        return max(self.vagas_totais - self.vagas_ocupadas, 0)

    @property
    def esta_lotada(self):
        return self.visibilidade == 'PUB' and self.vagas_disponiveis <= 0

    @property
    def eh_partida_aberta(self):
        """Partida pública, aprovada (confirmada), com vagas disponíveis."""
        return self.visibilidade == 'PUB' and self.status != 'CAN' and not self.esta_lotada


class Participante(models.Model):
    """
    Pessoa que entrou para jogar em uma partida pública.
    Como ainda não existe login, o nome é guardado numa sessão simples
    no navegador (cookie de sessão do Django) para não precisar digitar
    de novo a cada visita.
    """
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='participantes')
    nome = models.CharField(max_length=100)
    chave_sessao = models.CharField(max_length=40, blank=True)
    entrou_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Participante"
        verbose_name_plural = "Participantes"
        ordering = ['entrou_em']
        constraints = [
            models.UniqueConstraint(
                fields=['reserva', 'chave_sessao'],
                name='participante_unico_por_sessao',
                condition=models.Q(chave_sessao__gt=''),
            )
        ]

    def __str__(self):
        return f"{self.nome} em {self.reserva}"
