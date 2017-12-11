# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-30 06:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20171129_0923'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='created_at',
            new_name='created_date',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='updated_at',
            new_name='updated_date',
        ),
        migrations.AddField(
            model_name='user',
            name='created_uid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user5', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='updated_uid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user6', to=settings.AUTH_USER_MODEL),
        ),
    ]
