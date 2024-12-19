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

from .models import Dossier

from educ_finance.constants import control_elements, TEXTAREA

default_renderer = FormRenderer(
    form_css_classes="row",
    field_css_classes={
        "*": "mb-2 col-md-6 input200",
        "description": "mb-2 col-md-12 input100",
    },
)

class DossierForm(FormMixin, ModelForm):
    default_renderer = FormRenderer(
    form_css_classes="row",
    field_css_classes={
        "*": "mb-2 col-md-4 input200",
        "description": "mb-2 col-md-12 input100",
    },
)
    class Meta:
        model = Dossier
        fields = ["file", "enseignant", "module"]
        widgets = { 
            "file": UploadedFileInput(attrs={"max-size": 1024 * 1024 * 3}),
        }
        labels = {
            "file": "Document à uploader",  # Nouveau nom pour le champ 'file'
            "enseignant": "Nom de l'enseignant",  # Nouveau nom pour 'enseignant'
            "module": "Module concerné",  # Nouveau nom pour 'module'
        }


