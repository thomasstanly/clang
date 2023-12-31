# Generated by Django 4.2.7 on 2023-12-16 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0017_order_status_alter_orderproduct_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PROCESSING', 'Processing'), ('DISPATCHED', 'Dispatched'), ('OUT FOR DELIVERY', 'Out for delivery'), ('DELIVERED', 'Delivered'), ('CANCELLED', 'Cancelled')], default='PROCESSING', max_length=20),
        ),
    ]
