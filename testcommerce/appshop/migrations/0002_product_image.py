# Generated by Django 5.0.4 on 2024-04-09 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appshop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]
