from django.db import models
from admin_side.models import User
# Create your models here.

class Profile_image(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    profile_image=models.ImageField(upload_to='profile',blank=True,max_length=255)
    upload = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
