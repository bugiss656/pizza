# Generated by Django 2.2.7 on 2020-05-15 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_shoppingcart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoppingcart',
            old_name='itemName',
            new_name='item_name',
        ),
        migrations.RenameField(
            model_name='shoppingcart',
            old_name='itemPrice',
            new_name='item_price',
        ),
        migrations.RenameField(
            model_name='shoppingcart',
            old_name='itemSize',
            new_name='item_size',
        ),
        migrations.RenameField(
            model_name='shoppingcart',
            old_name='itemToppings',
            new_name='item_toppings',
        ),
    ]
