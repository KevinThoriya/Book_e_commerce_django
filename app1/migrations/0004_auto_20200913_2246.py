# Generated by Django 3.0.8 on 2020-09-13 17:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_auto_20200913_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='add_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 13, 17, 16, 36, 699274, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='offer_banner',
            name='offer_active_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='offer_banner',
            name='offer_expire_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='order_details',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 13, 17, 16, 36, 701267, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='add_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 13, 17, 16, 36, 700273, tzinfo=utc)),
        ),
    ]
