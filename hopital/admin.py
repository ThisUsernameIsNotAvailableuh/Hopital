from django.contrib import admin

from .models import Patient, Medecin, Salle
 
admin.site.register(Patient)
admin.site.register(Medecin)
admin.site.register(Salle)
