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
]
