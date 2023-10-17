from django.urls import path
from .views import Homepage, Profile, DeleteAccount

app_name = 'estoque'

urlpatterns = [
    path('', Homepage.as_view(), name="homepage"),
    path('profile/', Profile.as_view(), name="profile"),
    path('excluir_conta/<int:pk>/', DeleteAccount.as_view(), name="excluir_conta")
]