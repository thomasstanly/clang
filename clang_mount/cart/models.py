from django.db import models
from admin_side.models import User
from product.models import Product_varient
from offer_manage.models import CategoryOffer, BrandOffer
from coupon.models import Coupon
import uuid
from django.utils import timezone

# Create your models here.
class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
    
class CartItems(models.Model):
    product = models.ForeignKey(Product_varient,on_delete=models.CASCADE,related_name="items")
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cartitems")
    quantity = models.IntegerField(default=1)

    def sub_total(self):
         return self.product.price * self.quantity
    
    def discount(self):
        category_offer = 0
        brand_offer = 0

        product_offer = self.product.discount_percentage

        category= self.product.product_name.category_id
        if CategoryOffer.objects.filter(category_offer=category,is_active=True,offer_expire_date__gte=timezone.now()).exists():
            category_offer = CategoryOffer.objects.filter(category_offer=category,is_active=True,offer_expire_date__gte=timezone.now()).values_list('discount_percentage',flat=True).first()

        brand= self.product.product_name.product_brand
        if BrandOffer.objects.filter(brand_offer=brand,is_active=True,offer_expire_date__gte=timezone.now()).exists():
            brand_offer = BrandOffer.objects.filter(brand_offer=brand,is_active=True,offer_expire_date__gte=timezone.now()).values_list('discount_percentage',flat=True).first()
        
        offer = category_offer + brand_offer + product_offer

        if offer >= 100:
            offer = 100
        
        discount = (offer * self.product.price)/100
        return round(discount * self.quantity,2)

    def __str__(self):
        return self.product.product_name
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product_varient,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product.product_name
    


