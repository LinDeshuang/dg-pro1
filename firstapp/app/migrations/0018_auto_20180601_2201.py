# Generated by Django 2.0.5 on 2018-06-01 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20180601_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='cstatus',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='commentreply',
            name='crstatus',
            field=models.BooleanField(default=True),
        ),
    ]
