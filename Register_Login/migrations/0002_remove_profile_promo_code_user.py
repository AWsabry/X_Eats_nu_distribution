# Generated by Django 3.2.3 on 2022-10-31 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Register_Login', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='Promo_code_user',
        ),
    ]
