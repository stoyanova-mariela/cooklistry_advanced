from rest_framework import serializers

from recipes.models import Category, RecipeIngredient, Recipe


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = serializers.StringRelatedField()
    unit = serializers.CharField(source='get_unit_display', read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'quantity', 'unit')


class RecipeSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)
    recipe_ingredients = RecipeIngredientSerializer(read_only=True, many=True)
    difficulty = serializers.CharField(source='get_difficulty_display', read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'description', 'instructions', 'preparation_time', 'servings', 'difficulty', 'owner', 'category', 'recipe_ingredients', 'created_at')
        read_only_fields = fields
