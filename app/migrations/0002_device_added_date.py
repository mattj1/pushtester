# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 17, 21, 52, 18, 261790, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
