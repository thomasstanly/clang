# Generated by Django 4.2.7 on 2023-11-23 14:29

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_side', '0004_user_date_of_birth_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date(2023, 11, 23))]),
        ),
    ]
