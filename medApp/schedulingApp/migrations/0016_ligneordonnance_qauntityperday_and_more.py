# Generated by Django 4.2.1 on 2023-05-28 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedulingApp', '0015_ordonnance_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='ligneordonnance',
            name='qauntityPerDay',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ligneordonnance',
            name='remarks',
            field=models.CharField(default='no remarks', max_length=1255),
            preserve_default=False,
        ),
    ]
