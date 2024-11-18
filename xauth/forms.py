from datetime import timedelta, date

# from typing import Any
from django.forms import forms, fields, widgets
from django.forms.models import ModelForm, ModelChoiceField
from django.db.models import Q
from django.contrib.auth.models import Group, Permission, User
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from formset.collection import FormMixin, FormCollection
from formset.widgets import (
    Selectize,
    DualSortableSelector,
    UploadedFileInput,
    DateInput,
)
from formset.utils import FormsetErrorList
from formset.renderers.bootstrap import FormRenderer
from django.conf import settings

from educ_finance.constants import MEDIUM_LENGTH, MIN_LENGTH, submit
from parameter import models as params_models

from xauth.models import User, Assign, AccountActivationSecret


MINIMUM_AGE = 18 * 365

default_renderer = FormRenderer(
    form_css_classes="row",
    field_css_classes={"*": "mb-2 col-md-6 input100"},
)


class GroupForm(FormMixin, ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={"*": "mb-2 col-md-12 input100"},
    )

    def __init__(self, error_class=FormsetErrorList, **kwargs):
        super().__init__(error_class, **kwargs)
        permissions = Permission.objects.filter(
            content_type__app_label__in=[
                "xauth",
                "auth",
                "parameter",
                "gestion_administratif",
                "gestion_finance",
            ]
        )
        permissions = permissions.exclude(
            content_type__model__in=[
                "assign",
                "accountactivationsecret",
                "historicalassign",
            ]
        )
        self.fields["permissions"].queryset = permissions

    class Meta:
        model = Group
        fields = "__all__"
        widgets = {
            "permissions": DualSortableSelector(
                search_lookup=["name__icontains"],
                group_field_name="content_type",
            )
        }


class CustomSetPasswordForm(FormMixin, SetPasswordForm):
    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        self.user.is_active = True
        self.user.save()

        return self.user


class UserCreateForm(FormMixin, ModelForm):
    default_renderer = FormRenderer(
        form_css_classes="row",
        field_css_classes={
            "*": "mb-3 col-md-6",
            "photo": "mb-5 col-md-6",
            "folder": "mb-5 col-md-6",
        },
    )


    def __init__(self, error_class=FormsetErrorList, user: User = None, **kwargs):
        super().__init__(error_class, **kwargs)

    def clean__gender(self):
        gender = self.cleaned_data["gender"]

        if not gender:
            raise forms.ValidationError(
                "Ce champ est obligatoire", code="mandatory_field"
            )
        return gender

        return marital_status

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "birthdate",
            "birthplace",
            "email",
            "matricule",
            "address",
            "phone",
        ]
        widgets = {
            "birthdate": DateInput,
        }
        labels = {
            "email": "Adresse email",
            "address": "Adresse",
        }


class UserChangeForm(FormMixin, ModelForm):
    default_renderer = default_renderer

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "birthdate",
            "birthplace",
            "email",
            "matricule",
            "address",
            "phone",
        ]
        widgets = {
            "birthdate": DateInput,
        }
        labels = {"email": "Adresse email"}


class UserConfirmDeleteForm(forms.Form):
    default_renderer = default_renderer
    matricule = fields.CharField(max_length=MIN_LENGTH)

    def __init__(self, error_class=FormsetErrorList, user=None, **kwargs):
        super().__init__(error_class, **kwargs)
        self.user = user

    def clean_matricule(self):
        matricule = self.cleaned_data.get("matricule")
        if matricule != self.user.matricule:
            raise forms.ValidationError("Le matricule ne correspond pas!")
        return matricule

from django import forms
from .models import UserProfile  # Assure-toi d'importer le bon modèle
from django.db import models


class UserChangeProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = UserProfile  # Utiliser UserProfile au lieu de User
        fields = ['photo']
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'max-size': 1024 * 1024 * 3})
        }



class UserPublicActivationForm(FormMixin, forms.Form):
    identifier = fields.CharField(
        max_length=MIN_LENGTH,
        label="Identifiant",
        help_text="Vous pouvez saisir soit votre email ou votre matricule",
    )
    secret = fields.CharField(
        max_length=MIN_LENGTH,
        label="Code secret",
        help_text="Il s'agit du code que vous avez reçu par mail/sms",
    )

    default_renderer = default_renderer

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data["identifier"]
        secret = cleaned_data["secret"]

        user = User.objects.filter(Q(matricule=identifier) | Q(email=identifier))
        if not user.exists():
            raise forms.ValidationError(
                "Les informations fournies ne correspondent pas à un compte.",
                code="mismatch_account",
            )

        user = user.first()
        if user.is_active:
            raise forms.ValidationError(
                "Cet utilisateur est déja activé",
                code="mismatch_account",
            )

        exist = AccountActivationSecret.available_objects.filter(
            user=user, secret=secret
        ).exists()
        if not exist:
            raise forms.ValidationError(
                "Les informations fournies ne correspondent pas à un compte code.",
                code="mismatch_account",
            )
        cleaned_data["user"] = user
        return cleaned_data


class AssignForm(FormMixin, ModelForm):
    default_renderer = default_renderer

    def __init__(self, error_class=FormsetErrorList, **kwargs):
        super().__init__(error_class, **kwargs)
        if "instance" in kwargs and kwargs["instance"] is not None:
            # self.fields["code"].widget.attrs["readonly"] = True
            pass

    class Meta:
        model = Assign
        fields = ["group_assign"]
        widgets = {
            "office": Selectize(
                search_lookup="label__icontains",
                placeholder="Choisir le poste",
            ),
        }


class RoleForm(FormMixin, ModelForm):
    default_renderer = default_renderer

    #
    def __init__(self, error_class=FormsetErrorList, user: User = None, **kwargs):
        super().__init__(error_class, **kwargs)
        if "instance" in kwargs and kwargs["instance"] is not None:
            # self.fields["structure"].widget.attrs["readonly"] = True
            pass

    class Meta:
        model = Assign
        fields = [
            "group_assign",
        ]
        widgets = {
            "group_assign": Selectize(
                search_lookup="label__icontains",
                placeholder="Choisir le rôle",
            ),
        }
        labels = {
            "group_assign": "Rôle",
        }


