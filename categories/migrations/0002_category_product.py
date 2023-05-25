# Generated by Django 4.1.3 on 2023-05-25 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_product_categories'),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='product',
            field=models.ManyToManyField(db_constraint=False, related_name='categories', to='products.product'),
        ),
    ]