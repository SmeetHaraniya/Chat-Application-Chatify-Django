# Generated by Django 5.0.2 on 2024-03-05 04:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatifyApp', '0003_userinfo_theme_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserInfo',
        ),
    ]
