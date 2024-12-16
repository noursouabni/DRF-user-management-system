from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
class UserManager(BaseUserManager):
    def create_user(self, name_user, password=None, **extra_fields):
        if not name_user:
            raise ValueError('The Name User field must be set')
        user = self.model(name_user=name_user, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name_user, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(name_user, password, **extra_fields)

class User(AbstractBaseUser):
    id_user = models.AutoField(primary_key=True)
    name_user = models.CharField(max_length=255, unique=True)  # Username field
    type_user = models.CharField(max_length=50)
    id_document_filled = models.IntegerField(default=0)
    id_document_received = models.IntegerField(default=0)
    is_staff = models.BooleanField(default=False)  # Required for admin access
    is_superuser = models.BooleanField(default=False)  # Required for superuser
    is_active = models.BooleanField(default=True)  # Required by Django

    objects = UserManager()  # Link the custom manager

    USERNAME_FIELD = 'name_user'
    REQUIRED_FIELDS = ['type_user']  # Prompts during superuser creation

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name_user

    # Required by Django
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
