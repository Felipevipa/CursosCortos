# Generated by Django 3.2.8 on 2021-10-21 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nombre', '0006_auto_20211021_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='materialExterno',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='material',
            name='video',
            field=models.URLField(null=True),
        ),
    ]
