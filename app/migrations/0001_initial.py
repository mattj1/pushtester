# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_id', models.CharField(max_length=64)),
                ('type', models.CharField(max_length=16)),
                ('appKey', models.CharField(max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
