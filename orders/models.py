from django.db import models
from django.contrib.auth.models import User
from datetime import datetime



class MenuItemType(models.Model):
    item_type = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.item_type



class MenuItem(models.Model):
    name = models.CharField(max_length=128, null=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    shape = models.CharField(max_length=64, blank=True, null=True)
    size = models.CharField(max_length=128, default='', blank=True)
    toppings_number = models.IntegerField(default=0, blank=True)
    menu_position = models.IntegerField(default=0, blank=True)

    type = models.ForeignKey(MenuItemType, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.size} {self.name} {self.type}'

    @property
    def MenuItemName(self):
        return f'{self.size} {self.name} {self.type}'

    def getRegularSmPizza():
        return MenuItem.objects.filter(shape='regular').filter(size='small').order_by('menu_position')

    def getRegularLgPizza():
        return MenuItem.objects.filter(shape='regular').filter(size='large').order_by('menu_position')

    def getSicilianSmPizza():
        return MenuItem.objects.filter(shape='sicilian').filter(size='small').order_by('menu_position')

    def getSicilianLgPizza():
        return MenuItem.objects.filter(shape='sicilian').filter(size='large').order_by('menu_position')

    def getSmSub():
        return MenuItem.objects.filter(type__item_type='sub').filter(size='small').order_by('menu_position')

    def getLgSub():
        return MenuItem.objects.filter(type__item_type='sub').filter(size='large').order_by('menu_position')

    def getOtherSmSub():
        return MenuItem.objects.filter(type__item_type='othersub').filter(size='small').order_by('menu_position')

    def getOtherLgSub():
        return MenuItem.objects.filter(type__item_type='othersub').filter(size='large').order_by('menu_position')

    def getPasta():
        return MenuItem.objects.filter(type__item_type='pasta').order_by('menu_position')

    def getSalad():
        return MenuItem.objects.filter(type__item_type='salad').order_by('menu_position')

    def getSmDinner():
        return MenuItem.objects.filter(type__item_type='dinner').filter(size='small').order_by('menu_position')

    def getLgDinner():
        return MenuItem.objects.filter(type__item_type='dinner').filter(size='large').order_by('menu_position')



class PizzaToppings(models.Model):
    name = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.name

    def getPizzaToppings():
        return PizzaToppings.objects.all()



class SubToppings(models.Model):
    name = models.CharField(max_length=128, null=True)
    price = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

    def getSubToppings():
        return SubToppings.objects.all()

    def getExtraCheese():
        return SubToppings.objects.filter(name='Extra cheese')



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order_confirmed = models.BooleanField(default=False)
    order_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def getCartTotalCost(self):
        order_items = self.orderitem_set.all()
        cart_total_cost = sum([item.getItemTotalCost for item in order_items])
        return cart_total_cost



class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=128, null=True)
    apartment_number = models.CharField(max_length=128, null=True)
    city = models.CharField(max_length=128, null=True)
    state = models.CharField(max_length=128, null=True)
    postal_code = models.CharField(max_length=128, null=True)
    phone_number = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.address



class OrderItem(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    toppings = models.CharField(max_length=128, blank=True, null=True)

    @property
    def getItemTotalCost(self):
        total_cost = self.menu_item.price * self.quantity
        return total_cost
