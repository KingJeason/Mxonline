# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-26 19:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20170426_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorg',
            name='image',
            field=models.ImageField(default='image/default.png', upload_to='org/%Y/%m', verbose_name='\u673a\u6784LOGO\u56fe'),
        ),
    ]
