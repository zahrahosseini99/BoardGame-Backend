# Generated by Django 3.1.2 on 2020-11-27 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe',
            name='close_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cafe',
            name='open_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
