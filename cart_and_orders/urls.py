from django.urls import path
from . import views

app_name = 'cart_and_orders'


urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('order_sent', views.order_sent, name='order_sent'),
    path('email_template', views.email_template, name='email_template'),
    path('order_confirm', view = views.order_confirm, name='order_confirm'),
    path('ThankYou', view = views.ThankYou, name='ThankYou'),
    path('<int:id>', views.deleting, name='deleting'),
    path('checkout',views.checkout,name="checkout"),



    # APIs Handling
    path('get_orders/', view=views.get_orders, name='get_orders'),
    path('get_orders_by_id/<int:id>', view=views.get_orders_by_id, name='get_orders_by_id'),

    path('get_cartItems/', view=views.get_cartItems, name='get_cartItems'),
    path('get_user_cartItems/<str:email>', view=views.get_user_cartItems, name='get_user_cartItems'),
    path('delete_cartItems/<int:id>', view=views.delete_cartItems, name='delete_cartItems'),

    path('get_carts/', view=views.get_carts, name='get_carts'),
    path('get_carts_by_id/<str:email>', view=views.get_carts_by_id, name='get_carts_by_id'),

]
