# Generated by Django 2.2.7 on 2020-07-16 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0038_shippingaddress_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='phone_number',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
