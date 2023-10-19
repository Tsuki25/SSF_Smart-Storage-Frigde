from django.urls import path
from .views import Homepage, Profile, DeleteAccount, CreateGeladeira, Geladeiras, DetalhesGeladeira, UpdateGeladeira, \
    DeleteGeladeira

app_name = 'estoque'

urlpatterns = [
    path('', Homepage.as_view(), name="homepage"),
    path('profile/', Profile.as_view(), name="profile"),
    path('excluir_conta/<int:pk>/', DeleteAccount.as_view(), name="excluir_conta"),
    path('geladeiras/', Geladeiras.as_view(), name="geladeiras"),
    path('geladeiras/criar_geladeira', CreateGeladeira.as_view(), name="criar_geladeira"),
    path('geladeiras/geladeira/<int:pk>/', DetalhesGeladeira.as_view(), name="detalhes_geladeira"),
    path('geladeiras/geladeira/edit/<int:pk>/', UpdateGeladeira.as_view(), name="editar_geladeira"),
    path('geladeiras/geladeira/excluir_geladeira/<int:pk>/', DeleteGeladeira.as_view(), name="excluir_geladeira"),
]
