#aqui é onde fica a logica do usuário, o que ele quer e o que ele clica
from django.shortcuts import render

from .models import Usuarios

# Create your views here.
def home(request):
    #user = Usuarios(nome='Pedro', email='pedrobardo@gmail.com')
    #user.save()
    #usuario = Usuarios.objects.get(id=11)
    #usuario.delete()

    return render(request, 'home/index.html')