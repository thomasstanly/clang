# Generated by Django 4.2.7 on 2023-12-05 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_address_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='created_At',
            new_name='created_at',
        ),
    ]
