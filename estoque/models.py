from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import request

TIPOS_PRODUTOS = (
    ('BEBIDAS', 'Bebidas'),
    ('BEBIDAS_ALC', 'Bebidas alcoólicas'),
    ('CARNES', 'Carnes'),
    ('FRUTAS', 'Frutas'),
    ('LATICINIOS', 'Laticínios'),
    ('LEGUMES', 'Legumes'),
    ('OVOS', 'Ovos'),
    ('PREPARADOS', 'Alimentos preparados'),
)

UNIDADES_MEDIDA = (
    ('UN', 'un'),
    ('G', 'g'),
    ('KG', 'kg'),
    ('ML', 'ml'),
    ('L', 'lt'),
)

class Geladeira(models.Model):
    nome_geladeira = models.CharField(max_length=75, null=False, blank=False)
    dt_criacao = models.DateField(auto_now=True, blank=False)
    usuarios_proprietarios = models.ManyToManyField(User)

    def __str__(self):
        return self.nome_geladeira


class Lista(models.Model):
    titulo_lista = models.CharField(max_length=75, null=False, blank=False)
    descricao = models.TextField(max_length=700, blank=False)
    dt_criacao = models.DateField(auto_now=True, blank=False)
    geladeira = models.ForeignKey("Geladeira", on_delete=models.CASCADE, related_name='listas')

    def __str__(self):
        return self.titulo_lista


class Produto(models.Model):
    nome_produto = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS_PRODUTOS)
    imagem_produto = models.ImageField(upload_to='media', default='media/default_image_produtos')
    unidade_medida = models.tipo = models.CharField(max_length=20, choices=UNIDADES_MEDIDA, default='un')
    produto_geladeira = models.ManyToManyField(Geladeira, through='Item_Geladeira')
    produto_lista = models.ManyToManyField(Lista, through='Item_Lista')

    def __str__(self):
        return self.nome_produto

class Log_Itens_Geladeira(models.Model):
    item_geladeira = models.ForeignKey('Item_Geladeira', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    geladeira = models.ForeignKey(Geladeira, on_delete=models.CASCADE)
    dt_modificacao = models.DateField(auto_now=True, blank=False)
    descricao = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f"{self.item_geladeira.produto.nome_produto} - {self.dt_modificacao}"

class Item_Geladeira(models.Model):
    geladeira = models.ForeignKey(Geladeira, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    validade = models.DateField(null=False, blank=False)
    quantidade = models.IntegerField(null=False, blank=False)
    logs = models.ManyToManyField(Log_Itens_Geladeira, related_name='itens_geladeira', blank=True)
    def __str__(self):
        return f"{self.produto.nome_produto} - {self.geladeira.nome_geladeira}"

class Item_Lista(models.Model):
    lista = models.ForeignKey(Lista, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.produto.nome_produto} - {self.lista.titulo_lista}"

