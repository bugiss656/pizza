# Generated by Django 2.2.7 on 2019-11-27 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20191127_1238'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pizza',
            old_name='pizza_lg_price',
            new_name='pizza_price',
        ),
        migrations.RenameField(
            model_name='pizza',
            old_name='pizza_shape_1',
            new_name='pizza_shape',
        ),
        migrations.RenameField(
            model_name='pizza',
            old_name='pizza_shape_2',
            new_name='pizza_size',
        ),
        migrations.RemoveField(
            model_name='pizza',
            name='pizza_size_1',
        ),
        migrations.RemoveField(
            model_name='pizza',
            name='pizza_size_2',
        ),
        migrations.RemoveField(
            model_name='pizza',
            name='pizza_sm_price',
        ),
    ]
