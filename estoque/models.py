from django.db import models
from django.contrib.auth.hashers import make_password, check_password

TIPOS_PRODUTOS = (
    ('BEBIDAS', 'Bebidas'),
    ('CARNES', 'Carnes'),
    ('FRUTAS', 'Frutas'),
    ('LATICINIOS', 'Laticínios'),
    ('LEGUMES', 'Legumes'),
    ('OVOS', 'Ovos'),
    ('PREPARADOS', 'Alimentos preparados'),
)


# Create your models here.
class Usuario(models.Model):
    nome_user = models.CharField(max_length=75, null=False, blank=False)
    email = models.EmailField(max_length=80, null=False, blank=False, unique=True)
    senha = models.CharField(max_length=30, null=False, blank=False)
    senha_cripto = make_password(str(senha))

    def __str__(self):
        return self.nome_user


class Geladeira(models.Model):
    nome_geladeira = models.CharField(max_length=75, null=False, blank=False)
    dt_criacao = models.DateField(auto_now=True, blank=False)
    usuarios_proprietarios = models.ManyToManyField(Usuario)

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
    tipo = models.CharField(max_length=15, choices=TIPOS_PRODUTOS)
    produto_geladeira = models.ManyToManyField(Geladeira, through='Item_Geladeira')
    produto_lista = models.ManyToManyField(Lista, through='Item_Lista')

    def __str__(self):
        return self.nome_produto

class Item_Geladeira(models.Model):
    geladeira = models.ForeignKey(Geladeira, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    validade = models.DateField(null=False, blank=False)
    quantidade = models.IntegerField(null=False, blank=False)
    def __str__(self):
        return f"{self.pk}° item da geladeira"

class Item_Lista(models.Model):
    lista = models.ForeignKey(Lista, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.pk}° item da lista"