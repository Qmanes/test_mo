# Generated by Django 3.1.5 on 2021-01-24 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemons', '0003_auto_20210124_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='specie',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='pokemons.specie'),
        ),
    ]
