from django.db import models
from educ_finance.cmodels import CommonAbstractModel


class Paiement(CommonAbstractModel):
    
    
    STATUS_CHOICES = [
        ('initie', 'Initié'),
        ('partiellement payé', 'Partiellement payé'),
        ('soldé', 'Soldé'),
    ]
    
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='initie',
        verbose_name="Statut"
    )
    
    reference = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="Référence", 
        null=True
    )
    dossier = models.ForeignKey(
        'gestion_administratif.dossier', 
        on_delete=models.CASCADE, 
        verbose_name="Dossier enseignant", 
        help_text="Dossier de l'enseignant associé", 
        null=True
    )
    montant_total_a_verser = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Montant total", 
        null=True
    )
    date_paiement = models.DateField(
        verbose_name="Date de paiement", 
        null=True
    )
    montant_verser = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Montant versé", 
        null=True
    )
    montant_restant_a_verser = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Montant restant", 
        editable=False,  # Rend le champ non éditable via l'interface d'administration
        null=True
    )
    is_tranche = models.BooleanField(
        default=False, 
        verbose_name="Paiement par tranche"
    )
    
    is_tranfered = models.BooleanField(default=False, verbose_name="Transféré")
    
    type_paiement = models.ForeignKey(
        'parameter.TypePaiement', 
        on_delete=models.CASCADE, 
        verbose_name="Type de Paiement", 
        help_text="Type de paiement associé", 
        null=True
    )
    dossier = models.ForeignKey('gestion_administratif.dossier', on_delete=models.CASCADE, verbose_name="Dossier enseignant", 
    help_text="Dossier de l'enseignant associé", null=True)

    def save(self, *args, **kwargs):
        """
        Calcule automatiquement le montant restant à payer avant de sauvegarder l'instance.
        """
        if self.montant_total_a_verser is not None and self.montant_verser is not None:
            self.montant_restant_a_verser = self.montant_total_a_verser - self.montant_verser
        super().save(*args, **kwargs)  # Appelle la méthode `save` de la classe parente

    def __str__(self):
        return f"{self.reference} - {self.dossier}"
