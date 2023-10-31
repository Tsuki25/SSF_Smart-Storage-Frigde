from datetime import datetime, timedelta

from allauth.account.views import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView, DeleteView, CreateView, ListView, DetailView

from estoque.forms import UpdateUsuarioForm, ProdutoForm, GeladeiraForm, ListaForm, ItemGeladeiraForm, ItemListaForm
from estoque.models import Geladeira, Produto, Item_Geladeira, Lista, Item_Lista, Log_Itens_Geladeira


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


class DeleteAccount(LoginRequiredMixin, DeleteView):
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

class CreateGeladeira(LoginRequiredMixin, CreateView):
    template_name = "form_insert_update.html"
    model = Geladeira
    form_class = GeladeiraForm
    success_url = reverse_lazy('estoque:geladeiras')

    def form_valid(self, form):
        geladeira = form.save(commit=False)
        geladeira.save()
        geladeira.usuarios_proprietarios.add(self.request.user)

        return super().form_valid(form)


class Geladeiras(LoginRequiredMixin, ListView):
    template_name = "home_geladeiras.html"
    model = Geladeira

    def get_context_data(self, **kwargs):  # DEFINE O CONTEXTO DE GELADEIRAS
        context = super().get_context_data(**kwargs)
        context['geladeiras'] = Geladeira.objects.all() # PEGA TODOS OS OBJETOS GELADEIRA E ADICIONA A UMA LISTA

        termo_pesquisa = self.request.GET.get('q')  # Obtém o termo de busca da URL
        if termo_pesquisa:
            # Use a consulta Q para pesquisar geladeiras por nome
            context['geladeiras'] = Geladeira.objects.filter(nome_geladeira__icontains=termo_pesquisa)
        return context


class DetalhesGeladeira(LoginRequiredMixin, DetailView):
    template_name = "detalhes_geladeira.html"
    model = Geladeira

    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item_id')
        nova_quantidade = int(request.POST.get('quantidade' + item_id))
        nova_validade = request.POST.get('validade' + item_id)
        if nova_quantidade < 0: nova_quantidade = 0

        if item_id and nova_quantidade >= 0:
            try:
                item = Item_Geladeira.objects.get(id=item_id)
                att_item_log = Log_Itens_Geladeira(item_geladeira=item, usuario=self.request.user, geladeira=Geladeira.objects.get(pk=self.kwargs['pk']),descricao=f"{item.produto.nome_produto} modificado por {self.request.user.username} em {datetime.now().strftime('%d/%m/%Y %H:%M')}")
                att_item_log.save()

                item.quantidade = nova_quantidade
                item.validade = nova_validade
                item.save()
            except Item_Geladeira.DoesNotExist:
                pass

        return redirect('estoque:detalhes_geladeira', self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_geladeira'] = Item_Geladeira.objects.filter(geladeira=self.object)  # PEGA CADA ITEM DA GELADEIRA DE ACORDO COM A TABELA INTERMEDIARIA

        termo_pesquisa = self.request.GET.get('q')  # Obtém o termo de busca da URL
        if termo_pesquisa:# Use a consulta Q para pesquisar geladeiras por nome
            context['item_geladeira'] = Item_Geladeira.objects.filter(geladeira=self.object, produto__nome_produto__contains=termo_pesquisa)

        return context


class UpdateGeladeira(LoginRequiredMixin, UpdateView):  # TALVEZ SEJA REMOVIDO
    template_name = "form_insert_update.html"
    model = Geladeira
    form_class = GeladeiraForm

    def get_success_url(self):
        return reverse('estoque:detalhes_geladeira', args=[self.object.pk])


class DeleteGeladeira(LoginRequiredMixin, DeleteView):  # TALVEZ SEJA REMOVIDO
    template_name = "delete.html"
    model = Geladeira
    success_url = reverse_lazy('estoque:geladeiras')


# ===============================================================================
# =========================== PRODUTOS ==========================================

class CreateProduto(LoginRequiredMixin, CreateView):
    template_name = "form_insert_update.html"
    model = Produto
    form_class = ProdutoForm
    success_url = reverse_lazy("estoque:geladeiras")


class UpdateProduto(LoginRequiredMixin, UpdateView):
    template_name = "form_insert_update.html"
    model = Produto
    form_class = ProdutoForm
    success_url = reverse_lazy('estoque:geladeiras')


class DeleteProduto(LoginRequiredMixin, DeleteView):
    template_name = "delete.html"
    model = Produto
    success_url = reverse_lazy('estoque:geladeiras')


class Produtos(LoginRequiredMixin, ListView):
    template_name = "produtos_existentes.html"
    model = Produto

    def get_context_data(self, **kwargs):  # DEFINE O CONTEXTO DE GELADEIRAS
        context = super().get_context_data(**kwargs)
        context['produtos'] = Produto.objects.all()
        pk = self.kwargs['pk']

        try:  # Tenta encontrar uma geladeira com a pk passada pela url
            geladeira = Geladeira.objects.get(pk=pk)
            context['geladeira'] = geladeira
        except Geladeira.DoesNotExist:
            context['geladeira'] = None  # Define como None se não existir

        try:  # Tenta encontrar uma lista com a pk passada pela url
            lista = Lista.objects.get(pk=pk)
            context['lista'] = lista
        except Lista.DoesNotExist:
            context['lista'] = None  # Define como None se não existir

        # UTILIZADO PARA IMPLEMENTAR A BARRA DE PESQUISA NA PAGINA
        termo_pesquisa = self.request.GET.get('q')  # Obtém o termo de busca da URL
        if termo_pesquisa:
            # Use a consulta Q para pesquisar produtos por nome
            context['produtos'] = Produto.objects.filter(nome_produto__icontains=termo_pesquisa)

        return context

# =============================================================================
# =========================== LISTAS ==========================================

class CreateLista(LoginRequiredMixin, CreateView):
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


class Listas(LoginRequiredMixin, ListView):
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

    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item_id')
        nova_quantidade = int(request.POST.get('quantidade' + item_id))
        if nova_quantidade < 0: nova_quantidade = 0

        if item_id and nova_quantidade >= 0:
            try:
                item = Item_Lista.objects.get(id=item_id)
                item.quantidade = nova_quantidade
                item.save()
            except Item_Lista.DoesNotExist:
                pass

        return redirect('estoque:detalhes_lista', self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_lista'] = Item_Lista.objects.filter(
            lista=self.object)  # PEGA CADA ITEM DA GELADEIRA DE ACORDO COM A TABELA INTERMEDIARIA

        return context


class UpdateLista(LoginRequiredMixin, UpdateView):
    template_name = "form_insert_update.html"
    model = Lista
    form_class = ListaForm

    def get_success_url(self):
        return reverse('estoque:detalhes_lista', args=[self.object.pk])


class DeleteLista(LoginRequiredMixin, DeleteView):
    template_name = "delete.html"
    model = Lista

    def get_success_url(self):
        geladeira_pk = self.kwargs['geladeira']
        return reverse('estoque:listas', args=[geladeira_pk])


# =====================================================================================
# =========================== ITEM_GELADEIRA ==========================================

class CreateItemGeladeira(LoginRequiredMixin, CreateView):
    template_name = "form_insert_update.html"
    model = Item_Geladeira
    form_class = ItemGeladeiraForm

    def form_valid(self, form):
        item_geladeira = form.save(commit=False)
        item_geladeira.geladeira_id = self.kwargs['geladeira']
        item_geladeira.produto_id = self.kwargs['produto']
        item_geladeira.save()
        # REGISTRA O LOG DE INSERÇÃO DO ITEM NA GELADEIRA
        att_item_log = Log_Itens_Geladeira(item_geladeira=item_geladeira, usuario=self.request.user, geladeira=Geladeira.objects.get(pk=self.kwargs['geladeira']),
                                           descricao=f"{item_geladeira.produto.nome_produto} inserido por {self.request.user.username} em {datetime.now().strftime('%d/%m/%Y %H:%M')}\n Quantidade:{item_geladeira.quantidade}")
        att_item_log.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('estoque:detalhes_geladeira', kwargs={'pk': self.kwargs['geladeira']})


class DeleteItemGeladeira(LoginRequiredMixin, DeleteView):
    template_name = "delete.html"
    model = Item_Geladeira

    def get_success_url(self):
        geladeira_pk = self.kwargs['geladeira']
        return reverse('estoque:detalhes_geladeira', args=[geladeira_pk])


class CreateItemLista(LoginRequiredMixin, CreateView):
    template_name = "form_insert_update.html"
    model = Item_Lista
    form_class = ItemListaForm

    def form_valid(self, form):
        item_lista = form.save(commit=False)
        item_lista.lista_id = self.kwargs['lista']
        item_lista.produto_id = self.kwargs['produto']

        # VERIFICA SE O PRODUTO SELECIONADO JÁ EXISTE NA LISTA
        # Se sim -> modifica a quantidade do item já cadastrado
        # Se nõa -> Adiciona um novo item a lista com os valores informados
        if Item_Lista.objects.get(lista_id=self.kwargs['lista'], produto_id=self.kwargs['produto']):
            aux = Item_Lista.objects.get(lista_id=self.kwargs['lista'], produto_id=self.kwargs['produto'])
            aux.quantidade += item_lista.quantidade
            aux.save()

            return redirect(reverse_lazy('estoque:detalhes_lista', kwargs={'pk': self.kwargs['lista']}))
        else:
            item_lista.save()
            return super().form_valid(form)

    def form_invalid(self, form):
        return self.get_success_url()

    def get_success_url(self):
        return reverse_lazy('estoque:detalhes_lista', kwargs={'pk': self.kwargs['lista']})


class DeleteItemLista(LoginRequiredMixin, DeleteView):
    template_name = "delete.html"
    model = Item_Lista

    def get_success_url(self):
        lista_pk = self.kwargs['lista']
        return reverse('estoque:detalhes_lista', args=[lista_pk])

# ======================================================================================
# ============================== HISTORICO/LOG GELADEIRA ===============================
class HistoricoGeladeira(LoginRequiredMixin, ListView):
    template_name = "historico_movimentacoes_geladeira.html"
    model = Log_Itens_Geladeira

    def get_context_data(self, **kwargs):  # DEFINE O CONTEXTO
        context = super().get_context_data(**kwargs)

        aux = 0
        for aux in range(30): #Pega apenas os dias que possuam historico para carregar
            if Log_Itens_Geladeira.objects.filter(dt_modificacao=datetime.now().date() - timedelta(days=aux)):
                continue
            else:
                break

        dias_carregados = datetime.now().date() - timedelta(days=aux)  # Pega a data correspondente a 10 dias atrás
        # Captura os logs referentes a itens de uma data maior ou igual a 30 dias atrás
        # e menor ou igual a hoje
        context['historico'] = Log_Itens_Geladeira.objects.filter(dt_modificacao__gte=dias_carregados, dt_modificacao__lte=datetime.now().date())
        context['item_geladeira'] = Item_Geladeira.objects.all()
        context['geladeira'] = Geladeira.objects.get(pk=self.kwargs['pk'])
        datas = [datetime.now().date() - timedelta(days=i) for i in range(aux)]#PEGA A DATA DOS ULTIMOS 30 DIAS e ADICIONA EM UMA LISTA
        context['datas'] = datas

        return context
