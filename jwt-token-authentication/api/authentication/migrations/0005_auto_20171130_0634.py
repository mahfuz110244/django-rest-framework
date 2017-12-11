# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-30 06:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20171130_0630'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('date_of_birth', models.CharField(blank=True, max_length=10)),
                ('estimated_age', models.CharField(blank=True, max_length=50)),
                ('gender', models.CharField(blank=True, max_length=50)),
                ('status', models.BooleanField(default=False)),
                ('revera_id', models.CharField(blank=True, max_length=50)),
                ('nationality', models.CharField(blank=True, max_length=50)),
                ('national_id', models.CharField(blank=True, max_length=50)),
                ('medical_insurance_id', models.CharField(blank=True, max_length=50)),
                ('ethnicity', models.CharField(blank=True, max_length=50)),
                ('religion', models.CharField(blank=True, max_length=20)),
                ('merital_status', models.CharField(blank=True, max_length=20)),
                ('blood_group', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=50, unique=True)),
                ('username', models.CharField(blank=True, max_length=50, unique=True)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('height', models.CharField(blank=True, max_length=20)),
                ('weight', models.CharField(blank=True, max_length=20)),
                ('alergies', models.TextField(blank=True, max_length=500)),
                ('profile_photo', models.ImageField(blank=True, max_length=254, upload_to='images')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ContactsAttributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute_key', models.CharField(blank=True, max_length=50)),
                ('attribute_value', models.TextField(blank=True, max_length=500)),
                ('contact_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.Contacts')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='security_answer',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='user',
            name='security_question',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='terms_and_condition_accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='contact_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.Contacts'),
        ),
    ]
