# Generated by Django 3.2.8 on 2021-11-25 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nombre', '0004_docenteprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tematica',
            name='titulo',
            field=models.CharField(max_length=80),
        ),
    ]
