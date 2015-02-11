# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decisiontree.multitenancy', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answerlink',
            old_name='answer',
            new_name='linked',
        ),
        migrations.RenameField(
            model_name='entrylink',
            old_name='entry',
            new_name='linked',
        ),
        migrations.RenameField(
            model_name='questionlink',
            old_name='question',
            new_name='linked',
        ),
        migrations.RenameField(
            model_name='sessionlink',
            old_name='session',
            new_name='linked',
        ),
        migrations.RenameField(
            model_name='taglink',
            old_name='tag',
            new_name='linked',
        ),
        migrations.RenameField(
            model_name='tagnotificationlink',
            old_name='tag_notification',
            new_name='linked',
        ),
        migrations.RenameField(
            model_name='transitionlink',
            old_name='transition',
            new_name='linked',
        ),
        migrations.RenameField(
            model_name='treelink',
            old_name='tree',
            new_name='linked',
        ),
        migrations.RenameField(
            model_name='treestatelink',
            old_name='tree_state',
            new_name='linked',
        ),
    ]
