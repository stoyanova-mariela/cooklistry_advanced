from django.conf import settings
from django.db import models
from recipes.models import Recipe


class MealPlan(models.Model):
    class Meta:
        ordering = ['-week_start']

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='meal_plans',)
    title = models.CharField(max_length=100)
    week_start = models.DateField()
    notes = models.TextField(blank=True, max_length=500)
    recipes = models.ManyToManyField(Recipe, related_name='meal_plans')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

