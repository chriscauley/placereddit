# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Image.y_crop_order'
        db.alter_column('reddit_image', 'y_crop_order', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True))

        # Changing field 'Image.x_crop_order'
        db.alter_column('reddit_image', 'x_crop_order', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True))

    def backwards(self, orm):

        # Changing field 'Image.y_crop_order'
        db.alter_column('reddit_image', 'y_crop_order', self.gf('django.db.models.fields.CharField')(max_length=256, null=True))

        # Changing field 'Image.x_crop_order'
        db.alter_column('reddit_image', 'x_crop_order', self.gf('django.db.models.fields.CharField')(max_length=256, null=True))

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
        'reddit.subreddit': {
            'Meta': {'object_name': 'SubReddit'},
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'nsfw': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['reddit']