from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("menu/", views.menu, name="menu"),
    path("order/", views.order, name="order"),

    path("shopping/", views.viewShoppingCart, name="shopping"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.user_register, name="register"),

    path("addItem/", views.addItemToShoppingCart, name="addItem"),
    path("updateItem/", views.updateItemQuantity, name="updateItem"),

    path("removeItem/<int:id>", views.removeItemFromShoppingCart, name="removeItem"),

    path("placeOrder/", views.placeOrder, name="placeOrder"),
    path("confirmOrder/", views.confirmOrder, name="confirmOrder"),

    path("orders/", views.adminOrdersView, name="ordersView"),
    path("deleteOrder/<int:id>", views.deleteCompletedOrder, name="deleteOrder")
]
