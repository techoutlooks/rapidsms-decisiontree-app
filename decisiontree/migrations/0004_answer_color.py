# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorful.fields


class Migration(migrations.Migration):

    dependencies = [
        ('decisiontree', '0003_auto_20150211_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='color',
            field=colorful.fields.RGBColorField(default='#000000'),
            preserve_default=True,
        ),
    ]
