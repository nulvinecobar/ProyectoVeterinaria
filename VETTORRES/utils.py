#from twilio.rest import Client
#from django.conf import settings
#from twilio.base.exceptions import TwilioException
#import logging


# Configuración del logger
#logger = logging.getLogger(__name__)


#def enviar_confirmacion_whatsapp(cita, usuario_perfil):
    # Parámetros de Twilio
 #   account_sid = settings.TWILIO_ACCOUNT_SID
  #  auth_token = settings.TWILIO_AUTH_TOKEN
   # client = Client(account_sid, auth_token)
    
   
    
    #sender = settings.TWILIO_WHATSAPP_NUMBER

    #if usuario_perfil.whatsapp_number.startswith('+'):
        #recipient = f'whatsapp:{usuario_perfil.whatsapp_number}'
    #else:
     #   recipient = f'whatsapp:{usuario_perfil.whatsapp_number}'
      #  print(f"Número de WhatsApp con código de país: {recipient}")

    # Mensaje
    #mensaje = f'Hola {usuario_perfil.user.username}, tu cita con la veterinaria se ha agendado exitosamente para el {cita.fecha.strftime("%Y-%m-%d")} a las {cita.hora.strftime("%H:%M")}.\n\nMotivo: {cita.motivo}'

    #try:
     #   message = client.messages.create(
      #      body=mensaje,
       #     from_=sender,
        #    to=recipient
        #)
        #print(f"Mensaje enviado: {message.sid}")
    #except Exception as e:
     #   print(f"Error al enviar el mensaje: {e}")

    