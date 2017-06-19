# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-06-14 09:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MedApp', '0006_auto_20170613_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnostic',
            name='specilization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='diagnostic', to='MedApp.Specialization'),
        ),
        migrations.AddField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='sex',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 14, 12, 3, 4, 303000)),
        ),
    ]
