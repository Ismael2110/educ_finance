from django.db import models
import uuid
from educ_finance.cmodels import CommonAbstractModel

class Dossier(CommonAbstractModel):
    file = models.FileField(upload_to='documents_dossier/', null=True)
    code = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        help_text="Code unique permettant d'identifier cet élément",
        null=True

    )

    enseignant = models.ForeignKey(
        'parameter.Enseignant', 
        on_delete=models.CASCADE,  
        related_name="dossiers",  
        verbose_name="Enseignant associé",
        help_text="Enseignant associé à ce dossier",
        null=True
    )

    module = models.ForeignKey(
        "parameter.Module",
        on_delete=models.CASCADE,
        related_name="dossiers",
        verbose_name="Module associé",
        help_text="Module associé à ce dossier",
        null=True
    )

    # Champs booléens pour validation et paiement
    is_valided = models.BooleanField(null=True, help_text="Indique si le dossier est validé")
    is_payed = models.BooleanField(default=False, help_text="Indique si le dossier est payé")
    is_tranfered = models.BooleanField(default=False, help_text="Indique si le dossier est transféré")
    
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
    
    montant = models.IntegerField(
        default=0, 
        verbose_name = "Montant",
    )
    
    reste_a_payer = models.IntegerField(
        default=0, 
        verbose_name = "Reste à payer",
    )

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super(Dossier, self).save(*args, **kwargs)
        
    
    class Meta:
        ordering = ["-created"]
        verbose_name = "Dossier"
        verbose_name_plural = "Dossiers"
        permissions = [
            ("list_dossier", "Can list dossier"),
            ("export_dossier", "Can export dossier"),
            ("import_dossier", "Can import dossier"),
            ("print_dossier", "Can print dossier"),
        ]

    def generate_unique_code(self):
        unique_code = uuid.uuid4().hex[:8].upper()
        while Dossier.objects.filter(code=unique_code).exists():
            unique_code = uuid.uuid4().hex[:8].upper()
        return unique_code

    def __str__(self):
        return f"Dossier {self.code} pour {self.enseignant}"

    # Méthode pour valider le dossier
    def valider_dossier(self):
        self.is_valided = True
        self.save()  # Sauvegarde de l'état mis à jour dans la base de données

    # Méthode pour rejeter le dossier
    def rejeter_dossier(self):
        self.is_valided = False
        self.save()  # Sauvegarde de l'état mis à jour dans la base de données
    