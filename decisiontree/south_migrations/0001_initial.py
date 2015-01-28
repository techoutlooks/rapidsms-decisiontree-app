# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Question'
        db.create_table('decisiontree_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('error_response', self.gf('django.db.models.fields.CharField')(max_length=160, blank=True)),
        ))
        db.send_create_signal('decisiontree', ['Question'])

        # Adding model 'Tree'
        db.create_table('decisiontree_tree', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trigger', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('root_state', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tree_set', to=orm['decisiontree.TreeState'])),
            ('completion_text', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=160, blank=True)),
        ))
        db.send_create_signal('decisiontree', ['Tree'])

        # Adding model 'Answer'
        db.create_table('decisiontree_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('decisiontree', ['Answer'])

        # Adding model 'TreeState'
        db.create_table('decisiontree_treestate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['decisiontree.Question'])),
            ('num_retries', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('decisiontree', ['TreeState'])

        # Adding model 'Transition'
        db.create_table('decisiontree_transition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('current_state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['decisiontree.TreeState'])),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transitions', to=orm['decisiontree.Answer'])),
            ('next_state', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='next_state', null=True, to=orm['decisiontree.TreeState'])),
        ))
        db.send_create_signal('decisiontree', ['Transition'])

        # Adding unique constraint on 'Transition', fields ['current_state', 'answer']
        db.create_unique('decisiontree_transition', ['current_state_id', 'answer_id'])

        # Adding M2M table for field tags on 'Transition'
        db.create_table('decisiontree_transition_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('transition', models.ForeignKey(orm['decisiontree.transition'], null=False)),
            ('tag', models.ForeignKey(orm['decisiontree.tag'], null=False))
        ))
        db.create_unique('decisiontree_transition_tags', ['transition_id', 'tag_id'])

        # Adding model 'Session'
        db.create_table('decisiontree_session', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('connection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rapidsms.Connection'])),
            ('tree', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sessions', to=orm['decisiontree.Tree'])),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['decisiontree.TreeState'], null=True, blank=True)),
            ('num_tries', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('canceled', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('decisiontree', ['Session'])

        # Adding model 'Entry'
        db.create_table('decisiontree_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entries', to=orm['decisiontree.Session'])),
            ('sequence_id', self.gf('django.db.models.fields.IntegerField')()),
            ('transition', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entries', to=orm['decisiontree.Transition'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=160)),
        ))
        db.send_create_signal('decisiontree', ['Entry'])

        # Adding M2M table for field tags on 'Entry'
        db.create_table('decisiontree_entry_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entry', models.ForeignKey(orm['decisiontree.entry'], null=False)),
            ('tag', models.ForeignKey(orm['decisiontree.tag'], null=False))
        ))
        db.create_unique('decisiontree_entry_tags', ['entry_id', 'tag_id'])

        # Adding model 'Tag'
        db.create_table('decisiontree_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('decisiontree', ['Tag'])

        # Adding M2M table for field recipients on 'Tag'
        db.create_table('decisiontree_tag_recipients', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tag', models.ForeignKey(orm['decisiontree.tag'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('decisiontree_tag_recipients', ['tag_id', 'user_id'])

        # Adding model 'TagNotification'
        db.create_table('decisiontree_tagnotification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['decisiontree.Tag'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['decisiontree.Entry'])),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_sent', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('decisiontree', ['TagNotification'])

        # Adding unique constraint on 'TagNotification', fields ['tag', 'user', 'entry']
        db.create_unique('decisiontree_tagnotification', ['tag_id', 'user_id', 'entry_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'TagNotification', fields ['tag', 'user', 'entry']
        db.delete_unique('decisiontree_tagnotification', ['tag_id', 'user_id', 'entry_id'])

        # Removing unique constraint on 'Transition', fields ['current_state', 'answer']
        db.delete_unique('decisiontree_transition', ['current_state_id', 'answer_id'])

        # Deleting model 'Question'
        db.delete_table('decisiontree_question')

        # Deleting model 'Tree'
        db.delete_table('decisiontree_tree')

        # Deleting model 'Answer'
        db.delete_table('decisiontree_answer')

        # Deleting model 'TreeState'
        db.delete_table('decisiontree_treestate')

        # Deleting model 'Transition'
        db.delete_table('decisiontree_transition')

        # Removing M2M table for field tags on 'Transition'
        db.delete_table('decisiontree_transition_tags')

        # Deleting model 'Session'
        db.delete_table('decisiontree_session')

        # Deleting model 'Entry'
        db.delete_table('decisiontree_entry')

        # Removing M2M table for field tags on 'Entry'
        db.delete_table('decisiontree_entry_tags')

        # Deleting model 'Tag'
        db.delete_table('decisiontree_tag')

        # Removing M2M table for field recipients on 'Tag'
        db.delete_table('decisiontree_tag_recipients')

        # Deleting model 'TagNotification'
        db.delete_table('decisiontree_tagnotification')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'decisiontree.answer': {
            'Meta': {'object_name': 'Answer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'decisiontree.entry': {
            'Meta': {'ordering': "('sequence_id',)", 'object_name': 'Entry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sequence_id': ('django.db.models.fields.IntegerField', [], {}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': "orm['decisiontree.Session']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'entries'", 'symmetrical': 'False', 'to': "orm['decisiontree.Tag']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'transition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': "orm['decisiontree.Transition']"})
        },
        'decisiontree.question': {
            'Meta': {'object_name': 'Question'},
            'error_response': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '160'})
        },
        'decisiontree.session': {
            'Meta': {'object_name': 'Session'},
            'canceled': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'connection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms.Connection']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_tries': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['decisiontree.TreeState']", 'null': 'True', 'blank': 'True'}),
            'tree': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessions'", 'to': "orm['decisiontree.Tree']"})
        },
        'decisiontree.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'recipients': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tags'", 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'decisiontree.tagnotification': {
            'Meta': {'unique_together': "(('tag', 'user', 'entry'),)", 'object_name': 'TagNotification'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {}),
            'date_sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['decisiontree.Entry']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['decisiontree.Tag']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'decisiontree.transition': {
            'Meta': {'unique_together': "(('current_state', 'answer'),)", 'object_name': 'Transition'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transitions'", 'to': "orm['decisiontree.Answer']"}),
            'current_state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['decisiontree.TreeState']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next_state': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'next_state'", 'null': 'True', 'to': "orm['decisiontree.TreeState']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'transitions'", 'blank': 'True', 'to': "orm['decisiontree.Tag']"})
        },
        'decisiontree.tree': {
            'Meta': {'object_name': 'Tree'},
            'completion_text': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'root_state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tree_set'", 'to': "orm['decisiontree.TreeState']"}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'}),
            'trigger': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'decisiontree.treestate': {
            'Meta': {'object_name': 'TreeState'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'num_retries': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['decisiontree.Question']"})
        },
        'rapidsms.backend': {
            'Meta': {'object_name': 'Backend'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'rapidsms.connection': {
            'Meta': {'unique_together': "(('backend', 'identity'),)", 'object_name': 'Connection'},
            'backend': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms.Backend']"}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rapidsms.Contact']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'rapidsms.contact': {
            'Meta': {'object_name': 'Contact'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'pin': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'primary_backend': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'contact_primary'", 'null': 'True', 'to': "orm['rapidsms.Backend']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        }
    }

    complete_apps = ['decisiontree']
