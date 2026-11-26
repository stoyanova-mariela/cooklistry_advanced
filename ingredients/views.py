from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from ingredients.models import Ingredient
from ingredients.forms import IngredientForm


class IngredientManagementMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return (self.request.user.is_superuser or self.request.user.groups.filter(name='Recipe Editors').exists())


class IngredientCreateView(IngredientManagementMixin, CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'ingredients/ingredient_form.html'
    success_url = reverse_lazy('ingredients:ingredient_list')


class IngredientListView(ListView):
    model = Ingredient
    template_name = 'ingredients/ingredient_list.html'
    context_object_name = 'ingredients'


class IngredientUpdateView(IngredientManagementMixin, UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'ingredients/ingredient_form.html'
    success_url = reverse_lazy('ingredients:ingredient_list')


class IngredientDeleteView(IngredientManagementMixin, DeleteView):
    model = Ingredient
    template_name = 'ingredients/ingredient_confirm_delete.html'
    success_url = reverse_lazy('ingredients:ingredient_list')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, "This ingredient cannot be deleted because it is used by existing recipes.")
            return HttpResponseRedirect(self.success_url)

