# Generated by Django 2.2.14 on 2020-09-17 05:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_auto_20200914_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer_banner',
            name='expire',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='add_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 17, 5, 30, 2, 321423, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order_details',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 17, 5, 30, 2, 322288, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='add_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 17, 5, 30, 2, 321816, tzinfo=utc)),
        ),
    ]
