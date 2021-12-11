from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return user.subscriptions.filter(id=obj.id).exists()

    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')
        model = User


class CustomUserWithRecipesSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    # recipes = 'api.serializers'.RecipeSerializer('authors_recipes', many=True)
    recipes_count = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return user.subscriptions.filter(id=obj.id).exists()

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        model = User
