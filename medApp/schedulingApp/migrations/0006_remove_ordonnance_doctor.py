# Generated by Django 4.2.1 on 2023-05-07 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedulingApp', '0005_ordonnance_doctor_alter_ligneordonnance_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordonnance',
            name='Doctor',
        ),
    ]
