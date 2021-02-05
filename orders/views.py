from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.template import RequestContext, Context

from django.db.models import Sum, Count

import datetime
import json

from .forms import UserRegisterForm, ShippingAddressForm
from .models import *


from django.contrib.sessions.models import Session
Session.objects.all().delete()



# Create your views here.

def home(request):
    return render(request, 'orders/home.html')



def menu(request):

    context = {
        'rgl_sm_pizza': MenuItem.getRegularSmPizza(),
        'rgl_lg_pizza': MenuItem.getRegularLgPizza(),
        'scln_sm_pizza': MenuItem.getSicilianSmPizza(),
        'scln_lg_pizza': MenuItem.getSicilianLgPizza(),

        'sm_sub': MenuItem.getSmSub(),
        'lg_sub': MenuItem.getLgSub(),

        'other_sm_sub': MenuItem.getOtherSmSub(),
        'other_lg_sub': MenuItem.getOtherLgSub(),

        'pasta': MenuItem.getPasta(),
        'salad': MenuItem.getSalad(),

        'sm_dinner': MenuItem.getSmDinner(),
        'lg_dinner': MenuItem.getLgDinner(),

        'pizza_toppings': PizzaToppings.getPizzaToppings(),
        'sub_toppings': SubToppings.getSubToppings()
    }

    return render(request, 'orders/menu.html', context)


@login_required
def order(request):

    context = {
        'rgl_sm_pizza': MenuItem.getRegularSmPizza(),
        'rgl_lg_pizza': MenuItem.getRegularLgPizza(),
        'scln_sm_pizza': MenuItem.getSicilianSmPizza(),
        'scln_lg_pizza': MenuItem.getSicilianLgPizza(),

        'sm_sub': MenuItem.getSmSub(),
        'lg_sub': MenuItem.getLgSub(),

        'other_sm_sub': MenuItem.getOtherSmSub(),
        'other_lg_sub': MenuItem.getOtherLgSub(),

        'pasta': MenuItem.getPasta(),
        'salad': MenuItem.getSalad(),

        'sm_dinner': MenuItem.getSmDinner(),
        'lg_dinner': MenuItem.getLgDinner(),

        'pizza_toppings': PizzaToppings.getPizzaToppings(),
        'sub_toppings': SubToppings.getSubToppings(),
        'extra_cheese_topping': SubToppings.getExtraCheese()
    }

    return render(request, 'orders/order.html', context)


# Displaying cart items for specific user
def viewShoppingCart(request):

    if request.user.is_authenticated:
        user = request.user

        order = Order.objects.get(user=user, order_confirmed=False)
        cart_items = order.orderitem_set.all().order_by('id')

        context = {
            'cart_items': cart_items,
            'order': order
        }

        return render(request, 'orders/shoppingCart.html', context)


# Adding menu item to shopping cart from order view
def addItemToShoppingCart(request):

    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user

        data = json.loads(request.body)
        item_id = data['id']
        item_toppings = data['toppings']
        action = data['action']

        menu_item = MenuItem.objects.get(id=item_id)

        order, created = Order.objects.get_or_create(user=user, order_confirmed=False)

        if item_toppings:
            order_item, created = OrderItem.objects.get_or_create(menu_item=menu_item, order=order, toppings=item_toppings)

            if action == 'add':
                order_item.quantity = (order_item.quantity + 1)
            elif action == 'remove':
                order_item.quantity = (order_item.quantity - 1)

            order_item.save()

            if order_item.quantity <= 0:
                order_item.delete()
        else:
            order_item, created = OrderItem.objects.get_or_create(menu_item=menu_item, order=order)

            if action == 'add':
                order_item.quantity = (order_item.quantity + 1)
            elif action == 'remove':
                order_item.quantity = (order_item.quantity - 1)

            order_item.save()

            if order_item.quantity <= 0:
                order_item.delete()

        return JsonResponse('Item succesfully added to cart', safe=False)


# Updating shopping cart items quantity in shopping cart view
def updateItemQuantity(request):

    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user

        data = json.loads(request.body)
        item_id = data['id']
        item_toppings = data['toppings']
        action = data['action']

        menu_item = MenuItem.objects.get(id=item_id)

        order = Order.objects.get(user=user, order_confirmed=False)

        if item_toppings:
            order_item = OrderItem.objects.get(menu_item=menu_item, order=order, toppings=item_toppings)

            if action == 'add':
                order_item.quantity = (order_item.quantity + 1)
            elif action == 'remove':
                order_item.quantity = (order_item.quantity - 1)

            order_item.save()

            if order_item.quantity <= 0:
                order_item.delete()

        else:
            order_item = OrderItem.objects.get(menu_item=menu_item, order=order)

            if action == 'add':
                order_item.quantity = (order_item.quantity + 1)
            elif action == 'remove':
                order_item.quantity = (order_item.quantity - 1)

            order_item.save()

            if order_item.quantity <= 0:
                order_item.delete()

    return JsonResponse('Item quantity succesfully updated', safe=False)


# Deleting item from shopping cart
@login_required
def removeItemFromShoppingCart(request, id):

    if request.user.is_authenticated:
        user = request.user

    order = Order.objects.get(user=user, order_confirmed=False)

    order_item = order.orderitem_set.filter(id=id).delete()

    return redirect('shopping')



@login_required
def placeOrder(request):

    if request.user.is_authenticated:
        user = request.user

    order = Order.objects.get(user=user, order_confirmed=False)
    cart_items = order.orderitem_set.all().order_by('id')

    context = {
        'cart_items': cart_items,
        'order': order
    }

    return render(request, 'orders/placeOrder.html', context)



@login_required
def confirmOrder(request):

    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user

        order = Order.objects.get(user=user, order_confirmed=False)
        cart_items = order.orderitem_set.all().order_by('id')

        form = ShippingAddressForm(request.POST)

        if form.is_valid():

            address = form.cleaned_data.get('address')
            apartment_number = form.cleaned_data.get('apartment_number')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            postal_code = form.cleaned_data.get('postal_code')
            phone_number = form.cleaned_data.get('phone_number')

            order = Order.objects.get(user=user, order_confirmed=False)

            ShippingAddress.objects.create(user=user, order=order, address=address, apartment_number=apartment_number, city=city, state=state, postal_code=postal_code, phone_number=phone_number)

            Order.objects.filter(user=user, order_confirmed=False).update(order_confirmed=True, order_time=datetime.now())

            messages.success(request, f'Order was placed successfully.')

            return redirect('order')
        else:
            messages.warning(request, f'Complete all necessary fields.')
    else:
        form = ShippingAddressForm()

    context = {
        'cart_items': cart_items,
        'order': order,
        'form': form
    }

    return render(request, "orders/placeOrder.html", context)



@login_required
def adminOrdersView(request):

    orders = Order.objects.filter(order_confirmed=True).all().order_by('order_time')

    context = {
        "orders": orders
    }

    return render(request, "orders/adminOrdersView.html", context)



def deleteCompletedOrder(request, id):

    if request.user.is_authenticated:
        user = request.user

        order = Order.objects.get(id=id)
        order_items = order.orderitem_set.all().delete()
        shipping_address = order.shippingaddress_set.all().delete()
        order.delete()

        return redirect('ordersView')



def user_register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}.')

            return redirect('login')
        else:
            messages.warning(request, f'Fields completed incorrectly, try again.')
    else:
        form = UserRegisterForm()

    return render(request, "orders/register.html", {"form": form})



def user_login(request):

    if request.method == 'POST':
        username = request.POST["login-username"]
        password = request.POST["login-password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'You have been successfully loged in.')

            return redirect('menu')
        else:
            messages.warning(request, f'Username or password incorrect.')

    return render(request, "orders/login.html")



@login_required
def user_logout(request):

    logout(request)
    messages.success(request, f'You have been log out.')

    return redirect('login')
