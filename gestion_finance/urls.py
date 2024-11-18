# gestion_finance/urls.py

from django.urls import path
from . import views


app_name = 'gestion_finance'

urlpatterns = [
    path('paiements/list', views.PaiementListView.as_view(), name='paiement-list'),
    path('paiements/create/', views.PaiementCreateView.as_view(), name='paiement-create'),
    path('paiements/<uuid:pk>/', views.PaiementDetailView.as_view(), name='paiement-detail'),
    path('paiements/<uuid:pk>/update/', views.PaiementUpdateView.as_view(), name='paiement-update'),
    path('paiements/<uuid:pk>/delete/', views.PaiementDeleteView.as_view(), name='paiement-delete'),
    
    #path('Paiement/<uuid:pk>/<str:action>/', views.valider_ou_rejeter_Paiement, name='valider_ou_rejeter_Paiement'),
    path('paiement/dossier/list', views.DossierValideListView.as_view(), name='dossier-list'),
    path('paiements/create/<uuid:pk>', views.DossierPaiementCreateView.as_view(), name='dossier-paiement'),
]
