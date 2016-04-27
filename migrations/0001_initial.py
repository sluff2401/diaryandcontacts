# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('full_name', models.CharField(max_length=40)),
                ('name_in_meetup', models.CharField(max_length=40, null=True, blank=True)),
                ('name_in_twitter', models.CharField(max_length=40, null=True, blank=True)),
                ('email', models.CharField(max_length=20, null=True, blank=True)),
                ('phone_a', models.CharField(max_length=15, null=True, blank=True)),
                ('phone_b', models.CharField(max_length=15, null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('event_date', models.DateField(null=True, blank=True)),
                ('reference', models.CharField(max_length=200, null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(null=True, blank=True)),
                ('is_live', models.BooleanField(default=True)),
                ('employers', models.ManyToManyField(to='diaryandcontacts.Employer', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('job_reference', models.CharField(max_length=30, null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(null=True, blank=True)),
                ('employer', models.ForeignKey(to='diaryandcontacts.Employer')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('full_name', models.CharField(max_length=40)),
                ('second_name', models.CharField(max_length=20)),
                ('name_in_meetup', models.CharField(max_length=40, null=True, blank=True)),
                ('name_in_twitter', models.CharField(max_length=40, null=True, blank=True)),
                ('email', models.CharField(max_length=40, null=True, blank=True)),
                ('phone_a', models.CharField(max_length=15, null=True, blank=True)),
                ('phone_b', models.CharField(max_length=15, null=True, blank=True)),
                ('hcp', models.BooleanField(default=False)),
                ('plus', models.BooleanField(default=False)),
                ('esg', models.BooleanField(default=False)),
                ('wltmf', models.BooleanField(default=False)),
                ('it', models.BooleanField(default=False)),
                ('notes', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(null=True, blank=True)),
                ('employer', models.ForeignKey(blank=True, null=True, to='diaryandcontacts.Employer')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='persons',
            field=models.ManyToManyField(to='diaryandcontacts.Person', blank=True),
        ),
    ]
