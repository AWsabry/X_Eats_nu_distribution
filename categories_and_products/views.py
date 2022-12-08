from django.shortcuts import redirect, render
from Register_Login.forms import Restaurant_suggestion
from Register_Login.models import Restaurant_Suggestion, TopCustomers
from cart_and_orders.models import Cart, CartItems, Delivery
from categories_and_products.forms import Order_time, QuantityForm
from categories_and_products.models import (
    Category,
    Product,
    Restaurant,
    Settings,
)
from django.http import JsonResponse
from rest_framework import status
from django.contrib import messages
from django.utils.translation import gettext as _
from datetime import datetime, time, timedelta
from django.utils import timezone
import time
from rest_framework.decorators import api_view
from rest_framework.response import Response
from categories_and_products.serializers import CategorySerializer, ProductsSerializer, RestaurantSerializer


def index(request):
    form = Restaurant_suggestion(request.POST)
    customers = TopCustomers.objects.filter(is_active=True)
    email = form.data.get("email")
    city, restaurant_name, reason, city = (
        form.data.get("city"),
        form.data.get("restaurant_name"),
        form.data.get("reason"),
        form.data.get("city"),
    )
    if request.method == "POST":
        Restaurant_Suggestion.objects.create(
            email=email,
            city=city,
            restaurant_name=restaurant_name,
            reason=reason,
        )

    context = {"customers": customers}
    return render(request, "index.html", context)


def Restaurant_view(request):
    restaurant = Restaurant.objects.filter(active=True).order_by("-created")
    categories = Category.objects.filter(active=True)
    context = {"restaurant": restaurant, "categories": categories}
    return render(request, "Restaurant_view.html", context)


def menu(request, restaurant_slug):
    products = Product.objects.filter(
        active=True, Restaurant__restaurant_slug=restaurant_slug
    ).order_by("category")
    categories = Category.objects.filter(
        active=True, Restaurant__restaurant_slug=restaurant_slug
    )
    restaurants = Restaurant.objects.filter(
        active=True, restaurant_slug=restaurant_slug
    )
    context = {
        "products": products,
        "categories": categories,
        "restaurants": restaurants,
    }
    if request.method == "POST":
        if request.user.is_authenticated:
            pass
        else:
            return redirect("Register_Login:login")
    return render(request, "menu.html", context)


def product_details(request, productslug, restaurant_slug):
    quantityForm = QuantityForm(request.POST)
    order_timing_form = Order_time(request.POST)

    products = Product.objects.filter(
        productslug=productslug,
        active=True,
    )
    time_out = Settings.objects.get(id="1")
    start_1_PM = Settings.objects.get(id="2")
    start_3_PM = Settings.objects.get(id="3")
    start_11_AM = Settings.objects.get(id="4")

    now = datetime.now().time()
    end = time_out.end_order

    all_products = Product.objects.filter(
        active=True,
    )
    context = {
        "products": products,
        "all_products": all_products,
        "time_out": time_out,
        "periodic_time": end,
        "now": now,
        "start_1_PM": start_1_PM,
        "start_3_PM": start_3_PM,
        "start_11_AM" : start_11_AM
    }

    if request.method == "POST" and quantityForm.is_valid():
        if request.user.is_authenticated:
            restaurant = Restaurant.objects.get(restaurant_slug=restaurant_slug)

            cart = Cart.objects.get(user=request.user)
            product_data = Product.objects.get(productslug=productslug)
            totalOrderItemPrice = (
                product_data.price * quantityForm.cleaned_data["Quantity"]
            )
            delivery = Delivery.objects.get(city="NU")

            if order_timing_form.is_valid():

                if CartItems.objects.filter(
                    user=request.user, product__productslug=productslug, ordered=False,).exists():
                    cartItem = CartItems.objects.get(
                        user=request.user,
                        product__productslug=productslug,
                        ordered=False,
                    )
                    new_added_product = (
                        quantityForm.cleaned_data["Quantity"] + cartItem.quantity
                    )

                    CartItems.objects.filter(
                        user=request.user, product__productslug=productslug
                    ).update(
                        quantity=new_added_product,
                        totalOrderItemPrice=product_data.price * new_added_product,
                        order_shift=order_timing_form.cleaned_data["timing"],
                    )

                    cart.total_price += totalOrderItemPrice
                    cart.total_after_delivery = (
                        cart.total_price + delivery.delivery_fees
                    )
                    cart.save()

                    # Adding the user to the codes he ordered

                    messages.success(
                        request, _("* Updated in Cart"), extra_tags="danger"
                    )
                    return redirect("cart_and_orders:cart")
                else:
                    
                    if CartItems.objects.filter(
                        user=request.user, ordered=False,).exists():

                        
                        if CartItems.objects.filter(user=request.user,
                        ordered=False,Restaurant__restaurant_slug =restaurant_slug).exists():
                            
                            print('Same or New Restaurant')
                            CartItems.objects.create(
                                user=request.user,
                                cart=cart,
                                product=product_data,
                                price=product_data.price,
                                ordered=False,
                                quantity=quantityForm.cleaned_data["Quantity"],
                                totalOrderItemPrice=totalOrderItemPrice,
                                Restaurant=restaurant,
                                order_shift=order_timing_form.cleaned_data["timing"],
                            )

                            cart.total_price += totalOrderItemPrice

                            cart.total_after_delivery = (
                                cart.total_price + delivery.delivery_fees
                            )
                            cart.save()
                            messages.success(request, _("* Added to cart"), extra_tags="danger")
                            return redirect("cart_and_orders:cart")
                    
                        else:

                            messages.error(request, 'Cannot Order from two restaurants in one order.')
                            print("Another restaurant")
                            return redirect('cart_and_orders:cart')
                    else:
                        CartItems.objects.create(
                                user=request.user,
                                cart=cart,
                                product=product_data,
                                price=product_data.price,
                                ordered=False,
                                quantity=quantityForm.cleaned_data["Quantity"],
                                totalOrderItemPrice=totalOrderItemPrice,
                                Restaurant=restaurant,
                                order_shift=order_timing_form.cleaned_data["timing"],
                            )
                        cart.total_price += totalOrderItemPrice

                        cart.total_after_delivery = (
                                cart.total_price + delivery.delivery_fees
                            )
                        cart.save()
                        messages.success(request, _("* Added to cart"), extra_tags="danger")
                        return redirect("cart_and_orders:cart")
                    
                        
        else:
            messages.success(request, _("* Please Login First"), extra_tags="danger")
            return redirect("Register_Login:login")
    return render(request, "product_details.html", context)


def categories(request):
    products = Product.objects.filter(
        active=True,
    )
    categories = Category.objects.filter(active=True)
    context = {
        "products": products,
        "categories": categories,
    }
    if request.method == "POST":
        if request.user.is_authenticated:
            pass
        else:
            return redirect("Register_Login:login")
    return render(request, "categories.html", context)


def category_details(request, categoryslug, restaurant_slug):
    products = Product.objects.filter(active=True, category__categoryslug=categoryslug)
    categories = Category.objects.filter(active=True, categoryslug=categoryslug)
    category_list = Category.objects.filter(
        active=True, Restaurant__restaurant_slug=restaurant_slug
    )
    restaurant = Restaurant.objects.filter(active=True, restaurant_slug=restaurant_slug)

    context = {
        "products": products,
        "categories": categories,
        "category_list": category_list,
        "restaurant": restaurant,
    }
    if request.method == "POST":
        if request.user.is_authenticated:
            pass
        else:
            return redirect("Register_Login:login")
    return render(request, "categories_details.html", context)


def done(request):
    return render(request, "done.html")


def searched_Page_Restaurants(request):
    searched = request.GET.get("searched")
    searching = (
        Restaurant.objects.all()
        if not str(searched)
        else Restaurant.objects.filter(Name__contains=searched)
    )
    categories = Category.objects.filter(active=True)
    restaurant = Restaurant.objects.filter(active=True)

    context = {
        "searched": searched,
        "searching": searching,
        "categories": categories,
        "restaurant": restaurant,
    }
    return render(request, "searchedPageRestaurants.html", context)


def searched_Page_Restaurants_Products(request, restaurant_slug):
    searched = request.GET.get("searched")
    restaurant = Restaurant.objects.filter(restaurant_slug=restaurant_slug)
    searching = (
        Product.objects.filter(active = True,Restaurant__restaurant_slug=restaurant_slug)
        if not str(searched)
        else Product.objects.filter(active = True,
            Restaurant__restaurant_slug=restaurant_slug, name__contains=searched
        )
    )
    categories = Category.objects.filter(
        Restaurant__restaurant_slug=restaurant_slug, active=True
    )
    all_products = Product.objects.filter(active=True)
    context = {
        "searched": searched,
        "searching": searching,
        "categories": categories,
        "restaurant": restaurant,
        "all_products": all_products,
    }
    return render(request, "searched_Page_Restaurants_Products.html", context)


# APIs Handling

@api_view(['GET','POST'])

# Getting Restaurants

def get_restaurants(request,id):
    if request.method == 'GET':
        all = Restaurant.objects.filter(active = True,id=id)
        serializer = RestaurantSerializer(all,many = True,)
        return JsonResponse({"Names": serializer.data}, safe=False)
    if request.method == 'POST':
        serializer = RestaurantSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)



# Getting Categories

def get_category(request,id):
    if request.method == 'GET':
        all = Category.objects.filter(active = True,id=id)
        serializer = CategorySerializer(all,many = True)
        return JsonResponse({"Names": serializer.data}, safe=False)
    if request.method == 'POST':
        serializer = CategorySerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

# Getting Products
def get_products(request):
    if request.method == 'GET':
        all = Product.objects.filter(active = True)
        serializer = ProductsSerializer(all,many = True)
        return JsonResponse({"Names": serializer.data}, safe=False)
    if request.method == 'POST':
        serializer = ProductsSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
