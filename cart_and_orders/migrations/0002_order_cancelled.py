# Generated by Django 3.2.3 on 2022-12-25 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_and_orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cancelled',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]