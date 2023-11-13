from django.db import models

# Create your models here.
class Categories(models.Model):
    category_img = models.ImageField(upload_to='category/',default="")
    category_title = models.CharField(max_length=40,unique=True, default="")
    description = models.CharField(max_length=250, default="")
    created_on = models.DateTimeField(auto_now_add=True)