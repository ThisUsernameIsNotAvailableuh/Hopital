from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('statistiques/', views.statistiques, name='statistiques'),
    path('nouveau_patient/', views.nouveau_patient, name='nouveau_patient'),
    path('nouveau_medecin/', views.nouveau_medecin, name='nouveau_medecin'),
    path('salles/', views.liste_salles, name='liste_salles'),
    path('salles/<int:salle_id>/', views.detail_salle, name='detail_salle'),
    path('salles/supprimer/<int:salle_id>/', views.supprimer_salle, name='supprimer_salle'),
    path('salles/<int:salle_id>/gerer/', views.gerer_occupants, name='gerer_occupants'),
]