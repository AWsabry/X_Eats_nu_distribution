from django.contrib import admin
from categories_and_products.models import Poster,Category, Product, PromoCode, Restaurant, Settings

# Register your models here.






class Categories_Admin(admin.ModelAdmin):
    prepopulated_fields = {'categoryslug': ('Category_name',), }
    list_filter = ("Category_name", "created",)
    list_display = ('Category_name', "created","active","id",)
    search_fields = ['Category_name']

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj=obj, change=change, **kwargs)
        form.base_fields["image"].help_text = " * width: 700, height: 800px are recommended"
        return form

class PromoCodeAdmin(admin.ModelAdmin):
    list_filter = ("active", "Promocode",)
    list_display = ('Promocode', "percentage", 'created', "active")

    search_fields = ['Promocode']


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'productslug': ('name','Restaurant','ArabicName',), }
    list_filter = ("name", "category", "Restaurant", "created")
    list_display = ('name', "price", 'Restaurant', "category",
                     "id", "created","Best_Offer", "Most_Popular","New_Products","active",)
    list_display_links = [
        'name',
        'category',
    ]
    search_fields = ['name']
    list_editable=['active']


class RestaurantAdmin(admin.ModelAdmin):
    prepopulated_fields = {'restaurant_slug': ('Name',), }
    list_display = ("Name","created")
    search_fields = ['Name']

class Poster_Admin(admin.ModelAdmin):
    list_display = ("name","active")





admin.site.register(Category, Categories_Admin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(Settings,)
admin.site.register(Poster,Poster_Admin)


admin.site.register(PromoCode, PromoCodeAdmin)
