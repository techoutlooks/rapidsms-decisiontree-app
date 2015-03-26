# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decisiontree', '0004_answer_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='num_tries',
            field=models.PositiveIntegerField(default=0, help_text=b'The number of times the user has tried to answer the current question.'),
            preserve_default=True,
        ),
    ]
