# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_payload'),
    ]

    operations = [
        migrations.AddField(
            model_name='payload',
            name='aps_text',
            field=models.CharField(default='', max_length=2048),
            preserve_default=False,
        ),
    ]
