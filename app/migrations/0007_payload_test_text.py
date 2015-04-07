# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_payload_aps_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='payload',
            name='test_text',
            field=models.CharField(default='', max_length=2048),
            preserve_default=False,
        ),
    ]
