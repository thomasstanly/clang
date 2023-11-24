from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator,RegexValidator,MinValueValidator
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

# Create your models here.

class Manager(BaseUserManager):
    def create_user(self,email,password,user_name, **other_field):
        email = self.normalize_email(email)
        user = self.model(email=email,user_name=user_name,**other_field)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,user_name, password , **other_field):
        other_field.setdefault('is_active',True)
        other_field.setdefault('is_superuser',True)
        other_field.setdefault('is_staff',True)
        return self.create_user(email,password,user_name, **other_field)
 
class User(AbstractBaseUser,PermissionsMixin):
    user_name = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    joined_on = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(blank=True,null=True,validators=[MaxValueValidator(limit_value=timezone.now().date())],)
    phone = models.BigIntegerField(unique=True,null=True,validators=[MinValueValidator(1000000000),MaxValueValidator(9999999999)])

    objects = Manager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.email
