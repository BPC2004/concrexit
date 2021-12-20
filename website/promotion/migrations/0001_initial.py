# Generated by Django 3.2.10 on 2021-12-17 10:58

import datetime
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0051_event_caption'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromotionChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Channel name')),
            ],
        ),
        migrations.CreateModel(
            name='PromotionRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('publish_date', models.DateField(default=datetime.date.today, verbose_name='Publish date')),
                ('assigned_to', models.CharField(blank=True, max_length=50, null=True, verbose_name='Assigned to')),
                ('status', models.CharField(choices=[('not_started', 'Not started'), ('started', 'Started'), ('finished', 'Finished'), ('published', 'Published')], default='not_started', max_length=40, verbose_name='status')),
                ('drive_folder', models.URLField(blank=True, max_length=2000, null=True, verbose_name='drive folder')),
                ('remarks', tinymce.models.HTMLField(blank=True, null=True, verbose_name='remarks')),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='promotion.promotionchannel', verbose_name='channel')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.event', verbose_name='event')),
            ],
            options={
                'verbose_name': 'Promotion request',
                'verbose_name_plural': 'Promotion requests',
            },
        ),
    ]
