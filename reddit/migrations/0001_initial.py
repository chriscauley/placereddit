# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('width', models.IntegerField(default=0)),
                ('height', models.IntegerField(default=0)),
                ('y_crop_order', models.CharField(max_length=1024, null=True, blank=True)),
                ('x_crop_order', models.CharField(max_length=1024, null=True, blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-date_added',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('nsfw', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubReddit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', models.CharField(unique=True, max_length=255)),
                ('nsfw', models.BooleanField(default=False)),
                ('featured', models.BooleanField(default=False)),
                ('last_featured', models.DateField(default=datetime.date.today)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='subject',
            name='subreddits',
            field=models.ManyToManyField(to='reddit.SubReddit', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='image',
            name='subreddit',
            field=models.ForeignKey(to='reddit.SubReddit'),
            preserve_default=True,
        ),
    ]
