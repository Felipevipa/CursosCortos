# Generated by Django 3.2.8 on 2021-12-10 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nombre', '0005_remove_opcionrespuestacerrada_abierta'),
    ]

    operations = [
        migrations.AddField(
            model_name='tematica',
            name='color1',
            field=models.CharField(default='#F4F4F4', max_length=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tematica',
            name='color2',
            field=models.CharField(default='F4F4F6', max_length=9),
            preserve_default=False,
        ),
    ]
