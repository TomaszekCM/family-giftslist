# Generated by Django 5.2 on 2025-06-10 14:02

import wishlist.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0003_alter_userext_dob_alter_userext_names_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importantdates',
            name='date',
            field=wishlist.models.MonthDayField(max_length=4, verbose_name='Date'),
        ),
    ]
