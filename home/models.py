from django.db import models
# Create your models here.
#bertoncello - o django já tem o URM maius poderoso do mercado, então eu voiu criar uma tabela simples aqui e que já está pronta
class Usuarios(models.Model):
    nome = models.CharField(max_length=50) #criando a coluna 'nome' models.charfield é o tipo, o modelo, o final é quantos caracteres ao máximo
    email = models.EmailField(max_length=50) #criando a coluna emai dessa vendo só definindo o modelo sem máximo de caracteres 

# Bruno - Aqui vou criar a tabela para as quadras que serão gerenciadas no sistema, podem adicionar mais depois, colocar algumas pra testar
class Quadra(models.Model):
    TIPOS_ESPORTE = [
        ('FUT', 'Futebol'),
        ('VOL', 'Vôlei'),
        ('BAS', 'Basquete'),
    ]
    
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=3, choices=TIPOS_ESPORTE)
    preco_hora = models.DecimalField(max_digits=6, decimal_places=2)
    disponivel = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome