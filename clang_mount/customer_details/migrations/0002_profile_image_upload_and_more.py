# Generated by Django 4.2.7 on 2023-12-14 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_details', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile_image',
            name='upload',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='profile_image',
            name='profile_image',
            field=models.ImageField(blank=True, max_length=255, upload_to='profile'),
        ),
    ]
