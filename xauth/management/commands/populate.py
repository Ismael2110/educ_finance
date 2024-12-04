from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


from parameter import models as params_models
from xauth.models import User


class Command(BaseCommand):
    help = "Commande pour remplir la base de données avec les données de paramétrage."

    def handle(self, *args, **options):
        if not User.objects.filter(matricule="12345L").exists():
            User.objects.create_superuser(
                username="N00708020191",
                password="password",
                first_name="Ismael",
                last_name="COMPAORE",
                email="ismaelcompaore08.com",
                birthdate=timezone.now(),
                birthplace="Ouagadougou",
                matricule="N00708020191",
                phone="74481442",
            )

        self.set_permissions()
        # self.schedule_sending_mail()

        self.stdout.write(self.style.SUCCESS("Donné ajouté avec succès"))

    def set_permissions(self):

        Permission.objects.get_or_create(
            codename="list_group",
            name="Can list group",
            
            content_type=ContentType.objects.get_for_model(Group),
        )

        self.stdout.write(self.style.SUCCESS("permissions ajoutées"))
