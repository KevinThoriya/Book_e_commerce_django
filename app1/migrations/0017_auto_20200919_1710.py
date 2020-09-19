# Generated by Django 2.2.7 on 2020-09-19 11:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0016_auto_20200919_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='add_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 19, 11, 40, 41, 632255, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order_details',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 19, 11, 40, 41, 633254, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='add_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 19, 11, 40, 41, 632255, tzinfo=utc)),
        ),
    ]
