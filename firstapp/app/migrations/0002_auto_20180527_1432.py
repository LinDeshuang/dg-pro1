# Generated by Django 2.0.5 on 2018-05-27 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guest',
            name='ggname',
        ),
        migrations.AddField(
            model_name='guest',
            name='gname',
            field=models.CharField(default=None, max_length=20),
            preserve_default=False,
        ),
    ]