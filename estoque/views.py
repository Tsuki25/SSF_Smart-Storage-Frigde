from allauth.account.views import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.forms import ImageField, ClearableFileInput
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView, DeleteView, CreateView, ListView, DetailView

from estoque.forms import UpdateUsuarioForm, CreateGeladeiraForm, UpdateGeladeiraForm, ProdutoForm
from estoque.models import Geladeira, Produto, Item_Geladeira


class Homepage(TemplateView):
    template_name = "homepage.html"


class Profile(LoginRequiredMixin, UpdateView):
    template_name = "profile.html"
    model = User
    form_class = UpdateUsuarioForm

    def get_success_url(self):
        return reverse('estoque:homepage')

    def get_object(self, queryset=None):
        self.object = get_object_or_404(User, username=self.request.user)
        return self.object


class DeleteAccount(DeleteView):
    template_name = "delete.html"
    model = User
    success_url = reverse_lazy('estoque:homepage')

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        logout(request)
        user.delete()

        return HttpResponseRedirect(self.success_url)


class CreateGeladeira(CreateView, LoginRequiredMixin):
    template_name = "form_geladeira.html"
    model = Geladeira
    form_class = CreateGeladeiraForm
    success_url = reverse_lazy('estoque:geladeiras')

    def form_valid(self, form):
        geladeira = form.save(commit=False)
        geladeira.save()
        geladeira.usuarios_proprietarios.add(self.request.user)

        return super().form_valid(form)


class Geladeiras(ListView):
    template_name = "home_geladeiras.html"
    model = Geladeira

    def get_context_data(self, **kwargs):  # DEFINE O CONTEXTO DE GELADEIRAS
        context = super().get_context_data(**kwargs)
        context['geladeiras'] = Geladeira.objects.all()  # PEGA TODOS OS OBJETOS GELADEIRA E ADICIONA A UMA LISTA
        return context


class DetalhesGeladeira(LoginRequiredMixin, DetailView):
    template_name = "detalhes_geladeira.html"
    model = Geladeira

    # FALTA CONSEGUIR MEXER NO VALOR DOS ITENS DIRETAMENTE NA GELADEIRA
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_geladeira'] = Item_Geladeira.objects.all()#PEGA CADA ITEM DA GELADEIRA DE ACORDO COM A TABELA INTERMEDIARIA
        return context


class UpdateGeladeira(UpdateView):
    template_name = "form_geladeira.html"
    model = Geladeira
    form_class = UpdateGeladeiraForm

    def get_success_url(self):
        return reverse('estoque:detalhes_geladeira', args=[self.object.pk])

class DeleteGeladeira(DeleteView):
    template_name = "delete.html"
    model = Geladeira
    success_url = reverse_lazy('estoque:geladeiras')


class CreateProduto(CreateView, LoginRequiredMixin):
    template_name = "form_produto.html"
    model = Produto
    form_class = ProdutoForm
    success_url = reverse_lazy('estoque:geladeiras')

class UpdateProduto(UpdateView, LoginRequiredMixin):
    template_name = "form_produto.html"
    model = Produto
    form_class = ProdutoForm
    success_url = reverse_lazy('estoque:geladeiras')

class DeleteProduto(DeleteView):
    template_name = "delete.html"
    model = Produto
    success_url = reverse_lazy('estoque:geladeiras')