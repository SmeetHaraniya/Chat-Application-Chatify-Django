# Generated by Django 5.0.2 on 2024-03-05 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chatifyApp', '0005_delete_themes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Themes',
            fields=[
                ('theme_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('theme_name', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
            ],
        ),
    ]
