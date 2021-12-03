# Generated by Django 3.2.8 on 2021-12-03 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nombre', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opcionrespuesta',
            name='abierta',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='opcionrespuesta',
            name='opcion_multiple',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='opcionrespuesta',
            name='respuesta_correcta',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
