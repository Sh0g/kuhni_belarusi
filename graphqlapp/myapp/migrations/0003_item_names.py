# Generated by Django 5.0.4 on 2024-06-06 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_name_alter_item_options_remove_item_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='names',
            field=models.ManyToManyField(to='myapp.name'),
        ),
    ]
