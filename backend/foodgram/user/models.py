from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'admin'
        USER = 'user'

    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    # confirmation_code = models.CharField(max_length=16, verbose_name='Код', null=True, blank=True)
    role = models.CharField(max_length=50,
                            verbose_name='Название роли',
                            null=True,
                            choices=Roles.choices,
                            default=Roles.USER)
    email = models.EmailField(
        verbose_name='email', unique=True, max_length=254)
    username = models.CharField(unique=True, max_length=150)
    subscriptions = models.ManyToManyField(
        "self", symmetrical=False, blank=True)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.Roles.ADMIN

    @property
    def is_user(self):
        return self.role == self.Roles.USER

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'
