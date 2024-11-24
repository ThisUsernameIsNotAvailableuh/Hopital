# Generated by Django 2.2.28 on 2024-11-24 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hopital', '0004_auto_20241124_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medecin',
            name='salle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='medecins', to='hopital.Salle'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='salle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patients', to='hopital.Salle'),
        ),
    ]