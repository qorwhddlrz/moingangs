# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_post_schoolyear'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='grade',
            field=models.CharField(max_length=6, default='고1', choices=[('고1', '고1'), ('고2', '고2'), ('고3', '고3')]),
        ),
        migrations.AlterField(
            model_name='post',
            name='price',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(50000), django.core.validators.MaxValueValidator(100000000)]),
        ),
    ]
