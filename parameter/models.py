from django.db import models

# Create your models here.

from educ_finance.cmodels import (
    ParameterModel,
    CONSTRAINT,
    CommonAbstractModel,
    AutoSlugField,
    StatusModel,
    CommonAbstractModelWithCodeModel,
)
from educ_finance.constants import MIN_LENGTH, MEDIUM_LENGTH, BIG_LENGTH

class MailContent(CommonAbstractModel):
    slug = AutoSlugField(
        populate_from="label", always_update=True, max_length=MEDIUM_LENGTH, unique=True
    )
    label = models.CharField("Libellé", max_length=MEDIUM_LENGTH, unique=True)

    class Meta:
        abstract = True





from django.db import models

class UFR(ParameterModel): 
    sigle = models.CharField(max_length=10, unique=True, verbose_name="Sigle", null=True)

    class Meta:
        ordering = ["label"]
        verbose_name = "UFR"
        verbose_name_plural = "UFRs"
        permissions = [
            ("list_ufr", "Can list ufr"),
            ("export_ufr", "Can export ufr"),
            ("import_ufr", "Can import ufr"),
            ("print_ufr", "Can print ufr"),
        ]

    def __str__(self):
        return f"{self.sigle} - {self.label}"


class Departement(ParameterModel):
    ufr = models.ForeignKey(
        UFR,
        on_delete=models.CASCADE,
        related_name="departements",  # Relation pour accéder aux départements liés à une UFR
        verbose_name="UFR associée", null=True
    )

    class Meta:
        ordering = ["label"]
        verbose_name = "Departement"
        verbose_name_plural = "Departements"
        permissions = [
            ("list_departement", "Can list departement"),
            ("export_departement", "Can export departement"),
            ("import_departement", "Can import departement"),
            ("print_departement", "Can print departement"),
        ]

    def __str__(self):
        return f"{self.label} ({self.ufr})"


class Filiere(ParameterModel):
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, related_name="filieres", verbose_name="Département associé")
    
    class Meta:
        ordering = ["label"]
        verbose_name = "Filiere"
        verbose_name_plural = "Filieres"
        permissions = [
            ("list_filiere", "Can list filiere"),
            ("export_filiere", "Can export filiere"),
            ("import_filiere", "Can import filiere"),
            ("print_filiere", "Can print filiere"),
        ]
    def __str__(self):
        return f"{self.label} ({self.departement})"

class Module(ParameterModel):  # Assurez-vous que cette classe hérite de models.Model ou d'une autre classe appropriée.
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name="modules", verbose_name="Filière associée", null=True)
    volume = models.PositiveIntegerField(verbose_name="Volume ", null=True)
    credit = models.PositiveIntegerField(verbose_name="Crédits " ,null=True)

    class Meta:
        ordering = ["label"]
        verbose_name = "Module"
        verbose_name_plural = "Modules"
        permissions = [
            ("list_module", "Can list module"),
            ("export_module", "Can export module"),
            ("import_module", "Can import module"),
            ("print_module", "Can print module"),
        ]

    def __str__(self):
        return f"{self.label} ({self.code})"

from django.db import models

from django.db import models

class Enseignant(CommonAbstractModel):
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    email = models.EmailField(unique=True, verbose_name="Email")
    departement = models.ForeignKey(
        Departement,
        on_delete=models.SET_NULL,
        null=True,
        related_name="enseignants",
        verbose_name="Département associé"
    )
    ufr = models.ForeignKey(
        UFR,
        on_delete=models.CASCADE,
        related_name="enseignants",
        verbose_name="UFR associée",
        null=True
    )
    matricule = models.PositiveIntegerField(verbose_name="Numéro Matricule", null=True, blank=True)
    is_vacataire = models.BooleanField(default=False, verbose_name="Est Vacataire")  # Indicateur pour vacataire
    
    # Champ pour les grades avec des choix prédéfinis
    GRADE_CHOICES = [
        ('ingenieur', "Ingénieur"),
        ('assistant', "Assistant"),
        ('maitre_assistant', "Maître Assistant"),
        ('maitre_conference', "Maître de Conférences"),
        ('professeur', "Professeur Titulaire"),
    ]
    grade = models.CharField(
        max_length=20,
        choices=GRADE_CHOICES,
        default='assistant',
        verbose_name="Grade", null=True
    )

    class Meta:
        ordering = ["nom"]
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"
        permissions = [
            ("list_enseignant", "Can list enseignant"),
            ("export_enseignant", "Can export enseignant"),
            ("import_enseignant", "Can import enseignant"),
            ("print_enseignant", "Can print enseignant"),
        ]
    
    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.get_grade_display()} ({self.departement})"

    def get_name(self):
        return f"{self.prenom} {self.nom}"

    def get_grade(self):
        """Retourne le grade de l'enseignant en texte lisible."""
        return self.get_grade_display()


class TypePaiement(ParameterModel):
    actif = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Type de Paiement"
        verbose_name_plural = "Types de Paiement"
    
    def __str__(self):
        return self.label