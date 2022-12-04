from django.urls import path
from . import views


app_name = 'categories_and_products'


urlpatterns = [
    path('',views.index,name='index',),
    path('Restaurant_view/<slug:restaurant_slug>',views.menu,name='menu'),
    path('categories',views.categories,name='categories'),
    path('product/<slug:restaurant_slug>/<slug:productslug>',views.product_details,name='product_details'),
    path('Restaurant_view/<slug:restaurant_slug>/<slug:categoryslug>',views.category_details,name='category_details'),
    path('Restaurant_view',views.Restaurant_view,name='Restaurant_view'),
    path('searched_Page_Restaurants',views.searched_Page_Restaurants,name='searched_Page_Restaurants'),
    path('Restaurant_view/<slug:restaurant_slug>/searched_Page_Restaurants_Products/',views.searched_Page_Restaurants_Products,name='searched_Page_Restaurants_Products'),
    path('done',views.done,name='done'),

    
    # APIs URL

    path('get_category/', view=views.get_category, name='get_category'),
    path('get_products/', view=views.get_products, name='get_products'),
    path('get_restaurants/', view=views.get_restaurants, name='get_restaurants'),
]
