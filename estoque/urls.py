from django.urls import path
from .views import homepage

app_name = 'estoque'

urlpatterns = [
    path('', homepage),
]