# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'SubReddit', fields ['slug']
        db.create_unique('reddit_subreddit', ['slug'])

        # Adding unique constraint on 'SubReddit', fields ['name']
        db.create_unique('reddit_subreddit', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'SubReddit', fields ['name']
        db.delete_unique('reddit_subreddit', ['name'])

        # Removing unique constraint on 'SubReddit', fields ['slug']
        db.delete_unique('reddit_subreddit', ['slug'])


    models = {
        'reddit.image': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'Image'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subreddit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reddit.SubReddit']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'reddit.subreddit': {
            'Meta': {'object_name': 'SubReddit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'nsfw': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['reddit']