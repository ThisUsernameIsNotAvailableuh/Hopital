from django.conf import settings
from django.db import models
from django.utils import timezone

class Patient(models.Model):
    Etat_de_sante_liste = [
        ('Bonne santé', 'Bonne santé'),
        ('Décédé', 'Décédé'),
        ('Hospitalisé', 'Hospitalisé'),
        ('En opération', 'En opération'),
        ('Repos', 'Repos'),
        ('En réanimation', 'En réanimation'),
    ]

    numero_de_sécurite_sociale = models.IntegerField(null=False, blank=False)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    date_arrivee = models.DateField(null=True, blank=True)
    etat_de_sante = models.CharField(
        max_length=50, choices=Etat_de_sante_liste, default='Bonne santé'
    )
    salle = models.ForeignKey('Salle', on_delete=models.SET_NULL, null=True, blank=True, related_name='patients')
    soigne = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nom} {self.prenom}, {self.numero_de_sécurite_sociale}"

class Medecin(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    salle = models.ForeignKey('Salle', on_delete=models.SET_NULL, null=True, blank=True, related_name='medecins')

    def __str__(self):
        return f"Dr. {self.nom} {self.prenom}"

class Salle(models.Model):
    nom = models.CharField(max_length=100)
    capacite = models.IntegerField(null=True, blank=True)
    
    def est_pleine(self):
        return self.patients.count() >= self.capacite if self.capacite else False

    def __str__(self):
        return self.nom
