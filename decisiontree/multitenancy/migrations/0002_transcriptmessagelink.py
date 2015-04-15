# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('decisiontree', '0006_transcriptmessage'),
        ('multitenancy', '0003_auto_20141115_1029'),
        ('decisiontree_multitenancy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TranscriptMessageLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('linked', models.OneToOneField(related_name='tenantlink', to='decisiontree.TranscriptMessage')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, to='multitenancy.Tenant', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
