from django.db import models
# Create your models here.
#bertoncello - o django já tem o URM maius poderoso do mercado, então eu voiu criar uma tabela simples aqui e que já está pronta
class Usuarios(models.Model):
    nome = models.CharField(max_length=50) #criando a coluna 'nome' models.charfield é o tipo, o modelo, o final é quantos caracteres ao máximo
    email = models.EmailField(max_length=50) #criando a coluna emai dessa vendo só definindo o modelo sem máximo de caracteres 
