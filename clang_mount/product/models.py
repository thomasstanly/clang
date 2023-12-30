from django.db import models
from pro_category.models import Categories
from django.utils.text import slugify
from django.utils import timezone
from PIL import Image

# Create your models here.

class Brand(models.Model):
    Brand_name = models.CharField(max_length=29,unique=True)
    brand_image = models.ImageField(upload_to='brand/',default="")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.Brand_name

class Product(models.Model):
    product_name = models.CharField(max_length=60,unique=True,blank=False)
    category_id = models.ForeignKey(Categories,on_delete=models.SET_NULL, null=True)
    product_brand = models.ForeignKey(Brand,on_delete=models.SET_NULL, null= True)
    description = models.CharField(max_length=250)
    product_slug = models.SlugField(unique=True,max_length=300,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name


    def save(self,*args, **kwargs):
        slug = f"{self.product_name} {self.category_id.category_title} {self.product_brand.Brand_name}"
        self.product_slug = slugify(slug)
        super(Product,self).save(*args, **kwargs)

        if not self.is_active:
            self.product_vareint.filter(vari_is_active=True).update(vari_is_active=False)
        else:
            self.product_vareint.filter(vari_is_active=False).update(vari_is_active=True)

class attribute(models.Model):
    atrribute_name = models.CharField(max_length=50,unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.atrribute_name

class attribute_values(models.Model):
    attribute_id = models.ForeignKey(attribute,on_delete=models.CASCADE)
    attribute_value = models.CharField(max_length=40,unique=True)
    attr_is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.attribute_value


class Product_varient(models.Model):
    product_name = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_vareint')
    attribute_name = models.ManyToManyField(attribute_values,max_length=100)
    stock = models.IntegerField(default=0)
    sku_id = models.CharField(max_length=30,unique=True,default='')
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    discount_percentage = models.IntegerField(null=True,blank=True)
    thumbnail_image = models.ImageField(upload_to='product/thumbnail',blank=True)
    varient_slug = models.SlugField(unique=True,max_length=300,blank=True)
    vari_is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def percetage(self):
        product_offer = self.discount_percentage
        category_offer = 0
        brand_offer = 0

        category= self.product_name.category_id
        if self.product_name.category_id.categoryoffer_set.filter(category_offer=category,is_active=True,offer_expire_date__gte=timezone.now()).exists():
            category_offer = self.product_name.category_id.categoryoffer_set.filter(category_offer=category,is_active=True,offer_expire_date__gte=timezone.now()).values_list('discount_percentage',flat=True).first()

        brand= self.product_name.product_brand
        if self.product_name.product_brand.brandoffer_set.filter(brand_offer=brand,is_active=True,offer_expire_date__gte=timezone.now()).exists():
            brand_offer = self.product_name.product_brand.brandoffer_set.filter(brand_offer=brand,is_active=True,offer_expire_date__gte=timezone.now()).values_list('discount_percentage',flat=True).first()
        
        offer = category_offer + brand_offer + product_offer
        if offer >= 100:
            offer = 100
        
        return offer


    def after_discount(self):
        product_offer = self.discount_percentage
        category_offer = 0
        brand_offer = 0

        category= self.product_name.category_id
        if self.product_name.category_id.categoryoffer_set.filter(category_offer=category,is_active=True,offer_expire_date__gte=timezone.now()).exists():
            category_offer = self.product_name.category_id.categoryoffer_set.filter(category_offer=category,is_active=True,offer_expire_date__gte=timezone.now()).values_list('discount_percentage',flat=True).first()

        brand= self.product_name.product_brand
        if self.product_name.product_brand.brandoffer_set.filter(brand_offer=brand,is_active=True,offer_expire_date__gte=timezone.now()).exists():
            brand_offer = self.product_name.product_brand.brandoffer_set.filter(brand_offer=brand,is_active=True,offer_expire_date__gte=timezone.now()).values_list('discount_percentage',flat=True).first()

        offer = category_offer + brand_offer + product_offer

        if offer >= 100:
            offer = 100

        discount = (offer * self.price)/100
        return self.price - discount
    
    def __str__(self):
        return f"{self.product_name} {self.product_name.product_brand} {self.pk}"

    def save(self,*args, **kwargs):

        slug = f"{self.product_name} {self.product_name.product_brand} {self.pk}"
        self.varient_slug = slugify(slug)
        
        super(Product_varient,self).save(*args, **kwargs)
       

        if self.thumbnail_image:
            img = Image.open(self.thumbnail_image.path)
            size = (522,522)
            img=img.resize(size, Image.BOX)
            img.save(self.thumbnail_image.path)


class product_image(models.Model):
    varient_id = models.ForeignKey(Product_varient, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='varient/')

    def __str__(self):
        return f"{self.image}"
    
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            size = (522,522)
            img=img.resize(size, Image.BOX)
            img.save(self.image.path)