from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient, Medecin, Salle
from django.http import HttpResponseRedirect
from .form import *
from django.contrib import messages

def index(request):
    return render(request, 'hopital/index.html', {})

def statistiques(request):
    nombre_morts=len(Patient.objects.filter(etat_de_sante="Décédé"))
    nombre_sauve=len(Patient.objects.filter(soigne=True))
    nombre_patients=len(Patient.objects.all())-len(Patient.objects.filter(etat_de_sante='Décédé'))
    nombre_medecins=len(Medecin.objects.all())
    nombre_salles=len(Salle.objects.filter())
    return render(request, 'hopital/statistiques.html', {"nombre_morts":nombre_morts, "nombre_sauve":nombre_sauve, "nombre_patients":nombre_patients, "nombre_salles":nombre_salles, 'nombre_medecins':nombre_medecins})

def nouveau_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            salle = form.cleaned_data['salle']
            if salle and salle.est_pleine():
                messages.error(request, f"La salle '{salle.nom}' a atteint sa capacité maximale.")
            else:
                form.save()
                messages.success(request, "Patient créé avec succès.")
                return redirect('liste_salles')
    else:
        form = PatientForm()
    return render(request, 'hopital/nouveau_patient.html', {'form': form})

def nouveau_medecin(request):
    if request.method == 'POST':
        form = MedecinForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_salles')
    else:
        form = MedecinForm()
    return render(request, 'hopital/nouveau_medecin.html', {'form': form})

def liste_salles(request):
    salles = Salle.objects.all()
    form = SalleForm()
    if request.method == 'POST':
        form = SalleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Salle créée avec succès.")
            return redirect('liste_salles')
    return render(request, 'hopital/liste_salles.html', {'salles': salles, 'form': form})

def supprimer_salle(request, salle_id):
    salle = get_object_or_404(Salle, id=salle_id)
    if salle.patients.exists() or salle.medecins.exists():  # Utilise related_name pour vérifier les occupants
        messages.error(request, "Impossible de supprimer une salle occupée par des patients ou des médecins.")
    else:
        salle.delete()
        messages.success(request, "Salle supprimée avec succès.")
    return redirect('liste_salles')

def detail_salle(request, salle_id):
    salle = Salle.objects.get(id=salle_id)
    patients = salle.patients.all()
    medecins = salle.medecins.all()

    if request.method == 'POST':
        for patient in patients:
            patient.soigne = 'soigne' in request.POST.getlist(f'patient-{patient.id}')
            patient.save()
        for medecin in medecins:
            # Ajoutez une logique si nécessaire
            pass
        return HttpResponseRedirect(request.path)

    return render(request, 'hopital/detail_salle.html', {'salle': salle, 'patients': patients, 'medecins': medecins})

def gerer_occupants(request, salle_id):
    salle = get_object_or_404(Salle, id=salle_id)
    patients = salle.patients.all()
    medecins = salle.medecins.all()
    salles_disponibles = Salle.objects.exclude(id=salle_id)

    if request.method == 'POST':
        for patient in patients:
            nouvelle_salle_id = request.POST.get(f'salle_patient_{patient.id}')
            if nouvelle_salle_id:
                nouvelle_salle = get_object_or_404(Salle, id=nouvelle_salle_id)
                if nouvelle_salle.est_pleine():
                    messages.error(
                        request,
                        f"Impossible de déplacer {patient.nom} vers la salle '{nouvelle_salle.nom}', capacité maximale atteinte."
                    )
                else:
                    patient.salle = nouvelle_salle
                    patient.save()
        for patient in patients:
            nouveau_etat = request.POST.get(f'etat_patient_{patient.id}')
            if nouveau_etat:
                patient.etat_de_sante = nouveau_etat
                patient.save()
        
        supprimer_patient = request.POST.getlist('supprimer_patient')
        supprimer_medecin = request.POST.getlist('supprimer_medecin')
        Patient.objects.filter(id__in=supprimer_patient).delete()
        Medecin.objects.filter(id__in=supprimer_medecin).delete()

        messages.success(request, "Formulaire envoyé")
        return redirect('gerer_occupants', salle_id=salle_id)

    return render(request, 'hopital/gerer_occupants.html', {
        'salle': salle,
        'patients': patients,
        'medecins': medecins,
        'salles_disponibles': salles_disponibles,
    })

from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient
from django.contrib import messages

def supprimer_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    # Vérifiez si vous souhaitez afficher un message d'erreur si le patient est lié à une salle
    if patient.salle:
        messages.error(request, "Impossible de supprimer un patient qui est encore dans une salle.")
    else:
        patient.delete()
        messages.success(request, "Patient supprimé avec succès.")

    return redirect('liste_salles')  # Ou toute autre redirection souhaitée
