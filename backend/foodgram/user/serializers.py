from django.contrib.auth import get_user_model
from rest_framework import serializers
from api.models import Recipe

User = get_user_model()


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        if hasattr(self.context.get('request'), 'user'):
            user = self.context.get('request').user
            if user.is_authenticated:
                return user.subscriptions.filter(id=obj.id).exists()
        return False

    class Meta:
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')
        model = User


class CustomUserWithRecipesSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user.subscriptions.filter(id=obj.id).exists()
        return False

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        recipes_limit = int(self.context.get(
            'request').GET.get('recipes_limit', '-1'))
        qs = obj.recipes.all()
        if recipes_limit > -1:
            qs = qs[:recipes_limit]
        serializer = ShortRecipeSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        model = User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {"password": {"write_only": True}}
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
        )
        model = User

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user