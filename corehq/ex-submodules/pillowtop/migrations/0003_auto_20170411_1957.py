# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-11 19:57
from __future__ import unicode_literals

from __future__ import absolute_import
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pillowtop', '0002_djangopillowcheckpoint_sequence_format'),
    ]
    operations = [
        migrations.CreateModel(
            name='KafkaCheckpoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkpoint_id', models.CharField(db_index=True, max_length=126)),
                ('topic', models.CharField(max_length=126)),
                ('partition', models.IntegerField()),
                ('offset', models.IntegerField()),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='kafkacheckpoint',
            unique_together=set([('checkpoint_id', 'topic', 'partition')]),
        ),
    ]
