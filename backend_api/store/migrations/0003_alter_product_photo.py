# Generated by Django 5.1.4 on 2024-12-06 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name='Фотография'),
        ),
    ]
