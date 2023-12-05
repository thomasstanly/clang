from django.db import models
from admin_side.models import User
from account.models import Address
from product.models import Product_varient
# Create your models here.

class Payment(models.Model):
    payment_status = (("PENDING","Pending"),("FAILED","Failed"),("SUCCESS","Success"))
    payment_method = (("COD","Cash on delivery"),("ONLINE_PAYMENT","Online_payment"))
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(choices=payment_method, max_length=100)
    amount_paid = models.CharField(max_length=30)
    status = models.CharField(choices=payment_status, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

class Order(models.Model):
    order_status = (("PROCESSING","Processing"),("DISPATCHED","Dispatched"),("OUT OF DELIVERY","Out of delivery"),("CANCELLED","Cancelled"),("RETURNED","Returned"))
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
    order_no = models.CharField(max_length=100)
    delivery_address = models.ForeignKey(Address,on_delete=models.SET_NULL,null=True,)
    sub_total = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    shipping = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    grand_total = models.DecimalField(max_digits=12,decimal_places=2)
    status = models.CharField(choices=order_status,max_length=20,default="PROCESSING")
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_no}"
    
class OrderProduct(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product_varient, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=12, decimal_places=2)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.order)