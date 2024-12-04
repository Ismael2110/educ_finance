
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from gestion_administratif.models import Dossier
from educ_finance.views import (
    CustomCreateView,
    CustomDeleteView,
    CustomDetailView,
    CustomListView,
    CustomUpdateView,
)
from formset.views import FileUploadMixin
from .forms import PaiementForm, PaiementPartielleForm
from .models import Paiement
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from parameter.models import TypePaiement

from django.http import HttpResponse
from django.template.loader import render_to_string
from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import WeasyTemplateResponse
from django_weasyprint.utils import django_url_fetcher
from weasyprint import HTML


import tempfile



# Create your views here.
#finis

class PaiementListView(CustomListView):
    model = Paiement
    name = "paiement"
    template_name = "list-finance.html"
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_delete"] = False
        context["can_add"] = False
        context["can_update"] = False
        context["add_url"] = reverse_lazy("gestion_finance:paiement-create")
        return context


class PaiementCreateView(CustomCreateView):
    model = Paiement
    form_class = PaiementForm
    name = "paiement"
    success_url = reverse_lazy("gestion_finance:paiement-list")


class PaiementUpdateView(FileUploadMixin, CustomUpdateView):
    
    model = Paiement
    name = "paiement"
    form_class = PaiementForm
    template_name = "components/ufr_form.html"

    success_url = reverse_lazy("gestion_finance:paiement-list")


class PaiementDetailView(CustomDetailView):
    model = Paiement
    name = "paiement"
    template_name = "detail-finance.html"
    success_url = reverse_lazy("gestion_finance:paiement-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Détails du Paiement"
        context["update_url"] = "gestion_finance:paiement-update"
        context["delete_url"] = "gestion_finance:paiement-delete"
        context["list_url"] = "gestion_finance:paiement-list"
        return context


class PaiementDeleteView(CustomDeleteView):
    model = Paiement
    name = "paiement"
    template_name ="delete-finance.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_object()  # Utilisation de self.get_object()
        context["card_title"] = f"Suppression de dossier"  # Affichage du sigle
        context["list_url"] = reverse_lazy("gestion_finance:paiement-list")  # URL du retour
        context["list_of"] = "Suppression de dossier"
        return context
    

class DossierValideListView(CustomListView):
    model = Dossier
    name = "dossier"
    template_name = "list-finance1.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_delete"] = False
        context["can_add"] = False
        context["can_import"] = False
        context["can_update"] = False
        context["can_delete"] = False
        context["object_list_en_cours"] = Dossier.objects.filter(is_tranfered =True, status = "initie")
        context["object_list_transferes"] = Dossier.objects.filter(status = "partiellement payé")
        print(context["object_list_transferes"])
        context["object_list_solde"] = Paiement.objects.filter(montant_restant_a_verser=0)
        context["type_paiement_list"] = TypePaiement.objects.all() 
        return context
    
    
# def DossierPaiementCreateView(View):
#     def post(self, form):
#         id = self.kwargs.get("pk")
#         dossier = get_object_or_404(Dossier, pk=id)
#         form.instance.dossier = dossier
#         return super().form_valid(form)


def ValiderPaiement(request):
    reference = request.POST.get("reference")
    montant_total_a_verser = request.POST.get("montant_total_a_verser")
    montant_verser = request.POST.get("montant_verser")
    date_paiement = request.POST.get("date_paiement")
    type_paiement = request.POST.get("type_paiement")
    dossier_id = request.POST.get("dossier_id")

    dossier = Dossier.objects.filter(id = dossier_id).first()
    type = TypePaiement.objects.filter(id = type_paiement).first()
    
    if not (reference and montant_total_a_verser and montant_verser and date_paiement and type_paiement):
        return redirect("gestion_finance:paiement-list")
    if dossier.status == "initie":
        paiement = Paiement.objects.create(
        dossier=dossier,
        reference=reference,
        montant_total_a_verser=float(montant_total_a_verser),
        montant_verser=float(montant_verser),
        date_paiement=date_paiement,
        type_paiement=type,
        )
        dossier.montant = montant_total_a_verser
        
    elif dossier.status == "partiellement payé":
        pass
    
    dossier.is_payed = True
    dossier.save()
    paiement = Paiement.objects.create(
        dossier=dossier,
        reference=reference,
        montant_total_a_verser=float(montant_total_a_verser),
        montant_verser=float(montant_verser),
        date_paiement=date_paiement,
        type_paiement=type,
        )
    return redirect("gestion_finance:paiement-list")


class DossierPaiementCreateView(CustomCreateView):
    print(2)
    model = Paiement
    form_class = PaiementForm
    name = "paiement"
    success_url = reverse_lazy("gestion_finance:paiement-list")
    
    def get_form_class(self):
        id = self.kwargs.get("pk")
        dossier = get_object_or_404(Dossier, pk=id)
        print(dossier.status)
        if dossier.status == "initie":
            return PaiementForm
        elif dossier.status == "partiellement payé":
            return PaiementPartielleForm
    
    def form_valid(self, form):
        id = self.kwargs.get("pk")
        dossier = get_object_or_404(Dossier, pk=id)
        is_tranche = form.cleaned_data['is_tranche']
        
        if dossier.status == "initie":
            if is_tranche is 'm' :
                is_tranche = False
                form.instance.montant_restant_a_verser = 0 
                form.instance.montant_verser =  form.cleaned_data['montant_total_a_verser']
                dossier.montant = form.cleaned_data['montant_total_a_verser']
                dossier.status = "soldé"
            elif is_tranche is 'f':
                is_tranche = True
                form.instance.montant_restant_a_verser = form.cleaned_data['montant_total_a_verser'] - form.cleaned_data['montant_verser']
                form.instance.montant_verser =  form.cleaned_data['montant_verser']
                dossier.montant = form.cleaned_data['montant_total_a_verser']
                dossier.reste_a_payer = form.cleaned_data['montant_total_a_verser'] - form.cleaned_data['montant_verser']
                dossier.status = "partiellement payé"
            dossier.montant = form.cleaned_data['montant_total_a_verser']
        elif dossier.status == "partiellement payé":
            if is_tranche is 'm' :
                is_tranche = False
                form.instance.montant_restant_a_verser = 0 
                form.instance.montant_verser =  form.cleaned_data['montant_total_a_verser']
            elif is_tranche is 'f':
                is_tranche = True
                form.instance.montant_restant_a_verser = form.cleaned_data['montant_total_a_verser'] - form.cleaned_data['montant_verser']
                form.instance.montant_verser =  form.cleaned_data['montant_verser']
                dossier.montant = dossier.reste_a_payer - form.cleaned_data['montant_verser']
                dossier.status = "soldé"
        dossier.is_payed = True
        dossier.save()
        form.instance.is_tranche = is_tranche
        form.instance.dossier = dossier
        return super().form_valid(form)



from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic.detail import DetailView
from weasyprint import HTML
import os
import tempfile
from django.template.loader import render_to_string
import weasyprint


#    
class PrintReceiptView(WeasyTemplateResponseMixin, CustomDetailView):
    model = Paiement  # Modèle correspondant
    template_name = 'recu.html'

    def get_pdf_filename(self):
        paiement = self.get_object()
        return f"recu-{paiement.reference}.pdf"

    # def render_to_response(self, context, **response_kwargs):
    #     html = render_to_string(self.template_name, context)
        
    #     pdf = weasyprint.HTML(string=html).write_pdf()

    #     response = HttpResponse(pdf, content_type='application/pdf')
    #     response['Content-Disposition'] = f'attachment; filename="{self.get_pdf_filename()}"'
    #     return response


    
    