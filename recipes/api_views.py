from rest_framework import generics, permissions
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer


class RecipeListAPIView(generics.ListAPIView):
    queryset = Recipe.objects.select_related(
        'owner', 'category'
    ).prefetch_related('recipe_ingredients__ingredient')
    serializer_class = RecipeSerializer
    permission_classes = (permissions.AllowAny,)


class RecipeDetailAPIView(generics.RetrieveAPIView):
    queryset = Recipe.objects.select_related(
        'owner', 'category'
    ).prefetch_related('recipe_ingredients__ingredient')
    serializer_class = RecipeSerializer
    permission_classes = (permissions.AllowAny,)
