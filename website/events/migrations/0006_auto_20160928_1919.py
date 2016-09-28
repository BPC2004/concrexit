# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-28 17:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20160914_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='booleanregistrationinformation',
            name='explanation_field',
            field=models.TextField(blank=True, null=True, verbose_name='explanation_field'),
        ),
        migrations.AddField(
            model_name='integerregistrationinformation',
            name='explanation_field',
            field=models.TextField(blank=True, null=True, verbose_name='explanation_field'),
        ),
        migrations.AddField(
            model_name='textregistrationinformation',
            name='explanation_field',
            field=models.TextField(blank=True, null=True, verbose_name='explanation_field'),
        ),
    ]
