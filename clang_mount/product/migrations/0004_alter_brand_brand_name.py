# Generated by Django 4.2.7 on 2023-11-12 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_brand_brand_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='Brand_name',
            field=models.CharField(max_length=29, unique=True),
        ),
    ]