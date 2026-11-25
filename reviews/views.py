from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from recipes.models import Recipe
from reviews.forms import ReviewForm
from reviews.models import Review


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_create.html'

    def dispatch(self, request, *args, **kwargs):
        self.recipe = get_object_or_404(Recipe, pk=self.kwargs['recipe_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if Review.objects.filter(author=self.request.user, recipe=self.recipe).exists():
            form.add_error(None, 'You have already reviewed this recipe.')
            return self.form_invalid(form)

        form.instance.author = self.request.user
        form.instance.recipe = self.recipe

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = self.recipe
        return context

    def get_success_url(self):
        return reverse('recipes:recipe_detail', kwargs={'pk': self.recipe.pk})


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_edit.html'

    def test_func(self):
        review = self.get_object()
        return review.author == self.request.user

    def get_success_url(self):
        return reverse('recipes:recipe_detail', kwargs={'pk': self.object.recipe.pk})


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'

    def test_func(self):
        review = self.get_object()
        return review.author == self.request.user

    def get_success_url(self):
        return reverse('recipes:recipe_detail', kwargs={'pk': self.object.recipe.pk})
