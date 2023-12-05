from django.db import models
from admin_side.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=50)
    address = models.CharField(max_length=500)
    phone = models.BigIntegerField(unique=True,null=True,validators=[MinValueValidator(1000000000),MaxValueValidator(9999999999)])
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pin_code = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
