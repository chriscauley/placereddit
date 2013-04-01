# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Subject'
        db.create_table('reddit_subject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('nsfw', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('reddit', ['Subject'])

        # Adding M2M table for field subreddits on 'Subject'
        db.create_table('reddit_subject_subreddits', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('subject', models.ForeignKey(orm['reddit.subject'], null=False)),
            ('subreddit', models.ForeignKey(orm['reddit.subreddit'], null=False))
        ))
        db.create_unique('reddit_subject_subreddits', ['subject_id', 'subreddit_id'])


    def backwards(self, orm):
        # Deleting model 'Subject'
        db.delete_table('reddit_subject')

        # Removing M2M table for field subreddits on 'Subject'
        db.delete_table('reddit_subject_subreddits')


    models = {
        'reddit.image': {
            'Meta': {'ordering': "('-date_added',)", 'object_name': 'Image'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subreddit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reddit.SubReddit']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'x_crop_order': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'y_crop_order': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'})
        },
        'reddit.subject': {
            'Meta': {'object_name': 'Subject'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nsfw': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subreddits': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reddit.SubReddit']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'reddit.subreddit': {
            'Meta': {'object_name': 'SubReddit'},
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_featured': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'nsfw': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['reddit']