# Generated by Django 4.1.3 on 2023-05-25 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='categories',
        ),
    ]
