# Generated by Django 2.0.7 on 2018-10-09 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='FilmModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=30)),
                ('imdb_id', models.DecimalField(decimal_places=0, max_digits=10)),
            ],
        ),
        migrations.AddField(
            model_name='commentmodel',
            name='film',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a_player.FilmModel'),
        ),
        migrations.AddField(
            model_name='commentmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
