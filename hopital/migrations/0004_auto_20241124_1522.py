# Generated by Django 2.2.28 on 2024-11-24 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hopital', '0003_patient_soigne'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medecin',
            old_name='emplacement',
            new_name='salle',
        ),
        migrations.RenameField(
            model_name='patient',
            old_name='emplacement',
            new_name='salle',
        ),
    ]
