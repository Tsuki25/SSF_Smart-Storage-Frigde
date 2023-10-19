from django.contrib.auth.models import User
from django.forms import ModelForm

from estoque.models import Geladeira


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