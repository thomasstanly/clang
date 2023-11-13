from django.db import models
from pro_category.models import Categories
from django.utils.text import slugify

# Create your models here.

class Brand(models.Model):
    Brand_name = models.CharField(max_length=29,unique=True)
    brand_image = models.ImageField(upload_to='brand/',default="")
    is_active = models.BooleanField(default=True)

class Product(models.Model):
    product_name = models.CharField(max_length=60)
    category_id = models.ForeignKey(Categories,on_delete=models.SET_NULL, null=True)
    product_brand = models.ForeignKey(Brand,on_delete=models.SET_NULL, null= True)
    description = models.CharField(max_length=250)
    product_slug = models.SlugField(unique=True,max_length=300,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self,*args, **kwargs):
        slug = f"{self.product_name} {self.category_id.category_title} {self.product_brand.Brand_name}"
        self.product_slug = slugify(slug)
        super(Product,self).save(*args, **kwargs)

class attribute(models.Model):
    atrribute_name = models.CharField(max_length=50,unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.atrribute_name

class attribute_values(models.Model):
    attribute_id = models.ForeignKey(attribute,on_delete=models.CASCADE)
    attribute_value = models.CharField(max_length=40)

    


class Product_varient(models.Model):
    product_name = models.ForeignKey(Product,on_delete=models.CASCADE)
    attribute_name = models.ManyToManyField(attribute,max_length=100)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    discount_price = models.DecimalField(max_digits=10,decimal_places=2)
    thumbnail_image = models.ImageField(upload_to='product/thumbnail',blank=True)
    varient_slug = models.SlugField(unique=True,max_length=300,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self,*args, **kwargs):
        slug = f"{self.product_name} {self.p} {self.attribute_name} {self.id}"
        self.varient_slug = slugify(slug)
        super(Product_varient,self).save(*args, **kwargs)

class product_image(models.Model):
    varient_id = models.ForeignKey(Product_varient, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='varient/')

    