from django.db import models
from admin_side.models import User

# Create your models here.
class Wallet(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user+str(self.balance)
    
class Wallet_Transaction(models.Model):
    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.wallet+self.type