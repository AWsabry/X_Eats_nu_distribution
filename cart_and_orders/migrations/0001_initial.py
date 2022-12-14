# Generated by Django 3.2.3 on 2022-11-02 21:50

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories_and_products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('total_after_delivery', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('Promo_code_user', models.CharField(blank=True, max_length=250, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50, null=True)),
                ('delivery_fees', models.FloatField(default=0)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'DeliveryFees',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('paid', models.BooleanField(default=False)),
                ('comment', models.TextField(blank=True, max_length=2000, null=True)),
                ('totalPrice', models.FloatField(default=0)),
                ('total_price_after_delivery', models.FloatField(default=0, verbose_name='After Delivery')),
                ('flag', models.CharField(blank=True, default='Web', max_length=250, null=True)),
                ('cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cart_and_orders.cart')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('price', models.FloatField(default=0)),
                ('quantity', models.IntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('totalOrderItemPrice', models.PositiveIntegerField(default=0)),
                ('order_shift', models.CharField(blank=True, max_length=50, null=True)),
                ('Restaurant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='categories_and_products.restaurant')),
                ('cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cart_and_orders.cart')),
                ('orderId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart_and_orders.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='categories_and_products.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'CartItems',
            },
        ),
    ]
