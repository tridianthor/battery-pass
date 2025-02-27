from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.hashers import make_password

from utils.resp import Resp

class Role(models.TextChoices):
    ADMIN = "admin", "Admin"
    GOVT = "government", "Government"
    CO = "company", "Company"
    GUEST = "guest", "Guest"
    
class Account(AbstractUser):
    username = None
    is_superuser = None
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.ADMIN)
    
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="accounts_groups",  # Add a unique related_name
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="accounts_user_permissions",  # Add a unique related_name
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']
        
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
        return f'{self.first_name} {self.last_name} {self.email} {self.role} {self.password}'