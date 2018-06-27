# Generated by Django 2.0.5 on 2018-05-31 09:53

from django.db import migrations, models
import django.db.models.manager
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20180531_1525'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='announcement',
            managers=[
                ('a_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='announcement',
            name='aisdelete',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='acontent',
            field=tinymce.models.HTMLField(),
        ),
    ]
