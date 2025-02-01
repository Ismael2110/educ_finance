from django.urls import path
from . import views
from gestion_administratif.views import HistoriqueDossier
from .views import StatistiquesView

app_name = "gestion_administratif"

urlpatterns = [
    path('dossiers/', views.DossierListView.as_view(), name='dossier-list'),
    path('dossiers/create/', views.DossierCreateView.as_view(), name='dossier-create'),
    path('dossiers/<uuid:pk>/', views.DossierDetailView.as_view(), name='dossier-detail'),
    path('dossiers/<uuid:pk>/update/', views.DossierUpdateView.as_view(), name='dossier-update'),
    path('dossiers/<uuid:pk>/delete/', views.DossierDeleteView.as_view(), name='dossier-delete'),
    path('dossier/<uuid:pk>/<str:action>/', views.valider_ou_rejeter_dossier, name='valider_ou_rejeter_dossier'),
    path('transfert/<uuid:pk>/', views.Transfert.as_view(), name='transfert-dossier'),
    path('dossiers-transferes/', HistoriqueDossier.as_view(), name='historique-dossier'),
    
    

    path('statistiques/', StatistiquesView.as_view(), name='statistiques')
    
]

# urls.py
