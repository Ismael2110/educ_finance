# gestion_finance/forms.py

# gestion_finance/forms.py

from django import forms
from .models import Paiement
from formset.collection import FormMixin, FormCollection
from formset.renderers.bootstrap import FormRenderer

class PaiementForm(FormMixin, forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-4 input200",
            "description": "mb-2 col-md-12 input100",
        },
    )
    
    class Meta:
        model = Paiement
        fields = ['reference', 'montant_total_a_verser', 'montant_verser', 'date_paiement', 'type_paiement']
        widgets = {
            'date_paiement': forms.DateInput(attrs={'type': 'date'}),
        }
