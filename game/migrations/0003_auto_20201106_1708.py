# Generated by Django 3.1 on 2020-11-06 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20201105_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
    ]
