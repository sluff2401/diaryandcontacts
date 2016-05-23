# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('diaryandcontacts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Circle',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('full_name', models.CharField(max_length=40)),
            ],
        ),
        migrations.RemoveField(
            model_name='job',
            name='employer',
        ),
        migrations.RemoveField(
            model_name='event',
            name='employers',
        ),
        migrations.RemoveField(
            model_name='person',
            name='employer',
        ),
        migrations.AddField(
            model_name='person',
            name='phone_c',
            field=models.CharField(null=True, max_length=15, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='event',
            name='is_live',
            field=models.NullBooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='reference',
            field=models.CharField(max_length=200, blank=True, default=''),
        ),
        migrations.DeleteModel(
            name='Employer',
        ),
        migrations.DeleteModel(
            name='Job',
        ),
        migrations.AddField(
            model_name='person',
            name='circles',
            field=models.ManyToManyField(null=True, blank=True, to='diaryandcontacts.Circle'),
        ),
    ]
