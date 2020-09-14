# Generated by Django 3.0.5 on 2020-09-14 17:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_auto_20200914_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='add_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 14, 17, 43, 13, 913158, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order_details',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 14, 17, 43, 13, 914111, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='add_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 14, 17, 43, 13, 913590, tzinfo=utc)),
        ),
    ]
