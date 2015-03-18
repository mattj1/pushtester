# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_pushservice'),
    ]

    operations = [
        migrations.AddField(
            model_name='pushservice',
            name='app_type',
            field=models.CharField(default='android', max_length=16),
            preserve_default=False,
        ),
    ]
