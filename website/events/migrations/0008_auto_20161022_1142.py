# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-22 09:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20161009_2352'),
    ]

    operations = [
        migrations.RenameField('registrationinformationfield',
                               'description', 'description_nl'),
        migrations.RenameField('registrationinformationfield',
                               'name', 'name_nl'),
        migrations.AddField(
            model_name='registrationinformationfield',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='description (EN)'),
        ),
        migrations.AlterField(
            model_name='registrationinformationfield',
            name='description_nl',
            field=models.TextField(blank=True, null=True, verbose_name='description (NL)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='registrationinformationfield',
            name='name_en',
            field=models.CharField(default='', max_length=100,
                                   verbose_name='field name (EN)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='registrationinformationfield',
            name='name_nl',
            field=models.CharField(max_length=100,
                                   verbose_name='field name (NL)'),
            preserve_default=True,
        ),
    ]
