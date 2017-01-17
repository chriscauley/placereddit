# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reddit', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='x_crop_order',
        ),
        migrations.RemoveField(
            model_name='image',
            name='y_crop_order',
        ),
    ]
