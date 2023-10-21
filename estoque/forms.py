from django.contrib.auth.models import User
from django.forms import ModelForm, ClearableFileInput, ImageField

from estoque.models import Geladeira, Produto


class UpdateUsuarioForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class CreateGeladeiraForm(ModelForm):

    class Meta:
        model = Geladeira
        fields = ["nome_geladeira"]

class UpdateGeladeiraForm(ModelForm):
    class Meta:
        model = Geladeira
        fields = ['nome_geladeira']

class ProdutoForm(ModelForm):

    class Meta:
        model = Produto
        fields = ["nome_produto", "tipo", "imagem_produto", "unidade_medida"]

    imagem_produto = ImageField(widget=ClearableFileInput(attrs={'multiple': False}))

