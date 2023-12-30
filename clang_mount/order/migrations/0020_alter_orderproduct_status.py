# Generated by Django 4.2.7 on 2023-12-16 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0019_alter_orderproduct_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='status',
            field=models.CharField(choices=[('PROCESSING', 'Processing'), ('DISPATCHED', 'Dispatched'), ('OUT FOR DELIVERY', 'Out for delivery'), ('DELIVERED', 'Delivered'), ('CANCELLED', 'Cancelled'), ('RETURNED', 'Returned')], default='PROCESSING', max_length=20),
        ),
    ]