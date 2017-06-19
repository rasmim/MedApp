# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-06-09 12:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MedApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consultation', to=settings.AUTH_USER_MODEL),
        ),
    ]