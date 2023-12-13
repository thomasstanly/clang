# Generated by Django 4.2.7 on 2023-12-08 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0004_alter_coupon_expiry_date'),
        ('order', '0006_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='coupon.coupon'),
        ),
    ]