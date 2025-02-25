from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from educ_finance.views import (
    CustomCreateView,
    CustomDeleteView,
    CustomDetailView,
    CustomListView,
    CustomUpdateView,
)

from parameter.models import  UFR, Departement, Filiere, Module, Enseignant, TypePaiement
from parameter.forms import UfrForm, DepartementForm, FiliereForm, ModuleForm, EnseignantForm, TypePaiementForm

# Create your views here.
#finis

class UfrListView(CustomListView):
    model = UFR
    name = "ufr"
    template_name = "list_ufr.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_delete"] = True
        context["can_add"] = True
        context["add_url"] = reverse_lazy("parameter:ufr-create") 
        context["list_of"] = 'Liste des UFR'
        # context["ufr_sigles"] = UFR.objects.values_list("sigle", flat=True)  # Liste des sigles
        return context


class UfrCreateView(CustomCreateView):
    model = UFR
    form_class = UfrForm
    name = "ufr"
    success_url = reverse_lazy("parameter:ufr-list")


class UfrUpdateView(CustomUpdateView):
    model = UFR
    name = "ufr"
    template_name = "ufr_form.html"
    form_class = UfrForm
    success_url = reverse_lazy("parameter:ufr-list")


class UfrDetailView(CustomDetailView):
    model = UFR
    name = "ufr"
    template_name = "detail-ufr.html"
    success_url = reverse_lazy("parameter:ufr-list")
    
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Détails de l'UFR"
        context["update_url"] = "parameter:ufr-update"
        context["delete_url"] = "parameter:ufr-delete"
        context["list_url"] = "parameter:ufr-list"
        context["ufr_sigle"] = self.object.sigle  # Ajout du sigle dans le contexte
        context["list_of"] = 'Détails des UFR'
        return context


class UfrDeleteView(CustomDeleteView):
    model = UFR
    name = "ufr"
    template_name ="delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_object()  # Utilisation de self.get_object()
        context["card_title"] = f"Suppression de l'UFR {object.label} - {object.sigle}"  # Affichage du sigle
        context["list_url"] = reverse_lazy("parameter:ufr-list")  # URL du retour
        context["list_of"] = "Suppression d'un UFR"
        return context


    
    #finis

class DepartementListView(CustomListView):
    model = Departement
    name = "departement"
    template_name = "list-depart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_delete"] = True

        return context


class DepartementCreateView(CustomCreateView):
    model = Departement
    form_class = DepartementForm
    name = "Departement"
    success_url = reverse_lazy("parameter:departement-list")


class DepartementUpdateView(CustomUpdateView):
    model = Departement
    name = "Departement"
    template_name = "ufr_form.html"
    form_class = DepartementForm
    success_url = reverse_lazy("parameter:departement-list")


class DepartementDetailView(CustomDetailView):
    model = Departement
    name = "Departement"
    template_name = "detail-departement.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Détails du Departement"
        context["update_url"] = "parameter:departement-update"
        context["delete_url"] = "parameter:departement-delete"
        context["list_url"] = "parameter:departement-list"

        return context

class DepartementDeleteView(CustomDeleteView):
    model = Departement
    name = "Departement"
    template_name ="delete.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_object()  # Utilisation de self.get_object()
        context["card_title"] = f"Suppression du Departement {object.label}"
        context["list_url"] =reverse_lazy("parameter:departement-list")  # URL du retour
        return context

    
    
        #finis

class FiliereListView(CustomListView):
    model = Filiere
    name = "filiere"
    template_name = "list-filière.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_delete"] = True

        return context


class FiliereCreateView(CustomCreateView):
    model = Filiere
    form_class = FiliereForm
    name = "filiere"
    success_url = reverse_lazy("parameter:filiere-list")


class FiliereUpdateView(CustomUpdateView):
    model = Filiere
    name = "filiere"
    form_class = FiliereForm
    template_name = "ufr_form.html"
    success_url = reverse_lazy("parameter:filiere-list")


class FiliereDetailView(CustomDetailView):
    model = Filiere
    name = "filiere"
    template_name = "detail-filiere.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Détails de la Filière"
        context["update_url"] = "parameter:filiere-update"
        context["delete_url"] = "parameter:filiere-delete"
        context["list_url"] = "parameter:filiere-list"

        return context

class FiliereDeleteView(CustomDeleteView):
    model = Filiere
    name = "filiere"
    template_name ="delete.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_object()  # Utilisation de self.get_object()
        context["card_title"] = f"Suppression de la Filière {object.label}"
        context["list_url"] =reverse_lazy("parameter:filiere-list")   # URL du retour
        return context
    
    
        #finis

class ModuleListView(CustomListView):
    model = Module
    name = "module"
    template_name = "list-modu.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_delete"] = True

        return context


class ModuleCreateView(CustomCreateView):
    model = Module
    form_class = ModuleForm
    name = "module"
    success_url = reverse_lazy("parameter:module-list")


class ModuleUpdateView(CustomUpdateView):
    model = Module
    name = "module"
    template_name = "ufr_form.html"
    form_class = ModuleForm
    success_url = reverse_lazy("parameter:module-update")


class ModuleDetailView(CustomDetailView):
    model = Module
    name = "module"
    template_name = "detail-module.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Détails du Module"
        context["update_url"] = "parameter:module-update"
        context["delete_url"] = "parameter:module-delete"
        context["list_url"] = "parameter:module-list"

        return context

class ModuleDeleteView(CustomDeleteView):
    model = Module
    name = "module"
    template_name ="delete.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_object()  # Utilisation de self.get_object()
        context["card_title"] = f"Suppression du Module {object.label}"
        context["list_url"] =reverse_lazy("parameter:module-list")  # URL du retour
        return context
    
        #finis

class EnseignantListView(CustomListView):
    model = Enseignant
    name = "enseignant"
    template_name = "list-ense.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_delete"] = True

        return context


class EnseignantCreateView(CustomCreateView):
    model = Enseignant
    form_class = EnseignantForm
    name = "enseignant"
    success_url = reverse_lazy("parameter:enseignant-list")


class EnseignantUpdateView(CustomUpdateView):
    model = Enseignant
    name = "enseignant"
    template_name = "ufr_form.html"
    form_class = EnseignantForm
    success_url = reverse_lazy("parameter:enseignant-list")


class EnseignantDetailView(CustomDetailView):
    model = Enseignant
    name = "enseignant"
    template_name = "detail-enseignant.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Détails de l'enseignant"
        context["update_url"] = "parameter:enseignant-update"
        context["delete_url"] = "parameter:enseignant-delete"
        context["list_url"] = "parameter:enseignant-list"

        return context


class EnseignantDeleteView(CustomDeleteView):
    model = Enseignant
    name = "enseignant"
    template_name ="delete.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_object()  # Utilisation de self.get_object()
        context["card_title"] = f"Suppression de l'enseignant {object.nom}"
        context["list_url"] =reverse_lazy("parameter:enseignant-list")  # URL du retour
        return context
    
    
    
class TypePaiementListView(CustomListView):
        model = TypePaiement
        name = "typepaiement"
        template_name = "list-type.html"

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["can_delete"] = True

            return context
        
class TypePaiementCreateView(CustomCreateView):
    model = TypePaiement
    form_class = TypePaiementForm
    name = "typepaiement"
    success_url = reverse_lazy("parameter:typepaiement-list")
    
class TypePaiementUpdateView(CustomUpdateView):
    model = TypePaiement
    name = "typepaiement"
    template_name = "ufr_form.html"
    form_class = TypePaiementForm
    success_url = reverse_lazy("parameter:typepaiement-list")
    
    
class TypePaiementDetailView(CustomDetailView):
    model = TypePaiement
    name = "typetaiement"
    template_name = "detail-type.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Détails du type de Paiement"
        context["update_url"] = "parameter:typepaiement-update"
        context["delete_url"] = "parameter:typepaiement-delete"
        context["list_url"] = "parameter:typepaiement-list"

        return context
    
class TypePaiementDeleteView(CustomDeleteView):
    model = TypePaiement
    name = "typepaiement"
    template_name = "delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_object()  # Récupération de l'objet
        context["card_title"] = f"Suppression du type de paiement {object.label}"  # Correction ici
        context["list_url"] = reverse_lazy("parameter:typepaiement-list")  # URL du retour
        return context
