# Generated by Django 3.1.5 on 2021-01-24 21:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemons', '0009_auto_20210124_2055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evolutionchain',
            name='id',
        ),
        migrations.AlterField(
            model_name='evolutionchain',
            name='specie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pokemons.specie'),
        ),
    ]
