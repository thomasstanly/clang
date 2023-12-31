# Generated by Django 4.2.7 on 2023-12-05 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PROCESSING', 'Processing'), ('DISPATCHED', 'Dispatched'), ('OUT OF DELIVERY', 'Out of delivery'), ('CANCELLED', 'Cancelled'), ('RETURNED', 'Returned')], default='PROCESSING', max_length=20),
        ),
    ]
