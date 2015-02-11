# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decisiontree', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tree',
            name='trigger',
            field=models.CharField(help_text=b'The incoming message which triggers this Tree.', unique=True, max_length=30, verbose_name=b'Keyword'),
            preserve_default=True,
        ),
    ]
