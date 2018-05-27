# Generated by Django 2.0.3 on 2018-05-27 06:48

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0006_auto_20171207_0224'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='report',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created_at'], name='report_repo_created_edcdde_brin', pages_per_range=16),
        ),
    ]
