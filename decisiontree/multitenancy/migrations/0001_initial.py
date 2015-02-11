# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('decisiontree', '0003_auto_20150211_1345'),
        ('multitenancy', '0003_auto_20141115_1029'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('linked', models.OneToOneField(related_name='tenantlink', to='decisiontree.Answer')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, to='multitenancy.Tenant', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EntryLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('linked', models.OneToOneField(related_name='tenantlink', to='decisiontree.Entry')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, to='multitenancy.Tenant', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('linked', models.OneToOneField(related_name='tenantlink', to='decisiontree.Question')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, to='multitenancy.Tenant', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SessionLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('linked', models.OneToOneField(related_name='tenantlink', to='decisiontree.Session')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, to='multitenancy.Tenant', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('linked', models.OneToOneField(related_name='tenantlink', to='decisiontree.Tag')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, to='multitenancy.Tenant', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagNotificationLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('linked', models.OneToOneField(related_name='tenantlink', to='decisiontree.TagNotification')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, to='multitenancy.Tenant', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransitionLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('linked', models.OneToOneField(related_name='tenantlink', to='decisiontree.Transition')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, to='multitenancy.Tenant', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TreeLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('linked', models.OneToOneField(related_name='tenantlink', to='decisiontree.Tree')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, to='multitenancy.Tenant', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TreeStateLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('linked', models.OneToOneField(related_name='tenantlink', to='decisiontree.TreeState')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, to='multitenancy.Tenant', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
