# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('panapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='is_scanned',
            field=models.BooleanField(default=False),
        ),
    ]
