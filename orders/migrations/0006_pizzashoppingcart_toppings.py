# Generated by Django 2.2.7 on 2019-12-07 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20191127_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizzashoppingcart',
            name='toppings',
            field=models.CharField(default='', max_length=128),
        ),
    ]
