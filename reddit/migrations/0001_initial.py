# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SubReddit'
        db.create_table('reddit_subreddit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('nsfw', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('reddit', ['SubReddit'])

        # Adding model 'Image'
        db.create_table('reddit_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subreddit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reddit.SubReddit'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('width', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('height', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('reddit', ['Image'])


    def backwards(self, orm):
        # Deleting model 'SubReddit'
        db.delete_table('reddit_subreddit')

        # Deleting model 'Image'
        db.delete_table('reddit_image')


    models = {
        'reddit.image': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'Image'},
            'height': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subreddit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reddit.SubReddit']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'reddit.subreddit': {
            'Meta': {'object_name': 'SubReddit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nsfw': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['reddit']