# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20181130_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='subject',
            field=models.CharField(max_length=10, default='국어', choices=[('국어', '국어'), ('수학(가)', '수학(가)'), ('수학(나)', '수학(나)'), ('영어', '영어'), ('한국사', '한국사'), ('사회', '사회'), ('과학', '과학'), ('제2외국어_한문', '제2외국어_한문')]),
        ),
    ]
