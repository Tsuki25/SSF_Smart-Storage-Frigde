from django.contrib import admin

from estoque.models import *

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Geladeira)
admin.site.register(Lista)
admin.site.register(Produto)
admin.site.register(Item_Geladeira)
admin.site.register(Item_Lista)
