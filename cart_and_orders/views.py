from datetime import datetime
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from Register_Login.models import Profile
from cart_and_orders.forms import BromoCodeForm, CommentForm
from cart_and_orders.models import Cart, CartItems, Delivery, Order

# Rest Libraries
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.response import Response
from rest_framework import status
from cart_and_orders.serializers import (
    Cart_Serializer,
    CartItems_Serializer,
    Orders_Serializer,
)
from django.http import JsonResponse
from rest_framework.parsers import JSONParser


from categories_and_products.models import Category, PromoCode, Settings

# Create your views here.


def send_code_email(request, order_components, cart):
    subject, from_email, to = (
        " Finally X-Eats Team recieved your order, Your order has been made successfully !",
        "noreply@x-eats.com",
        request.user.email,
    )
    text_content = "This is an important message."
    context = {"order_components": order_components, "user": request.user, "cart": cart}
    html_content = render_to_string("order_sent.html", context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    messages.success(request, _("Check YOUR ORDERS section or you Email"))


def discounts(request, code):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        if PromoCode.objects.filter(active=True, Promocode=code).exists():
            if cart.Promo_code_user == code:
                messages.error(
                    request, _("*Promo Code is Applied Before"), extra_tags="danger"
                )
                return redirect("cart_and_orders:cart")
            else:
                delivery = Delivery.objects.get(city="NU")

                Promo_code = PromoCode.objects.get(Promocode=code)

                getting_price = cart.total_price * Promo_code.percentage
                final_after_promotion = cart.total_after_delivery - getting_price

                getting_price_before_delivery = cart.total_price * Promo_code.percentage
                before_delivery = cart.total_price - getting_price_before_delivery

                cart = Cart.objects.filter(user=request.user).update(
                    total_price=before_delivery,
                    total_after_delivery=final_after_promotion,
                    Promo_code_user=code,
                )
                messages.error(
                    request, _("*Promo Code is Applied"), extra_tags="danger"
                )
                return redirect("cart_and_orders:cart")
        else:
            messages.error(request, _("*Invalid"), extra_tags="danger")
            return redirect("cart_and_orders:cart")

    else:
        messages.error(request, _("* Please Login First !"), extra_tags="danger")
        return redirect("Register_Login:login")


def order_confirm(request):

    cart = Cart.objects.get(user=request.user)

    # Creating Order ID
    order_sent = Order.objects.create(
        user=request.user,
        totalPrice=cart.total_price,
        cart=cart,
    )

    # Updating the cartItem with the order id that's ordered
    CartItems.objects.filter(user=request.user, ordered=False,).update(
        orderId=order_sent.id,
    )

    order_components = CartItems.objects.filter(
        user=request.user,
        orderId=order_sent.id,
    )

    cart = Cart.objects.filter(user=request.user)

    # Updating the total price in the cart

    # Sending Email
    if order_sent:

        # send_code_email(request, order_components, cart)
        CartItems.objects.filter(user=request.user, orderId=order_sent.id,).update(
            ordered=True,
        )
        Cart.objects.filter(user=request.user).update(
            total_price=0, total_after_delivery=10, Promo_code_user=None
        )
        return redirect("cart_and_orders:ThankYou")

    return render(request, "order_confirmation.html")


def email_template(request):
    return render(request, "email_template.html")


def order_sent(request):
    return render(request, "order_sent.html")


def cart(request):
    if request.user.is_authenticated:
        cartItems = CartItems.objects.filter(user=request.user, ordered=False)
        cart = Cart.objects.filter(user=request.user)
        profile = Profile.objects.get(email=request.user)
        delivery = Delivery.objects.filter(city="NU")
        form = BromoCodeForm(request.POST)

        if request.method == "POST" and form.is_valid():
            code = form.cleaned_data["code"]

            if cartItems.exists():
                discounts(request, str(code))
            else:
                Cart.objects.filter(user=request.user).update(
                    total_price=0, total_after_delivery=10
                )
                messages.error(
                    request,
                    _("* Your Cart is Empty, Please add to cart first"),
                    extra_tags="danger",
                )
        context = {
            "cartItems": cartItems,
            "cart": cart,
            "delivery": delivery,
        }
    else:
        messages.error(request, _("Please Login First !"), extra_tags="danger")
        return redirect("Register_Login:login")

    return render(request, "cart.html", context)


def ThankYou(request):
    return render(request, "ThankYou.html")


def deleting(request, id):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cartItem = CartItems.objects.get(user=request.user, ordered=False, id=id)
        delivery = Delivery.objects.get(city="NU")

        deleteing = CartItems.objects.filter(
            user=request.user, ordered=False, id=id
        ).delete()
        if deleteing:
            if cartItem.price > cart.total_price:
                Cart.objects.filter(user=request.user).update(
                    total_price=0, total_after_delivery=10
                )

            else:
                new_total_after_deleting = cart.total_price - (
                    cartItem.price * cartItem.quantity
                )
                Cart.objects.filter(user=request.user).update(
                    total_price=new_total_after_deleting,
                    total_after_delivery=new_total_after_deleting
                    + delivery.delivery_fees,
                )

            messages.error(request, _("* Removed From Cart "), extra_tags="danger")
            return redirect("cart_and_orders:cart")
    else:
        messages.error(request, _("* Please Login First !"), extra_tags="danger")
        return redirect("Register_Login:login")
    return render(request, "deleting.html")


def checkout(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        form = CommentForm(request.POST)
        delivery = Delivery.objects.filter(city="NU")
        cartItems = CartItems.objects.filter(
            user=request.user,
            ordered=False,
        )
        profile = Profile.objects.filter(email=request.user)
        time_out = Settings.objects.get(id="1")

        now = datetime.now().time()
        end = time_out.end_order

        if request.method == "POST":
            if cartItems.exists():
                return redirect("cart_and_orders:order_confirm")
            else:
                Cart.objects.filter(user=request.user).update(
                    total_price=0, total_after_delivery=10
                )
                messages.error(
                    request,
                    _("* Your Cart is Empty, Please add to cart first"),
                    extra_tags="danger",
                )

    else:
        messages.error(request, _("Please Login First !"), extra_tags="danger")
        return redirect("Register_Login:login")

    context = {
        "cart": cart,
        "cartItems": cartItems,
        "delivery": delivery,
        "profile": profile,
        "now": now,
        "end": end,
        "time_out": time_out,
    }
    return render(request, "checkout.html", context)


# API Handling

# Deleting CartItems
@api_view(["GET", "DELETE"])
def delete_cartItems(request, id):
    if request.method == "GET":
        all = CartItems.objects.filter(id=id, ordered=False)
        serializer = CartItems_Serializer(all, many=True)
        return JsonResponse({"Names": serializer.data}, safe=False)

    if request.method == "DELETE":
        deleting = CartItems.objects.get(
            id=id,
        )
        deleting.delete()
        return Response(status=status.HTTP_201_CREATED)


# Getting CartItems
@api_view(["GET", "PUT", "DELETE", "POST"])
def get_cartItems(request):
    if request.method == "GET":
        all = CartItems.objects.all()
        serializer = CartItems_Serializer(all, many=True)
        return JsonResponse({"Names": serializer.data}, safe=False)
    if request.method == "POST":
        serializer = CartItems_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# Getting User CartItems
@api_view(["GET", "PUT", "DELETE", "POST"])
def get_user_cartItems(request, email):
    if request.method == "GET":
        all = CartItems.objects.filter(user__email=email, ordered=False)
        serializer = CartItems_Serializer(all, many=True)
        return JsonResponse({"Names": serializer.data}, safe=False)

    if request.method == "POST":
        serializer = CartItems_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# Getting Carts
@api_view(["GET", "PUT", "DELETE", "POST"])
def get_carts(request):
    if request.method == "GET":
        all = Cart.objects.all()
        serializer = Cart_Serializer(all, many=True)
        return JsonResponse({"Names": serializer.data}, safe=False)

    if request.method == "POST":
        serializer = Cart_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == "PUT":
        serializer = Cart_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# Getting Carts by ID
@api_view(["GET", "PUT", "POST"])
def get_carts_by_id(request, email):
    if request.method == "GET":
        all = Cart.objects.filter(user__email=email)
        serializer = Cart_Serializer(all, many=True)
        return JsonResponse({"Names": serializer.data}, safe=False)

    if request.method == "POST":
        serializer = Cart_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == "PUT":
        serializer = Cart_Serializer(data=request.data, partial=True)
        print(request.data["total_after_delivery"])
        if request.data != None:
            Cart.objects.update(
                total_price=request.data["total_price"],
                total_after_delivery=request.data["total_after_delivery"],
            ),
            return Response(request.data, status=status.HTTP_200_OK)
        else:
            return Response('Data is Null', status=status.HTTP_304_NOT_MODIFIED)


# Getting Orders
@api_view(["GET", "PUT", "POST"])
def get_orders(request):
    if request.method == "GET":
        all = Order.objects.all()
        serializer = Orders_Serializer(all, many=True)
        return JsonResponse({"Names": serializer.data}, safe=False)
    if request.method == "POST":
        serializer = Orders_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# Getting Orders by Id
@api_view(["GET", "PUT", "POST"])
def get_orders_by_id(request, id):
    if request.method == "GET":
        all = Order.objects.filter(id=id)
        serializer = Orders_Serializer(all, many=True)
        return JsonResponse({"Names": serializer.data}, safe=False)
    if request.method == "POST":
        serializer = Orders_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
