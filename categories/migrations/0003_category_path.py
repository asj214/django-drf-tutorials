# Generated by Django 4.1.3 on 2023-05-26 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_category_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='path',
            field=models.JSONField(default=list),
        ),
    ]
