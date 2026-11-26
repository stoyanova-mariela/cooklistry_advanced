from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from meal_plans.forms import MealPlanForm
from meal_plans.models import MealPlan


class MealPlanOwnerMixin(LoginRequiredMixin):
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user).prefetch_related('recipes')


class MealPlanListView(MealPlanOwnerMixin, ListView):
    model = MealPlan
    template_name = 'meal_plans/meal_plan_list.html'
    context_object_name = 'meal_plans'


class MealPlanDetailView(MealPlanOwnerMixin, DetailView):
    model = MealPlan
    template_name = 'meal_plans/meal_plan_detail.html'
    context_object_name = 'meal_plan'


class MealPlanCreateView(LoginRequiredMixin, CreateView):
    model = MealPlan
    template_name = 'meal_plans/meal_plan_form.html'
    form_class = MealPlanForm
    success_url = reverse_lazy('meal_plans:meal_plan_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MealPlanUpdateView(MealPlanOwnerMixin, UpdateView):
    model = MealPlan
    template_name = 'meal_plans/meal_plan_form.html'
    form_class = MealPlanForm
    success_url = reverse_lazy('meal_plans:meal_plan_list')


class MealPlanDeleteView(MealPlanOwnerMixin, DeleteView):
    model = MealPlan
    template_name = 'meal_plans/meal_plan_confirm_delete.html'
    success_url = reverse_lazy('meal_plans:meal_plan_list')