# Generated by Django 4.2 on 2024-04-08 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rockclimb_app', '0004_vote_grade_vote_rockvideo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='rockVideo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='unquie_votes', to='rockclimb_app.rockvideo'),
        ),
    ]
