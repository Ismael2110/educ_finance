from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from model_utils.choices import Choices
from datetime import datetime
from phonenumber_field.modelfields import PhoneNumberField
from educ_finance.constants import MEDIUM_LENGTH, MIN_LENGTH
from model_utils.models import (
    TimeStampedModel,
    UUIDModel,
    SoftDeletableModel,
    StatusModel,
)
CONSTRAINT = models.PROTECT

class CommonAbstractModel(TimeStampedModel, UUIDModel, SoftDeletableModel):
    is_active = models.BooleanField("Est actif", default=True)

    class Meta:
        abstract = True

# xauth/models.py
from django.db import models

class Teacher(models.Model):
    # Champs du modèle Teacher
    name = models.CharField(max_length=255)
    speciality = models.CharField(max_length=255)

    def __str__(self):
        return self.name



from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser, CommonAbstractModel):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]  # Retirer 'email' ici

    first_name = models.CharField(_("first name"), max_length=100)
    last_name = models.CharField(_("last name"), max_length=100)
    email = models.EmailField(_("email address"), unique=True)
    birthdate = models.DateField("Date de naissance")
    birthplace = models.CharField("Lieu de naissance", max_length=100)
    matricule = models.CharField(max_length=50, unique=True)
    address = models.CharField("Adresse", max_length=50, null=True, blank=True)
    phone = PhoneNumberField("Numéro de téléphone", unique=True)

    def get_role(self):
        if self.is_staff:
            return "admin"
        elif hasattr(self, "assign"):
            return self.assign.group_assign.name
        else:
            return "-"

    def __str__(self):
        return f"{self.get_full_name()}"

    class Meta:
        ordering = ["first_name", "last_name"]
        verbose_name = "utilisateur"
        verbose_name_plural = "utilisateurs"
        permissions = [
            ("list_user", "Can list user"),
            ("deactivate_user", "Can deactivate user"),
            ("change_right_user", "Can change user right"),
            ("access_parameter", "Can access to parameter module"),
            ("access_account", "Can access to account module"),
            ("access_statistics", "Can access to statistics module"),
            ("access_gestion_finance", "Can access to gestion_finance module"),
            ("access_gestion_administratif", "Can access to gestion_administratif module"),
            ("view_dossier_enseignant", "Can access to dossier"),
            ("gestion_administratif.view_status_dossier", "Can access to gestion_administratif statut"),
            ("gestion_administratif.view_rapport_academique", "Can access to gestion_administratif rapport"),
            ("is_responsable_administrative", "est un responsable administratif"),
            ("is_responsable_financier", "est un responsable financier"),
            
        ]



"""class AccountActivationSecret(CommonAbstractModel):
    user = models.OneToOneField(User, on_delete=CONSTRAINT)
    secret = models.CharField(max_length=50)"""


"""class Assign(CommonAbstractModel):
    user = models.OneToOneField(
        User, on_delete=CONSTRAINT, related_name="assign", null=True, blank=True
    )

    group_assign = models.ForeignKey(
        "auth.Group", on_delete=CONSTRAINT, null=True, blank=True
    )"""


# Définition du modèle UserProfile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class AccountActivationSecret(CommonAbstractModel):
    user = models.OneToOneField(User, on_delete=CONSTRAINT)
    secret = models.CharField(max_length = MIN_LENGTH)


class Assign(CommonAbstractModel):
    assigner = models.ForeignKey(
        User, on_delete=CONSTRAINT, related_name="assigner", null=True, blank=True
    )
    unassigner = models.ForeignKey(
        User, on_delete=CONSTRAINT, related_name="unassigner", null=True, blank=True
    )
    
    user = models.OneToOneField(
        User, on_delete=CONSTRAINT, related_name="assign", null=True, blank=True
    )

    nomination_date = models.DateField(null=True)
    effective_date = models.DateField(null=True)
    end_date = models.DateField(null=True, blank=True)
    group_assign = models.ForeignKey(
        "auth.Group", on_delete=CONSTRAINT, null=True, blank=True
    )