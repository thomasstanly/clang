from django.db import models
from django.utils import timezone

# Create your models here.
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10,unique=True,blank=True)
    description = models.CharField(max_length=50)
    dis_percentage = models.DecimalField(max_digits=3,decimal_places=1)
    min_amount = models.PositiveIntegerField(default=500)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(blank=True,null=True)
    

    def save(self,*args, **kwargs):
        if self.dis_percentage > 100:
            self.dis_percentage = 100
        
        if self.expiry_date and self.expiry_date < timezone.now().date():
            self.is_active = False
        super().save(*args, **kwargs)

    def __Str__(self):
        return self.coupon_code
    
    class Meta:
        db_table = 'coupon'