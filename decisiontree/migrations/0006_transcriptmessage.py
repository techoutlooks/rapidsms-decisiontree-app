# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decisiontree', '0005_num_tries_default'),
    ]

    operations = [
        migrations.CreateModel(
            name='TranscriptMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('direction', models.CharField(max_length=1, choices=[(b'I', b'Incoming'), (b'O', b'Outgoing')])),
                ('message', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('session', models.ForeignKey(to='decisiontree.Session')),
            ],
            options={
                'ordering': ['created'],
            },
            bases=(models.Model,),
        ),
    ]
