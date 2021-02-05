from .models import Order, OrderItem


def cartItemsQuantity(request):

    if request.user.is_authenticated:
        user = request.user

        order, created = Order.objects.get_or_create(user=user, order_confirmed=False)

        cart_items = order.orderitem_set.all()
        cart_items_quantity = len(cart_items)
    else:
        cart_items_quantity = ''

    return {
        'cart_items_quantity': cart_items_quantity
    }



def cartTotalCost(request):

    if request.user.is_authenticated:
        user = request.user

        order = Order.objects.get(user=user, order_confirmed=False)
        cart_total_cost = order.getCartTotalCost
    else:
        cart_total_cost = ''

    return {
        'cart_total_cost': cart_total_cost
    }
