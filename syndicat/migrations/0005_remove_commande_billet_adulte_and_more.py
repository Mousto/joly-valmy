# Generated by Django 4.0.6 on 2023-02-27 15:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('syndicat', '0004_alter_produit_disponible'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commande',
            name='billet_adulte',
        ),
        migrations.RemoveField(
            model_name='commande',
            name='billet_enfant',
        ),
        migrations.AddField(
            model_name='produit',
            name='billet_adulte',
            field=models.PositiveIntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='produit',
            name='billet_enfant',
            field=models.PositiveIntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
