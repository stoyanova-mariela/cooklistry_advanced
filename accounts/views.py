from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from accounts.forms import RegistrationForm, ProfileEditForm
from accounts.models import Profile


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = '/'

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
            Profile.objects.create(user=self.object)
        return HttpResponseRedirect(self.get_success_url())


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    next_page = 'recipes:home'

class UserLogoutView(LogoutView):
    next_page = 'accounts:login'

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile_edit.html'
    context_object_name = 'profile'
    success_url = reverse_lazy('accounts:profile_detail')

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'accounts/profile_confirm_delete.html'
    success_url = reverse_lazy('recipes:home')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        logout(self.request)
        return response