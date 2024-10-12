#from django.db.models.signals import post_save
#from django.dispatch import receiver
#from django.conf import settings
#from VETTORRES.models import Cita, User  # Ajusta la importación según tus modelos
#from VETTORRES.utils import enviar_confirmacion_whatsapp
#from VETTORRES.models import UserProfile  # Asegúrate de importar tu modelo de perfil de usuario
#import logging
#from django.contrib.auth import get_user_model


#User = get_user_model()

#logger = logging.getLogger(__name__)

#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
 #   print("Signal de creación de perfil de usuario se ha disparado")
  #  if created:
   #     UserProfile.objects.create(user=instance)

#@receiver(post_save, sender=Cita)
#def enviar_confirmacion_cita(sender, instance, created, **kwargs):
 #   if created:
  #      usuario = instance.usuario
   #     if hasattr(usuario, 'whatsapp_number') and usuario.whatsapp_number:
    #        enviar_confirmacion_whatsapp(instance, usuario)
     ##      logger.warning(f"El usuario {usuario.username} no tiene un número de WhatsApp registrado.")