# Generated by Django 2.2.7 on 2020-06-28 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0032_auto_20200607_1946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='toppings',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='toppings',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]