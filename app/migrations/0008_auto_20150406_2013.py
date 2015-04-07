# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_payload_test_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payload',
            name='aps_text',
        ),
        migrations.RemoveField(
            model_name='payload',
            name='test_text',
        ),
    ]
