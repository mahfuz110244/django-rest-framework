# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-11 14:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0002_attendee'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='attribute_key',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='attendee',
            name='attribute_value',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='contact_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contacts1', to='snippets.Contact'),
        ),
        migrations.AlterUniqueTogether(
            name='attendee',
            unique_together=set([('contact_id', 'attribute_key')]),
        ),
    ]
