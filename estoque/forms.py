from django.contrib.auth.models import User
from django.forms import ModelForm, ClearableFileInput, ImageField

from estoque.models import Geladeira, Produto, Lista, Item_Geladeira, Item_Lista
from django import forms
from django.forms import ModelForm

class UpdateUsuarioForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class GeladeiraForm(ModelForm):
    class Meta:
        model = Geladeira
        fields = ['nome_geladeira']

    nome_geladeira = forms.CharField(
        label='',  # Edite aqui para a label desejada
        widget=forms.TextInput(attrs={'placeholder': 'Nome da Geladeira'})
    )

class ProdutoForm(ModelForm):
    class Meta:
        model = Produto
        fields = ["nome_produto", "tipo", "imagem_produto", "unidade_medida"]

    imagem_produto = ImageField(widget=ClearableFileInput(attrs={'multiple': False}))


class ListaForm(ModelForm):
    class Meta:
        model = Lista
        fields = ['titulo_lista', 'descricao']


class ItemGeladeiraForm(ModelForm):
    class Meta:
        model = Item_Geladeira
        fields = ['validade', 'quantidade']


class ItemListaForm(ModelForm):
    class Meta:
        model = Item_Lista
        fields = ['quantidade']
