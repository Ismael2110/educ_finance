from django.forms import forms, fields, widgets
from django.forms.models import ModelForm, ModelChoiceField
from django.db.models import Q

from formset.collection import FormMixin, FormCollection
from formset.widgets import (
    Selectize,
    DualSortableSelector,
    UploadedFileInput,
    DateInput,
)
from formset.richtext.widgets import RichTextarea
from formset.utils import FormsetErrorList
from formset.renderers.bootstrap import FormRenderer
from django.conf import settings

from .models import UFR, Departement, Filiere, Module, Enseignant , TypePaiement

from educ_finance.constants import control_elements, TEXTAREA

default_renderer = FormRenderer(
    form_css_classes="row",
    field_css_classes={
        "*": "mb-2 col-md-6 input200",
        "description": "mb-2 col-md-12 input100",
    },
)


class UfrForm(FormMixin, ModelForm):
    default_renderer = FormRenderer(
    form_css_classes="row",
    field_css_classes={
        "*": "mb-2 col-md-4 input200",
        "description": "mb-2 col-md-12 input100",
    },
)
    class Meta:
        model = UFR
        fields = ["code", "label","sigle", "description"]
        
        
class DepartementForm(FormMixin, ModelForm):
    default_renderer = default_renderer

    class Meta:
        model = Departement
        fields = ["code", "label","ufr", "description"]
        widgets = {
        }
    

class FiliereForm(FormMixin, ModelForm):
    default_renderer = default_renderer

    class Meta:
        model = Filiere
        fields = ["code", "label","departement", "description"]
        

class ModuleForm(FormMixin, ModelForm):
    default_renderer = default_renderer

    class Meta:
        model = Module
        fields = ["code","credit","volume","label","filiere", "description"]
        
        

class EnseignantForm(ModelForm):
    default_renderer = default_renderer
    class Meta:
        model = Enseignant
        fields = ['nom', 'prenom', 'email', 'departement', 'ufr', 'matricule', 'is_vacataire', 'grade']
        
    def __init__(self, *args, **kwargs):
        super(EnseignantForm, self).__init__(*args, **kwargs)
        # Exemple : rendre le champ matricule optionnel
        self.fields['matricule'].required = False

class TypePaiementForm(FormMixin, ModelForm):
    default_renderer = default_renderer
    class Meta:
        model = TypePaiement
        fields = ["code","label","description"]