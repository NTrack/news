# Generated by Django 5.0 on 2024-02-01 11:04

import builtins
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_rename_myapp_articles_articles_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='type',
            field=models.CharField(default=builtins.dir, max_length=20),
            preserve_default=False,
        ),
    ]
