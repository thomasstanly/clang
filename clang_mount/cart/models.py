from django.db import models
from admin_side.models import User
from product.models import Product_varient
import uuid

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

    def __str__(self):
        return self.product.product_name