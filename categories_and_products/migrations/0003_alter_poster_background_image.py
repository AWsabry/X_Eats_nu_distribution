# Generated by Django 3.2.3 on 2022-12-17 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories_and_products', '0002_auto_20221204_0117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poster',
            name='background_image',
            field=models.ImageField(blank=True, upload_to='Mobile_Poster'),
        ),
    ]