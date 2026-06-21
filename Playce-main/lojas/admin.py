from django.contrib import admin
from .models import Loja, Produto, Categoria

admin.site.register(Loja)
admin.site.register(Produto)
admin.site.register(Categoria)