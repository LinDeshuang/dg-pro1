# Generated by Django 2.0.5 on 2018-06-01 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20180601_2035'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crcontent', models.TextField()),
                ('crstatus', models.BooleanField(default=False)),
                ('craddtime', models.DateTimeField(auto_now_add=True)),
                ('crauthor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_comment_replies', to='app.Guest')),
            ],
        ),
        migrations.RemoveField(
            model_name='comment',
            name='cguest',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='cisdelete',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='cobject',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='cpid',
        ),
        migrations.AddField(
            model_name='comment',
            name='cauthor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_comments', to='app.Guest'),
        ),
        migrations.AddField(
            model_name='comment',
            name='cbelong',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='art_comments', to='app.Publishment'),
        ),
        migrations.AddField(
            model_name='comment',
            name='cstatus',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='ccontent',
            field=models.TextField(),
        ),
        migrations.AddField(
            model_name='commentreply',
            name='crcomment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment_replies', to='app.Comment'),
        ),
        migrations.AddField(
            model_name='commentreply',
            name='crto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_replied', to='app.Guest'),
        ),
    ]