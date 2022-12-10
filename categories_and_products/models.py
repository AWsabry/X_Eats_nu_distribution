
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.db import models

from X_Eats_nu_distribution import settings


# from cart_and_orders.models import Order

# Create your models here.

class Restaurant(models.Model):
    Name = models.CharField(max_length=250, blank=True, unique=True,null = True)
    restaurant_slug = models.SlugField(unique=True, db_index=True)
    address = models.CharField(max_length=250, blank=True,null = True,)
    image = models.ImageField(
        upload_to="Restaurant", blank=True, )
    delivery_fees = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.Name)

    def get_absolute_url_restaurant(self):
        return reverse('categories_and_products:menu', args=[self.restaurant_slug])
    
    class Meta:
        verbose_name_plural = "Restaurants"




class Category(models.Model):
    Category_name = models.CharField(max_length=250,unique = True,)
    display_name =  models.CharField(max_length=250, blank=True,null = True)
    categoryslug = models.SlugField(unique=True, db_index=True,blank=True,null = True)
    image = models.ImageField(
        upload_to="Categories", blank=True,null = True )
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    Restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, blank=True,null= True)

    
    
    def __str__(self):
        return str(self.Category_name)
        
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url_category(self):
        return reverse('categories_and_products:category_details', args=[self.Restaurant.restaurant_slug] + [self.categoryslug])

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=250, blank=True)
    ArabicName = models.CharField(max_length = 250, blank = True, null= True)
    productslug = models.SlugField(unique=True, db_index=True,)
    Restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, blank=True,null= True)
    description = models.TextField(blank=True)
    price = models.FloatField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True,null = True,)
    boughtPrice = models.FloatField(blank=True, null=True, default=0)
    offerPercentage = models.FloatField(blank=True, null=True,)
    active = models.BooleanField(default=True)
    Most_Popular = models.BooleanField(default=False)
    New_Products = models.BooleanField(default=False)
    Best_Offer = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        arabic_string = self.ArabicName
        arabic_string.encode('unicode-escape')
        return arabic_string

    def get_absolute_url(self):
        return reverse("categories_and_products:product_details", args=[self.Restaurant.restaurant_slug] + [self.productslug])
    
    def get_absolute_searched_url(self):
        return reverse("categories_and_products:searched_Page_Restaurants_Products", args=[self.Restaurant.restaurant_slug])
    
    def discountpercentage(self):
        if self.boughtPrice:
            discountAmount = self.boughtPrice - self.price
            self.offPercentage = (discountAmount/self.oldPrice) * 100
            return (int(self.offPercentage))
        else:
            pass
    offerPercentage = property(discountpercentage)








class Poster(models.Model):
    name = models.CharField(max_length=250, blank=True, unique=True)
    background_image = models.ImageField(
        upload_to="Mobile_Poster", blank=True,)
    active = models.BooleanField(default=True)


class PromoCode(models.Model):
    Promocode = models.CharField(
        max_length=10, unique=True, blank=True, null=True)
    percentage = models.FloatField(default=0.0, validators=[
                                   MinValueValidator(0.0), MaxValueValidator(1.0)], blank=True, null=True,)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    avaliable_time = models.IntegerField(default= 0, blank = True, null = True)


    def __str__(self):
        return self.Promocode

    def save(self, *args, **kwargs):
        self.percentage = round(self.percentage, 2)
        super(PromoCode, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "PromoCodes"


class Settings(models.Model):
    start_order = models.TimeField(auto_now=False,)
    end_order = models.TimeField(auto_now_add=False)
    
    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Settings"