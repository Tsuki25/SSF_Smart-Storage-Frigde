from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, UpdateView


class Homepage(TemplateView):
    template_name = "homepage.html"


class Profile(LoginRequiredMixin, UpdateView):
    template_name = "profile.html"
    model = User
    fields = ["username", "email"]

    def get_object(self, queryset=None):
        self.object = get_object_or_404(User, username=self.request.user)
        return self.object
