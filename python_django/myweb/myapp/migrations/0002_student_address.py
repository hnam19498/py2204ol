# Generated by Django 4.0.6 on 2022-07-23 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='address',
            field=models.TextField(default='Nam Định'),
        ),
    ]
