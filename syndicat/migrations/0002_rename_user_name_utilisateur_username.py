# Generated by Django 4.0.6 on 2023-05-25 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('syndicat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='utilisateur',
            old_name='user_name',
            new_name='username',
        ),
    ]
