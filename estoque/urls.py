from django.urls import path
from .views import Homepage, Profile

app_name = 'estoque'

urlpatterns = [
    path('', Homepage.as_view(), name="homepage"),
    path('profile/', Profile.as_view(), name='profile'),
]