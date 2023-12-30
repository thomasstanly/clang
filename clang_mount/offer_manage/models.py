from django.db import models
from pro_category.models import Categories
from product.models import Brand
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.
class CategoryOffer(models.Model):
    offer_name = models.CharField(max_length=50,unique=True)
    offer_expire_date = models.DateTimeField()
    category_offer = models.ForeignKey(Categories,on_delete=models.SET_NULL,null=True)
    discount_percentage = models.IntegerField(default=0,validators=[MinValueValidator(1),MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.offer_name

class BrandOffer(models.Model):
    offer_name = models.CharField(max_length=50,unique=True)
    offer_expire_date = models.DateTimeField()
    brand_offer = models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True)
    discount_percentage = models.IntegerField(default=0,validators=[MinValueValidator(1),MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.offer_name
