from django.contrib import admin
from home.models import Quadra
from home.models import Usuarios
# Register your models here.
#Bruno - Estou registrando os modelos aqui
admin.site.register(Usuarios)
admin.site.register(Quadra)