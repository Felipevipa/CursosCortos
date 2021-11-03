# Generated by Django 3.2.8 on 2021-10-29 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nombre', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tematica',
            name='docente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='nombre.docente'),
        ),
        migrations.AlterField(
            model_name='tematica',
            name='materia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='nombre.materia'),
        ),
    ]
