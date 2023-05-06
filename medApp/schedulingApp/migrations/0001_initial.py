# Generated by Django 4.2.1 on 2023-05-06 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PendingDoctors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, verbose_name='username')),
                ('First_name', models.CharField(max_length=50, verbose_name='First_name')),
                ('Last_name', models.CharField(max_length=50, verbose_name='Last_name')),
                ('Email', models.EmailField(max_length=254, verbose_name='email')),
                ('Specialty', models.CharField(max_length=50, verbose_name='Last_name')),
                ('phoneNumber', models.CharField(max_length=8, verbose_name='phone number')),
            ],
        ),
    ]