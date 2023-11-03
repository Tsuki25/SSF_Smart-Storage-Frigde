from datetime import datetime, timedelta

from allauth.account.views import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, UpdateView, DeleteView, CreateView, ListView, DetailView
from allauth.account.views import SignupView

from estoque.forms import UpdateUsuarioForm, ProdutoForm, GeladeiraForm, ListaForm, ItemGeladeiraForm, ItemListaForm
from estoque.models import Geladeira, Produto, Item_Geladeira, Lista, Item_Lista, Log_Itens_Geladeira


class Homepage(TemplateView):
    template_name = "homepage.html"


class Profile(LoginRequiredMixin, UpdateView):
    template_name = "profile.html"
    model = User
    form_class = UpdateUsuarioForm

    def get_success_url(self):
        return reverse('estoque:geladeiras')

    def get_object(self, queryset=None):
        self.object = get_object_or_404(User, username=self.request.user)
        return self.object


class DeleteAccount(LoginRequiredMixin, DeleteView):
    template_name = "delete.html"
    model = User

    def get_success_url(self):
        return reverse('estoque:geladeiras')

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        logout(request)
        user.delete()

        return HttpResponseRedirect(self.success_url)

class CustomSignupView(SignupView):
    def form_invalid(self, form):
        response = super().form_invalid(form)
        # Verificar as regras da senha
        # Por exemplo, você pode usar a biblioteca "django-password-validators"
        # para verificar a força da senha.
        if not password_validators.password_changed(self.request.POST.get('password1')):
            form.add_error('password1', 'A senha não atende aos requisitos.')
        return response


# =================================================================================
# =========================== GELADEIRAS ==========================================

class CreateGeladeira(LoginRequiredMixin, CreateView):
    template_name = "form_insert_update.html"
    model = Geladeira
    form_class = GeladeiraForm

    def get_success_url(self):
        return reverse('estoque:geladeiras')

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
        context['geladeiras'] = Geladeira.objects.all()  # PEGA TODOS OS OBJETOS GELADEIRA E ADICIONA A UMA LISTA

        termo_pesquisa = self.request.GET.get('q')  # Obtém o termo de busca da URL
        if termo_pesquisa:
            context['geladeiras'] = Geladeira.objects.filter(nome_geladeira__icontains=termo_pesquisa)
        return context


class DetalhesGeladeira(LoginRequiredMixin, DetailView):
    template_name = "detalhes_geladeira.html"
    model = Geladeira

    def post(self, request, *args, **kwargs):
        # Utilizado para atualizar de forma mais direta cada item exibido e que pertencee a essa geladeira
        item_id = request.POST.get('item_id')
        nova_quantidade = int(request.POST.get('quantidade' + item_id))
        nova_validade = request.POST.get('validade' + item_id)
        if nova_quantidade < 0: nova_quantidade = 0 # Garante que a quantidade minima será 0

        if item_id: #Se o item informado existir
            try:
                item = Item_Geladeira.objects.get(id=item_id) #Pega a instancia do item
                # Cria um histórico de modificação
                att_item_log = Log_Itens_Geladeira(item_geladeira=item, usuario=self.request.user,
                                                   geladeira=Geladeira.objects.get(pk=self.kwargs['pk']),
                                                   descricao=f"{item.produto.nome_produto} modificado por {self.request.user.username} em {datetime.now().strftime('%d/%m/%Y %H:%M')}")
                att_item_log.save()

                # Modifica os dados do item de acordo com os novos informados
                item.quantidade = nova_quantidade
                item.validade = nova_validade
                item.save()
            except Item_Geladeira.DoesNotExist:
                pass

        return redirect('estoque:detalhes_geladeira', self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_geladeira'] = Item_Geladeira.objects.filter(
            geladeira=self.object)  # Pega os itens da tabela intemediaria Item_Geladeira

        termo_pesquisa = self.request.GET.get('q')  # Obtém o termo de busca da URL
        if termo_pesquisa:  # Use a consulta Q para pesquisar geladeiras por nome
            context['item_geladeira'] = Item_Geladeira.objects.filter(geladeira=self.object,
                                                                      produto__nome_produto__contains=termo_pesquisa)

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
    def get_success_url(self):
        return reverse('estoque:geladeiras')


# ===============================================================================
# =========================== PRODUTOS ==========================================

class CreateProduto(LoginRequiredMixin, CreateView):
    template_name = "form_insert_update.html"
    model = Produto
    form_class = ProdutoForm

    def get_success_url(self):
        return reverse('estoque:geladeiras')


class UpdateProduto(LoginRequiredMixin, UpdateView):
    template_name = "form_insert_update.html"
    model = Produto
    form_class = ProdutoForm

    def get_success_url(self):
        return reverse('estoque:geladeiras')


class DeleteProduto(LoginRequiredMixin, DeleteView):
    template_name = "delete.html"
    model = Produto

    def get_success_url(self):
        return reverse('estoque:geladeiras')


class Produtos(LoginRequiredMixin, ListView):
    template_name = "produtos_existentes.html"
    model = Produto

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos'] = Produto.objects.all() # Pega todos os dados da tabela Produto
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
            context['produtos'] = Produto.objects.filter(nome_produto__icontains=termo_pesquisa)

        return context


# =============================================================================
# =========================== LISTAS ==========================================

class CreateLista(LoginRequiredMixin, CreateView):
    template_name = "form_insert_update.html"
    model = Lista
    form_class = ListaForm

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
        geladeira = Geladeira.objects.get(pk=self.kwargs['pk']) # Instancia um objeto geladeira baseado nessa pk
        context['geladeira'] = geladeira # Passa a instancia como um contexto para o template
        context['listas'] = Lista.objects.filter(geladeira=geladeira) # Passa todas as listas para o template
        return context


class DetalhesLista(LoginRequiredMixin, DetailView):
    template_name = "detalhes_lista.html"
    model = Lista

    def post(self, request, *args, **kwargs):
        # Utilizado para atualizar de forma mais direta cada item exibido e que pertence a essa lista
        item_id = request.POST.get('item_id')
        nova_quantidade = int(request.POST.get('quantidade' + item_id))
        if nova_quantidade < 0: nova_quantidade = 0 # Garante que a quantidade minima é 0

        if item_id: # Se o item foi informado corretamente
            try: # Tenta buscar e atualizar o objeto item de Item_Lista no banco com os novos dados inseridos
                item = Item_Lista.objects.get(id=item_id)
                item.quantidade = nova_quantidade
                item.save()
            except Item_Lista.DoesNotExist:
                pass

        return redirect('estoque:detalhes_lista', self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_lista'] = Item_Lista.objects.filter(
            lista=self.object)  # Pega cada item na tabela intermediaria Item_Lista que pertença a lista atual

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

    def form_valid(self, form): #Pega os valores do formulario e salva no banco de dados
        item_geladeira = form.save(commit=False)
        item_geladeira.geladeira_id = self.kwargs['geladeira']
        item_geladeira.produto_id = self.kwargs['produto']
        item_geladeira.save()
        # REGISTRA O LOG DE INSERÇÃO DO ITEM NA GELADEIRA
        att_item_log = Log_Itens_Geladeira(item_geladeira=item_geladeira, usuario=self.request.user,
                                           geladeira=Geladeira.objects.get(pk=self.kwargs['geladeira']),
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

    def form_valid(self, form): #Pega os valores do formulario e salva no banco de dados
        item_lista = form.save(commit=False)
        item_lista.lista_id = self.kwargs['lista']
        item_lista.produto_id = self.kwargs['produto']

        # VERIFICA SE O PRODUTO SELECIONADO JÁ EXISTE NA LISTA
        try: # Tenta adicionar a nova quantidade informada ao item existente
            aux = Item_Lista.objects.get(lista_id=self.kwargs['lista'], produto_id=self.kwargs['produto'])
            aux.quantidade += item_lista.quantidade
            aux.save()

            return redirect(reverse_lazy('estoque:detalhes_lista', kwargs={'pk': self.kwargs['lista']}))

        except Item_Lista.DoesNotExist: # Se o item não existir, cria um novo item conforme solicitado pelo usuario
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
class HistoricoGeladeira(LoginRequiredMixin, ListView): #View para exibir o histórico de alterações de uma geladeira
    template_name = "historico_movimentacoes_geladeira.html"
    model = Log_Itens_Geladeira

    def get_context_data(self, **kwargs):  # DEFINE O CONTEXTO
        context = super().get_context_data(**kwargs)

        dias_carregados = datetime.now().date() - timedelta(days=30)  # Pega a data correspondente a 30 dias atrás
        # Pega o histórico de dias maiores ou iguais a 30 dias atrás
        context['historico'] = Log_Itens_Geladeira.objects.filter(dt_modificacao__gte=dias_carregados)
        geladeira = Geladeira.objects.get(pk=self.kwargs['pk']) #Instancia um objeto de identificação da geladeira
        context['item_geladeira'] = Item_Geladeira.objects.filter(geladeira=geladeira) # Pega todos os objetos de item_geladeira que pertençam a geladeira do histórico
        context['geladeira'] = geladeira
        datas = Log_Itens_Geladeira.objects.filter(dt_modificacao__gte=dias_carregados).values_list('dt_modificacao', flat=True).distinct().order_by('-dt_modificacao')
        # Salva todas as datas para as quais existam logs e que estejam dentro dos 30 dias de histórico
        context['datas'] = datas

        return context


class CompartilharGeladeira(LoginRequiredMixin, View):
    def get(self, request, pk):
        geladeira = get_object_or_404(Geladeira, pk=pk)

        if request.user not in geladeira.usuarios_proprietarios.all():
            geladeira.usuarios_proprietarios.add(request.user)
        else:
            redirect('estoque:geladeiras')

        return redirect('estoque:detalhes_geladeira', pk)
