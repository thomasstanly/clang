# Generated by Django 4.2.7 on 2023-12-15 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_alter_orderproduct_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PROCESSING', 'Processing'), ('DISPATCHED', 'Dispatched'), ('OUT FOR DELIVERY', 'Out for delivery'), ('DELIVERED', 'Delivered')], default='PROCESSING', max_length=20),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='status',
            field=models.CharField(choices=[('CANCELLED', 'Cancelled'), ('RETURNED', 'Returned')], max_length=20),
        ),
    ]
