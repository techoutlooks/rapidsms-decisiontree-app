# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('multitenancy', '0003_auto_20141115_1029'),
        ('decisiontree', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.OneToOneField(related_name='tenantlink', to='decisiontree.Answer')),
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
                ('entry', models.OneToOneField(related_name='tenantlink', to='decisiontree.Entry')),
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
                ('question', models.OneToOneField(related_name='tenantlink', to='decisiontree.Question')),
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
                ('session', models.OneToOneField(related_name='tenantlink', to='decisiontree.Session')),
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
                ('tag', models.OneToOneField(related_name='tenantlink', to='decisiontree.Tag')),
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
                ('tag_notification', models.OneToOneField(related_name='tenantlink', to='decisiontree.TagNotification')),
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
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, to='multitenancy.Tenant', null=True)),
                ('transition', models.OneToOneField(related_name='tenantlink', to='decisiontree.Transition')),
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
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, to='multitenancy.Tenant', null=True)),
                ('tree', models.OneToOneField(related_name='tenantlink', to='decisiontree.Tree')),
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
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, to='multitenancy.Tenant', null=True)),
                ('tree_state', models.OneToOneField(related_name='tenantlink', to='decisiontree.TreeState')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
