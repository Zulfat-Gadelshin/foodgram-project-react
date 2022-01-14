from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'id',
        'username',
        'first_name',
        'last_name',
    )
    search_fields = (
        'username',
        'email',
        'last_name',
        'first_name',
    )
    list_filter = (
        'username',
        'email',
    )
