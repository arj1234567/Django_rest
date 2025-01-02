from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User as user
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# First, create a custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        user = self.model(username=username, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        return self.create_user(username, password, **extra_fields)

# Then modify your User model
class User(AbstractBaseUser, PermissionsMixin):
    username        = models.CharField(max_length=255,null=True,blank=True,unique=True)
    password        = models.CharField(max_length=255,null=True,blank=True)
    email           = models.EmailField(max_length=255, null=True, blank=True)
    first_name      = models.CharField(max_length=255, null=True, blank=True)
    last_name       = models.CharField(max_length=255, null=True, blank=True)
    
    # Custom fields
    phoneno         = models.CharField(max_length=255, null=True, blank=True)
    is_logged_in    = models.BooleanField(default=False)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    
    objects         = CustomUserManager()

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'authentication_user'

    def __str__(self):
        return self.username or ''

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
class GeneratedAccessToken(models.Model):
    token = models.TextField(null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

# Create your models here.
