# gestion_finance/models.py

from django.db import models
from educ_finance.cmodels import CommonAbstractModel


class Paiement(CommonAbstractModel):
    reference = models.CharField(max_length=20, unique=True, verbose_name="Référence", null=True)
    dossier = models.ForeignKey('gestion_administratif.dossier', on_delete=models.CASCADE, verbose_name="Dossier enseignant", help_text="Dossier de l'enseignant associé", null=True)
    montant_total_a_verser = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant total",null=True)
    date_paiement = models.DateField(verbose_name="Date de paiement",null=True)
    montant_verser = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant verser",null=True)
    montant_restant_a_verser = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant restant",null=True)
    is_tranche = models.BooleanField(default=False, verbose_name="paiement par tranche") 
    type_paiement = models.ForeignKey(
        'parameter.TypePaiement', on_delete=models.CASCADE, verbose_name="Type de Paiement", help_text="Type de paiement associé", null=True 
    )
    def __str__(self):
        return f"{self.reference} - {self.dossier} "
