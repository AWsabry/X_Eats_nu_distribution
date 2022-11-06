from django.contrib import admin
from cart_and_orders.models import Cart, CartItems, Delivery, Order
from .models import CartItems
import pandas as pd
from django.db.models import F
from django.http import HttpResponse

from categories_and_products.models import Product

class CartItemsAdmin(admin.TabularInline):
    model = CartItems
    # raw_id_fields = ['product']


class CartAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'total_price',
                    'total_after_delivery',
                    'ordered_date',
                    'Cart_Name',
                    'PhoneNumber',

                    ]
    inlines = [
        CartItemsAdmin,
    ]
    search_fields = ['user']

    


    
    
    def Cart_Name(self, obj):
        return   str(obj.user.first_name) + " " + str(obj.user.last_name)
      

    def PhoneNumber(self, obj):
        return obj.user.PhoneNumber



class OrderAdmin(admin.ModelAdmin):
    
    list_display = ['user',
                    'total_price_after_delivery',
                    'paid',
                    'ordered_date',
                    'id',
                    'OrderName',
                    'PhoneNumber',
                    'NU_id',
                    ]

    inlines = [
        CartItemsAdmin,
    ]

    list_filter = ['paid',
                   'ordered_date',
                   
                   ]
    search_fields = ['user__first_name']


    def OrderName(self, obj):

        return   str(obj.user.first_name) + " " + str(obj.user.last_name)
      

    def PhoneNumber(self, obj):
        return obj.user.PhoneNumber

    def NU_id(self, obj):
        return obj.user.nu_id


    

class CartItemssAdmin(admin.ModelAdmin):
    list_display = ('user','ordered', 'created')
    list_filter = ('ordered',  'created')
    actions = ["export_as_csv",]

    @admin.action(description='Export Selected')
    def export_as_csv(self, request, queryset):
        vals = ["product_id", "product_name", "product_arabicname","restaurant_name", "price", "bought_price", "quantity"]
        new_queryset = queryset.annotate(
            product_name=F("product__name"),
            product_arabicname=F("product__ArabicName"),
            bought_price=F("product__boughtPrice"),
            restaurant_name=F("Restaurant__Name"),
            ).values_list(*vals)
        
        df = pd.DataFrame(new_queryset, columns=vals)
        new_df = df.groupby(["product_id", "product_name", "product_arabicname", "restaurant_name", "price", "bought_price"], as_index=False)["quantity"].aggregate(sum)
        new_df["total_price"] = new_df["price"] * new_df["quantity"]
        new_df["total_bought_price"] = new_df["bought_price"] * new_df["quantity"]
        new_df["profit"] = new_df["total_price"] - new_df["total_bought_price"]
        
        new_df.loc["Totals"] = new_df.agg({
            'quantity': 'sum', 
            'total_price': 'sum', 
            'total_bought_price': 'sum', 
            'profit':'sum'
            })

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=summary.xlsx'
        
        new_df.to_excel(response)
        
        return response

class DeliveryfeesAdmin(admin.ModelAdmin):
    list_filter = ("city", "delivery_fees",)
    list_display = ('city', "delivery_fees", 'ordered_date','active')
    search_fields = ['city']


admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
# admin.site.register(Codes,CodeAdmin)
admin.site.register(Delivery, DeliveryfeesAdmin)
admin.site.register(CartItems,CartItemssAdmin)
# admin.site.register(BromoCode, BromoCodeAdmin)
