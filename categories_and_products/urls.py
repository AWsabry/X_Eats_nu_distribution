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
    path('get_category_by_id/<int:id>', view=views.get_category_by_id, name='get_category_by_id'),
    path('get_category_of_restaurants/<int:id>', view=views.get_category_of_restaurants, name='get_category_of_restaurants'),

    
    
    path('get_products/', view=views.get_products, name='get_products'),
    path('get_products_mostSold_products/', view=views.get_products_mostSold_products, name='get_products_mostSold_products'),
    path('get_products_new_products/', view=views.get_products_new_products, name='get_products_new_products'),
    path('get_best_offer_products/', view=views.get_best_offer_products, name='get_best_offer_products'),
    path('get_products_by_id/<int:id>', view=views.get_products_by_id, name='get_products_by_id'),
    path('get_products_by_restaurant_id/<int:id>', view=views.get_products_by_restaurant_id, name='get_products_by_restaurant_id'),
    
    path('get_products_of_restaurant_by_category/<str:restaurantid>/<str:categoryid>', view=views.get_products_of_restaurant_by_category, name='get_products_of_restaurant_by_category'),




    path('get_restaurants_by_id/<int:id>', view=views.get_restaurants_by_id, name='get_restaurants_by_id'),
    path('get_restaurants/', view=views.get_restaurants, name='get_restaurants'),


    path('get_poster/', view=views.get_poster, name='get_poster'),
    

]
