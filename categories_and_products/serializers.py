from rest_framework import serializers
from categories_and_products.models import Restaurant,Category, Product


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['Name',"restaurant_slug", "image", 'created',
                    "active",]



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['Category_name',"display_name", "categoryslug", 'image',
                    "active", "created", "Restaurant",]


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name',"ArabicName", "productslug", 'Restaurant',
                    "description", "price", "category","Most_Popular","New_Products","Best_Offer","created",]