from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class Usuario(models.Model):
    nome = models.CharField(max_length=75)
    email = models.EmailField(max_length=80)
    senha = models.CharField(max_length=30)
    senha_cripto = make_password(senha, None, 'default')

    def __str__(self): #RETORNA O TITULO QUANDO CHAMA A CLASSE PELO NOME, FAZENDO EXIBIR O TITULO DA MUSICA NA
        # PAGINA DE ADM
        return self.nome

