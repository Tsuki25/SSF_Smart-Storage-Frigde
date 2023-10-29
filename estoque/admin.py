from django.contrib import admin

from estoque.models import *

admin.site.register(Geladeira)
admin.site.register(Lista)
admin.site.register(Produto)
admin.site.register(Item_Geladeira)
admin.site.register(Item_Lista)
admin.site.register(Log_Itens_Geladeira)

