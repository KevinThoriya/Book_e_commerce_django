# Generated by Django 3.0.8 on 2020-09-13 17:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_auto_20200913_2246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer_banner',
            name='offer_expire_date',
        ),
        migrations.AlterField(
            model_name='cart',
            name='add_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 13, 17, 17, 50, 628739, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order_details',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 13, 17, 17, 50, 629767, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='add_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 13, 17, 17, 50, 629767, tzinfo=utc)),
        ),
    ]
