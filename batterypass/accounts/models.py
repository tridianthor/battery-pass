from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.hashers import make_password

from utils.resp import Resp
    
class Account(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="accounts_groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="accounts_user_permissions",
    )
        
    @classmethod
    def activate(cls, id):
        try:
            user = cls.objects.get(id=id)
            user.is_active = True
            user.save()
            return Resp(True, "Account activated", user)
        except Exception as exc:
            return Resp(False, str(exc))

    @classmethod
    def deactivate(cls, id):
        try:
            user = cls.objects.get(id=id)
            user.is_active = False
            user.save()
            return Resp(True, "Account deactivated", user)
        except Exception as exc:
            return Resp(False, str(exc))

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email} {self.password}'