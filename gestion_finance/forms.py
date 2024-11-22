from django import forms
from .models import Paiement
from formset.collection import FormMixin
from formset.renderers.bootstrap import FormRenderer


class PaiementForm(FormMixin, forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-4 input200",
            "description": "mb-2 col-md-12 input100",
        },
    )
    
    is_tranche = forms.fields.ChoiceField(
        label="Est un paiement par tranche ?",
        choices=[('f', "Oui"), ('m', "Non")],
        widget=forms.widgets.RadioSelect,
    )

    montant_verser = forms.fields.IntegerField(
        label="Montant versé pour ce paiement",
        required=False,
        widget=forms.widgets.NumberInput(attrs={'df-show': ".is_tranche=='f'"})
    )

    # Champ calculé et affiché uniquement
    montant_restant_a_verser = forms.DecimalField(
        label="Montant restant à verser",
        disabled=True,  # Rendre ce champ non modifiable
        required=False,  # Pas obligatoire car calculé automatiquement
    )

    class Meta:
        model = Paiement
        fields = [
            'reference',
            'montant_total_a_verser',
            'date_paiement',
            'type_paiement'
        ]  # Retirer 'montant_restant_a_verser'

        widgets = {
            'date_paiement': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        """
        Recalcule le champ montant_restant_a_verser à chaque validation du formulaire.
        """
        cleaned_data = super().clean()
        montant_total = cleaned_data.get('montant_total_a_verser')
        montant_verser = cleaned_data.get('montant_verser')
        if montant_total is not None and montant_verser is not None:
            cleaned_data['montant_restant_a_verser'] = montant_total - montant_verser
        return cleaned_data





class PaiementPartielleForm(FormMixin, forms.ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-2 col-md-4 input200",
            "description": "mb-2 col-md-12 input100",
        },
    )
    
    is_tranche = forms.fields.ChoiceField(
        label="Est un paiement par tranche ?",
        choices=[('f', "Oui"), ('m', "Non")],
        widget=forms.widgets.RadioSelect,
    )

    montant_verser = forms.fields.IntegerField(
        label="Montant versé pour ce paiement",
        required=False,
        widget=forms.widgets.NumberInput(attrs={'df-show': ".is_tranche=='f'"})
    )

    # Champ calculé et affiché uniquement
    montant_restant_a_verser = forms.DecimalField(
        label="Montant restant à verser",
        disabled=True,  # Rendre ce champ non modifiable
        required=False,  # Pas obligatoire car calculé automatiquement
    )

    class Meta:
        model = Paiement
        fields = [
            'reference',
            'date_paiement',
            'type_paiement'
        ]  # Retirer 'montant_restant_a_verser'

        widgets = {
            'date_paiement': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        """
        Recalcule le champ montant_restant_a_verser à chaque validation du formulaire.
        """
        cleaned_data = super().clean()
        montant_total = cleaned_data.get('montant_total_a_verser')
        montant_verser = cleaned_data.get('montant_verser')
        if montant_total is not None and montant_verser is not None:
            cleaned_data['montant_restant_a_verser'] = montant_total - montant_verser
        return cleaned_data
