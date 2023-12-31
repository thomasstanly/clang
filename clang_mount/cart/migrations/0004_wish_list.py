# Generated by Django 4.2.7 on 2023-11-30 13:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_alter_product_varient_discount_percentage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0003_alter_cartitems_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wish_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product_varient')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
