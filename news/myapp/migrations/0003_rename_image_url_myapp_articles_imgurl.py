# Generated by Django 5.0 on 2024-02-01 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_rename_userid_myapp_users_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myapp_articles',
            old_name='image_url',
            new_name='imgurl',
        ),
    ]
