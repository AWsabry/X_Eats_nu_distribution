from django.contrib import admin
from cart_and_orders.models import Cart, CartItems, Delivery, Order
import csv
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




    def export_as_csv(self, obj, queryset):
       
        meta = self.model._meta
        field_names = ["product", "quantity",]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response
    export_as_csv.short_description = "Export Selected"
    

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
