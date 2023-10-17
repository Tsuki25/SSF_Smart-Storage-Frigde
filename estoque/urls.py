from django.urls import path
from .views import Homepage, Profile, DeleteAccount, CreateGeladeira, Geladeiras

app_name = 'estoque'

urlpatterns = [
    path('', Homepage.as_view(), name="homepage"),
    path('profile/', Profile.as_view(), name="profile"),
    path('excluir_conta/<int:pk>/', DeleteAccount.as_view(), name="excluir_conta"),
    path('geladeiras/', Geladeiras.as_view(), name="geladeiras"),
    path('geladeiras/criar_geladeira', CreateGeladeira.as_view(), name="criar_geladeira"),
]
