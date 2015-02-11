# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decisiontree', '0002_auto_20150211_0833'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transition',
            options={'verbose_name': 'path'},
        ),
        migrations.AlterModelOptions(
            name='tree',
            options={'verbose_name': 'survey', 'permissions': [('can_view', 'Can view tree data')]},
        ),
        migrations.AlterModelOptions(
            name='treestate',
            options={'verbose_name': 'survey state'},
        ),
    ]
