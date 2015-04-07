# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20150406_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='payload',
            name='aps_text',
            field=models.CharField(max_length=2048, null=True),
            preserve_default=True,
        ),
    ]
