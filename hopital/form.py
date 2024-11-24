from django import forms
from .models import Patient, Medecin, Salle

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['numero_de_sécurite_sociale', 'nom', 'prenom', 'date_naissance', 'etat_de_sante', 'salle']


class MedecinForm(forms.ModelForm):
    class Meta:
        model = Medecin
        fields = ['nom', 'prenom', 'date_naissance', 'salle']


class SalleForm(forms.ModelForm):
    class Meta:
        model = Salle
        fields = ['nom', 'capacite']