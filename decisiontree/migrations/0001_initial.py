# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('rapidsms', '0002_delete_backendmessage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('type', models.CharField(max_length=1, choices=[(b'A', b'Exact Match'), (b'R', b'Regular Expression'), (b'C', b'Custom Logic')])),
                ('answer', models.CharField(max_length=160)),
                ('description', models.CharField(max_length=100, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sequence_id', models.IntegerField()),
                ('time', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('text', models.CharField(max_length=160)),
            ],
            options={
                'ordering': ('sequence_id',),
                'verbose_name_plural': 'Entries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(help_text=b'The text to send to the user.', max_length=160, verbose_name=b'message text')),
                ('error_response', models.CharField(help_text=b'Optional error message to send if the question is not answered properly.', max_length=160, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('num_tries', models.PositiveIntegerField(help_text=b'The number of times the user has tried to answer the current question.')),
                ('canceled', models.NullBooleanField()),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('connection', models.ForeignKey(to='rapidsms.Connection')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('recipients', models.ManyToManyField(related_name='tags', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sent', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField()),
                ('date_sent', models.DateTimeField(null=True, blank=True)),
                ('entry', models.ForeignKey(to='decisiontree.Entry')),
                ('tag', models.ForeignKey(to='decisiontree.Tag')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.ForeignKey(related_name='transitions', to='decisiontree.Answer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tree',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('trigger', models.CharField(help_text=b'The incoming message which triggers this Tree.', unique=True, max_length=30)),
                ('completion_text', models.CharField(help_text=b'The message that will be sent when the tree is completed', max_length=160, null=True, blank=True)),
                ('summary', models.CharField(max_length=160, blank=True)),
            ],
            options={
                'permissions': [('can_view', 'Can view tree data')],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TreeState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('num_retries', models.PositiveIntegerField(help_text=b"The number of tries the user has to get out of this state. If empty, there is no limit. When the number of retries is hit, the user's session will be terminated.", null=True, blank=True)),
                ('question', models.ForeignKey(to='decisiontree.Question')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tree',
            name='root_state',
            field=models.ForeignKey(related_name='tree_set', to='decisiontree.TreeState', help_text=b'The first Question sent when this Tree is triggered, which may lead to many more.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transition',
            name='current_state',
            field=models.ForeignKey(to='decisiontree.TreeState'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transition',
            name='next_state',
            field=models.ForeignKey(related_name='next_state', blank=True, to='decisiontree.TreeState', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transition',
            name='tags',
            field=models.ManyToManyField(related_name='transitions', to='decisiontree.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='transition',
            unique_together=set([('current_state', 'answer')]),
        ),
        migrations.AlterUniqueTogether(
            name='tagnotification',
            unique_together=set([('tag', 'user', 'entry')]),
        ),
        migrations.AddField(
            model_name='session',
            name='state',
            field=models.ForeignKey(blank=True, to='decisiontree.TreeState', help_text=b'None if the session is complete.', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='session',
            name='tree',
            field=models.ForeignKey(related_name='sessions', to='decisiontree.Tree'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entry',
            name='session',
            field=models.ForeignKey(related_name='entries', to='decisiontree.Session'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entry',
            name='tags',
            field=models.ManyToManyField(related_name='entries', to='decisiontree.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entry',
            name='transition',
            field=models.ForeignKey(related_name='entries', to='decisiontree.Transition'),
            preserve_default=True,
        ),
    ]
