from email.policy import default
from enum import unique
from profile import Profile
from urllib import request
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from categories_and_products.models import Category, Product, PromoCode,Restaurant
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.urls import reverse
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import Group
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.



class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,unique = True)
    total_price = models.FloatField(default=0, validators=[MinValueValidator(0.0)])
    total_after_delivery = models.FloatField(default=0,  validators=[MinValueValidator(0.0),],)
    ordered_date = models.DateTimeField(auto_now_add=True)
    Promo_code_user = models.CharField(max_length = 250, blank = True, null= True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("cart_and_orders:discounts",)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,null=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    comment = models.TextField(max_length=2000, blank=True, null=True)
    totalPrice = models.FloatField(default=0)
    total_price_after_delivery = models.FloatField(
        default=0, verbose_name='After Delivery')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    flag = models.CharField(max_length = 250, blank = True, null= True,default="Web")
    cancelled = models.BooleanField(default=False,blank = True, null= True)
    
    

    def __str__(self):
        return str(self.id)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    


@receiver(pre_save, sender=Order)
def calculatedFromSales(sender, **kwargs):
    orders = kwargs['instance']
    delivery = Delivery.objects.get(city="NU")
    total_price_after_delivery = orders.totalPrice + \
        delivery.delivery_fees
    orders.total_price_after_delivery = total_price_after_delivery


@receiver(post_save, sender=Profile)
def operation_group(sender, instance, **kwargs):
    group = Group.objects.filter(name='Operations').first()
    if group and instance.is_operation:
        group.user_set.add(instance)
    else:
        group.user_set.remove(instance)  



class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,null=True)
    orderId = models.ForeignKey(
        Order, on_delete=models.CASCADE, null = True, blank=True)
    ordered = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=1, name='quantity')
    created = models.DateTimeField(auto_now_add=True)
    totalOrderItemPrice = models.PositiveIntegerField(default=0)
    Restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, blank=True,null= True)
    order_shift = models.CharField(max_length=50, null=True, name='order_shift',blank = True)
    
    
    class Meta:
        verbose_name_plural = "CartItems"

    def deleteing_item(self):
        return reverse('cart_and_orders:deleting', args=[self.id])

    def __unicode__(self):
        return u'%s',(self.product.ArabicName)
        
    def __str__(self):
        return str(self.user.email) + " " + str(self.product)



class Delivery(models.Model):
    city = models.CharField(max_length=50, null=True)
    delivery_fees = models.FloatField(default=0)
    ordered_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)


    def __str__(self):
        return str(self.city) + " " + str(self.delivery_fees) + "EGP"

    
    class Meta:
        verbose_name_plural = "DeliveryFees"