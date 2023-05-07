# Generated by Django 4.2.1 on 2023-05-07 21:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedulingApp', '0006_remove_ordonnance_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordonnance',
            name='Doctor',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_user', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
