from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'admin'
        USER = 'user'

    id = models.BigAutoField(primary_key=True)
    confirmation_code = models.CharField(max_length=16, verbose_name='Код')
    bio = models.CharField(max_length=254, null=True, blank=True)
    role = models.CharField(max_length=50, verbose_name='Название роли',
                            null=True, choices=Roles.choices)
    email = models.EmailField(verbose_name='email', unique=True, max_length=254)
    username = models.CharField(unique=True, max_length=150)
    subscriptions = models.ManyToManyField("self", symmetrical=False)

    @property
    def is_admin(self):
        return self.is_superuser or self.role == 'admin'

    @property
    def is_user(self):
        return self.role == 'user'
