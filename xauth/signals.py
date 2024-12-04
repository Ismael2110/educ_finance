

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings

from .models import User

@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    print('helleo')
    if created and not instance.is_active:
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        token = PasswordResetTokenGenerator().make_token(instance)
        activation_link = reverse("user-set-password", kwargs={"uidb64": uid, "token": token})

        # Construire l'URL complète avec le domaine et le protocole configurés
        activation_url = f"{settings.SITE_PROTOCOL}://{settings.SITE_DOMAIN}{activation_link}"
        print(activation_url)
        # send_mail(
        #     subject="Activation de votre compte",
        #     message=f"Bonjour {instance.get_full_name()},\n\nVeuillez cliquer sur le lien suivant pour activer votre compte : {activation_url}",
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=[instance.email],
        #     fail_silently=False,
        # )
        print('email envoyé')  # Pour éviter les erreurs de connexion SMTP