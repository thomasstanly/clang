# Generated by Django 4.2.7 on 2023-11-30 13:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_alter_product_varient_discount_percentage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0004_wish_list'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Wish_list',
            new_name='Wishlist',
        ),
    ]
