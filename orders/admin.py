from django.contrib import admin

from .models import *
# Register your models here.


admin.site.register(MenuItem)
admin.site.register(MenuItemType)
admin.site.register(PizzaToppings)
admin.site.register(SubToppings)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(ShippingAddress)
