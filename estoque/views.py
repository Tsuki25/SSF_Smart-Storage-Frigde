from allauth.account.views import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView, DeleteView, CreateView, ListView, DetailView

from estoque.forms import UpdateUsuarioForm, ProdutoForm, GeladeiraForm, ListaForm, ItemGeladeiraForm, ItemListaForm
from estoque.models import Geladeira, Produto, Item_Geladeira, Lista, Item_Lista


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


# =================================================================================
# =========================== GELADEIRAS ==========================================

class CreateGeladeira(CreateView, LoginRequiredMixin):
    template_name = "form_insert_update.html"
    model = Geladeira
    form_class = GeladeiraForm
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
        context[
            'item_geladeira'] = Item_Geladeira.objects.all()  # PEGA CADA ITEM DA GELADEIRA DE ACORDO COM A TABELA INTERMEDIARIA
        return context


class UpdateGeladeira(UpdateView):  # TALVEZ SEJA REMOVIDO
    template_name = "form_insert_update.html"
    model = Geladeira
    form_class = GeladeiraForm

    def get_success_url(self):
        return reverse('estoque:detalhes_geladeira', args=[self.object.pk])


class DeleteGeladeira(DeleteView):  # TALVEZ SEJA REMOVIDO
    template_name = "delete.html"
    model = Geladeira
    success_url = reverse_lazy('estoque:geladeiras')


# ===============================================================================
# =========================== PRODUTOS ==========================================

class CreateProduto(CreateView, LoginRequiredMixin):
    template_name = "form_insert_update.html"
    model = Produto
    form_class = ProdutoForm
    success_url = reverse_lazy("estoque:geladeiras")


class UpdateProduto(UpdateView, LoginRequiredMixin):
    template_name = "form_insert_update.html"
    model = Produto
    form_class = ProdutoForm
    success_url = reverse_lazy('estoque:geladeiras')


class DeleteProduto(DeleteView):
    template_name = "delete.html"
    model = Produto
    success_url = reverse_lazy('estoque:geladeiras')


class Produtos(ListView):
    template_name = "produtos_existentes.html"
    model = Produto

    def get_context_data(self, **kwargs):  # DEFINE O CONTEXTO DE GELADEIRAS
        try:
            context = super().get_context_data(**kwargs)
            context['produtos'] = Produto.objects.all()
            pk = self.kwargs['pk']

            geladeira = Geladeira.objects.get(pk=pk)
            context['geladeira'] = geladeira

            lista = Lista.objects.get(pk=pk)
            context['lista'] = lista
        except Geladeira.DoesNotExist:
            pass

        except Lista.DoesNotExist:
            pass

        return context


# =============================================================================
# =========================== LISTAS ==========================================

class CreateLista(CreateView, LoginRequiredMixin):
    template_name = "form_insert_update.html"
    model = Lista
    form_class = ListaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        geladeira = Geladeira.objects.get(pk=pk)
        context['geladeira'] = geladeira  # PEGA CADA ITEM DA GELADEIRA DE ACORDO COM A TABELA INTERMEDIARIA
        return context

    def form_valid(self, form):
        lista = form.save(commit=False)
        lista.geladeira_id = self.kwargs['pk']  # Associe a lista à geladeira com base na PK na URL
        lista.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('estoque:listas', kwargs={'pk': self.kwargs['pk']})


class Listas(ListView):
    template_name = "home_listas.html"
    model = Lista

    def get_context_data(self, **kwargs):  # DEFINE O CONTEXTO DE GELADEIRAS
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        geladeira = Geladeira.objects.get(pk=pk)
        context['geladeira'] = geladeira
        context['listas'] = Lista.objects.all()
        return context


class DetalhesLista(LoginRequiredMixin, DetailView):
    template_name = "detalhes_lista.html"
    model = Lista

    # FALTA CONSEGUIR MEXER NO VALOR DOS ITENS DIRETAMENTE NA Lista
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[
            'item_lista'] = Item_Lista.objects.all()  # PEGA CADA ITEM DA GELADEIRA DE ACORDO COM A TABELA INTERMEDIARIA
        return context


class UpdateLista(UpdateView, LoginRequiredMixin):
    template_name = "form_insert_update.html"
    model = Lista
    form_class = ListaForm

    def get_success_url(self):
        return reverse('estoque:detalhes_lista', args=[self.object.pk])


class DeleteLista(DeleteView, LoginRequiredMixin):
    template_name = "delete.html"
    model = Lista

    def get_success_url(self):
        geladeira_pk = self.kwargs['geladeira']
        return reverse('estoque:listas', args=[geladeira_pk])


# =====================================================================================
# =========================== ITEM_GELADEIRA ==========================================

class CreateItemGeladeira(CreateView, LoginRequiredMixin):
    template_name = "form_insert_update.html"
    model = Item_Geladeira
    form_class = ItemGeladeiraForm

    def form_valid(self, form):
        item_geladeira = form.save(commit=False)
        item_geladeira.geladeira_id = self.kwargs['geladeira']
        item_geladeira.produto_id = self.kwargs['produto']
        item_geladeira.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('estoque:detalhes_geladeira', kwargs={'pk': self.kwargs['geladeira']})


class CreateItemLista(CreateView, LoginRequiredMixin):
    template_name = "form_insert_update.html"
    model = Item_Lista
    form_class = ItemListaForm

    def form_valid(self, form):
        item_lista = form.save(commit=False)
        item_lista.lista_id = self.kwargs['lista']
        item_lista.produto_id = self.kwargs['produto']
        item_lista.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('estoque:detalhes_lista', kwargs={'pk': self.kwargs['lista']})
