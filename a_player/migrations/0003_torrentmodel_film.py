# Generated by Django 2.0.7 on 2018-10-17 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('a_player', '0002_remove_torrentmodel_film'),
    ]

    operations = [
        migrations.AddField(
            model_name='torrentmodel',
            name='film',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='a_player.FilmModel'),
            preserve_default=False,
        ),
    ]