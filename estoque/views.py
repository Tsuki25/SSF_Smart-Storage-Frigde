from allauth.account.views import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView, DeleteView

from estoque.forms import UpdateUsuarioForm


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
    template_name = "delete_account.html"
    model = User
    success_url = reverse_lazy('estoque:homepage')

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        logout(request)
        user.delete()

        return HttpResponseRedirect(self.success_url)