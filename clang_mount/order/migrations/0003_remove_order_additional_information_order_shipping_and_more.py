# Generated by Django 4.2.7 on 2023-12-03 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='additional_information',
        ),
        migrations.AddField(
            model_name='order',
            name='shipping',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='total_discount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]
