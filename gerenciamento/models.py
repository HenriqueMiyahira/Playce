from django.db import models

class Artigo(models.Model):
    CATEGORIA_CHOICES = [
        ('equipamento', 'Equipamento'),
        ('vestuario', 'Vestuário'),
        ('alimento', 'Alimento'),
    ]

    nome = models.CharField(max_length=200, verbose_name="Nome do Artigo")
    categoria = models.CharField(max_length=30, choices=CATEGORIA_CHOICES, default='equipamento')
    preco = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Preço (un)")

    class Meta:
        verbose_name = "Artigo"
        verbose_name_plural = "Artigos"
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def total_em_estoque(self):
        return self.unidades.count()


class ItemUnitario(models.Model):
    CONDICAO_CHOICES = [
        ('excelente', 'Excelente'),
        ('desgastado', 'Desgastado'),
        ('manutencao', 'Em Manutenção'),
        ('pronto_para_uso', 'Pronto p/ Uso'),
    ]

    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='unidades')

    codigo = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        verbose_name="Código/Etiqueta"
    )

    condicao = models.CharField(max_length=30, choices=CONDICAO_CHOICES, default='excelente')
    disponivel = models.BooleanField(default=True, verbose_name="Pronto para Uso?")

    class Meta:
        verbose_name = "Item Unitário"
        verbose_name_plural = "Itens Unitários"
        ordering = ['codigo']

    def __str__(self):
        return f"{self.artigo.nome} ({self.codigo})"

# Create your models here.
