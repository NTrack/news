# Generated by Django 5.0 on 2024-02-12 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_remove_users_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='session_key',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
