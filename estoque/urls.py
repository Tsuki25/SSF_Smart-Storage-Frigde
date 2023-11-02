from django.conf import settings
from django.urls import path
import estoque.views as views
from django.conf.urls.static import static

app_name = 'estoque'

urlpatterns = [
    path('', views.Geladeiras.as_view(), name="main_page_geladeiras"),
    path('profile/', views.Profile.as_view(), name="profile"),
    path('excluir_conta/<int:pk>/', views.DeleteAccount.as_view(), name="excluir_conta"),

    path('geladeiras/', views.Geladeiras.as_view(), name="geladeiras"),
    path('geladeiras/criar_geladeira', views.CreateGeladeira.as_view(), name="criar_geladeira"),
    path('geladeiras/geladeira/<int:pk>/', views.DetalhesGeladeira.as_view(), name="detalhes_geladeira"),
    path('geladeiras/geladeira/edit/<int:pk>/', views.UpdateGeladeira.as_view(), name="editar_geladeira"),
    path('geladeiras/geladeira/excluir_geladeira/<int:pk>/', views.DeleteGeladeira.as_view(), name="excluir_geladeira"),

    path('produtos/cadastrar_produto', views.CreateProduto.as_view(), name="cadastrar_produto"),
    path('produtos/editar_produto/<int:pk>', views.UpdateProduto.as_view(), name="editar_produto"),# TALVEZ DEVA SER REMOVIDO
    path('produtos/excluir_produto/<int:pk>', views.DeleteProduto.as_view(), name="excluir_produto"),# TALVEZ DEVA SER REMOVIDO

    path('geladeiras/listas/<int:pk>', views.Listas.as_view(), name="listas"),
    path('geladeiras/lista/criar_lista/<int:pk>', views.CreateLista.as_view(), name="criar_lista"),
    path('geladeiras/lista/<int:pk>/', views.DetalhesLista.as_view(), name="detalhes_lista"),
    path('geladeiras/lista/edit/<int:pk>/', views.UpdateLista.as_view(), name="editar_lista"),
    path('geladeiras/lista/<int:geladeira>/excluir_lista/<int:pk>/', views.DeleteLista.as_view(), name="excluir_lista"),

    path('geladeira/produtos/<int:pk>', views.Produtos.as_view(), name="produtos_geladeira"),
    path('geladeira/produtos_lista/<int:pk>', views.Produtos.as_view(), name="produtos_lista"),

    path('geladeira/<int:geladeira>/cadastrar_item_geladeira/<int:produto>', views.CreateItemGeladeira.as_view(), name="cadastrar_item_geladeira"),
    path('geladeira/<int:geladeira>/excluir_item/<int:pk>', views.DeleteItemGeladeira.as_view(), name="excluir_item_geladeira"),
    path('geladeira/listas/<int:lista>/cadastrar_item_lista/<int:produto>', views.CreateItemLista.as_view(), name="cadastrar_item_lista"),
    path('geladeira/listas/<int:lista>/excluir_item/<int:pk>', views.DeleteItemLista.as_view(), name="excluir_item_lista"),

    path('geladeiras/geladeira/historico/<int:pk>', views.HistoricoGeladeira.as_view(), name="historico_geladeira"),
    path('geladeiras/geladeira/compartilhar_geladeira/<int:pk>', views.CompartilharGeladeira.as_view(), name="compartilhar_geladeira"),
]
