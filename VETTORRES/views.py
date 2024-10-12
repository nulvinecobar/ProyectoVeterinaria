import json
from django.shortcuts import render, get_object_or_404, redirect
#from .models import InformacionContacto, Servicio
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
#from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CitaForm, ContactoForm, ComentarioForm
from .models import Cita, Comentario, Contacto
#from django.core.exceptions import ValidationError
import logging
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
logger = logging.getLogger(__name__)
from .forms import UserRegistrationForm
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetDoneView
from .models import Comentario
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Permission, User
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
#from django.db.models import Count
from .models import DiaDisponible
from .forms import CustomPasswordResetForm

#from django.core.mail import send_mail
#from twilio.rest import Client
#from django.conf import settings
#from .utils import enviar_confirmacion_whatsapp
from .models import UserProfile

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView
)





def principal(request):
    return render(request, 'pagina_principal.html')

def catalogo_urnas(request):
    return render(request, 'urnas.html')

def precios_servicios(request):
    return render(request, 'precios.html')


def servicios(request):
    # Lógica necesaria para la página de servicios
    descripcion = "Nuestra veterinaria se dedica a proporcionar cuidados de alta calidad para tus mascotas. Ofrecemos una amplia gama de servicios veterinarios, desde consultas médicas y cirugías hasta servicios de urgencias. Además, entendemos lo importante que es honrar y recordar a tus mascotas cuando llega el momento de despedirse. Es por eso que también ofrecemos servicios de cremación y una variedad de urnas personalizadas para ayudarte a preservar su memoria de manera especial. Nuestro equipo de profesionales altamente capacitados se asegurará de que tu mascota reciba el más alto nivel de cuidado en cada etapa de su vida"
    servicios_destacados = [
        "Consulta médica y vacunación", 
        "Cirugías y tratamientos quirúrgicos", 
        "Control de pulgas y garrapatas", 
        "Estética y cuidado del pelaje",
    ]
    context = {
        'descripcion': descripcion, 
        'servicios_destacados': servicios_destacados}
    return render(request, 'servicios.html', context)


@login_required
def agendar_cita(request):
    usuario = request.user
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)  # Guardar la cita en la base de datos
            cita.usuario = request.user #asigna la cita al ususario actual
            cita.save()
            if not UserProfile.objects.filter(user=request.user).exists():
                UserProfile.objects.create(user=request.user)
            # Verifica si el perfil de usuario existe
            try:
                usuario_perfil = UserProfile.objects.get(user=request.user)
                print(f"Perfil de usuario: {usuario_perfil}, Número de WhatsApp: {usuario_perfil.whatsapp_number}")
                if usuario_perfil.whatsapp_number:
                    # Enviar confirmación por WhatsApp
                    #enviar_confirmacion_whatsapp(cita, usuario_perfil)
                    print(f"Mensaje enviado al número: {usuario_perfil.whatsapp_number}")
                else:
                    messages.error(request, 'El perfil de usuario no tiene un número de WhatsApp registrado.')
            except UserProfile.DoesNotExist:
                # Manejar el caso en el que el perfil no existe
                messages.error(request, 'No se ha encontrado el perfil de usuario para enviar la confirmación por WhatsApp.')
            messages.success(request, 'La cita ha sido agendada exitosamente.')
            return redirect('agendar_cita')
            
    else:
    
       form = CitaForm()
    return render(request, 'cita.html', {'form': form, 'usuario': usuario })


@login_required
def mis_citas(request):
    citas = Cita.objects.filter(usuario=request.user)
    return render(request, 'mis_citas.html', {'citas': citas})


def cancelar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, usuario=request.user)

    if request.method == "POST":
        cita.cancelada = True  # Marca la cita como cancelada
        cita.save()
        messages.success(request, "La cita ha sido cancelada con éxito.")
        return redirect('mis_citas')  # Redirige a la página de citas del usuario

    return render(request, 'cancelar_cita.html', {'cita': cita})


@login_required
def detalle_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, usuario=request.user)
    return render(request, 'detalle_cita.html', {'cita': cita})


def cita_confirmacion(request, cita_id):
    cita = Cita.objects.get(id=cita_id)
    return render(request, 'cita_confirmacion.html', {'cita': cita})




#nuevo inicio de sesion  

@csrf_protect
def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username').strip()
            password = form.cleaned_data.get('password').strip()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Verificar el rol del usuario y redirigir
                if user.is_superuser:
                    return redirect('admin:index')  # Panel de administración para superusuario
                elif user.is_staff:
                    if user.has_perm('auth.add_user'):
                        return redirect('admin:index')  # Panel de administrador
                    return redirect('admin:index')  # Panel de staff
                else:
                    return redirect('principal')  # Redirigir a la página principal si es un usuario normal
            else:
                messages.error(request, 'Credenciales inválidas. Por favor, inténtelo de nuevo.')
    else:
        form = AuthenticationForm()
    return render(request, 'iniciar_sesion.html', {'form': form})

# fechas disponibles

def actualizar_dia_disponible(cita):
    dia_disponible, created = DiaDisponible.objects.get_or_create(fecha=cita.fecha)
    citas_en_el_dia = Cita.objects.filter(fecha=cita.fecha).count()
    
    # Por ejemplo, consideramos que el día se vuelve no disponible después de 5 citas
    dia_disponible.disponible = citas_en_el_dia < 5
    dia_disponible.save()

# permisos admin super user

def es_superuser_o_admin(user):
    return user.is_superuser or (user.is_staff and user.has_perm('auth.add_user'))

@user_passes_test(lambda u: u.is_superuser)
def setup_permissions_view(request):
    try:
        # Configura permisos para el administrador
        admin_user = User.objects.get(username='nombre_admin')
        admin_user.is_staff = True
        admin_user.user_permissions.set([
            Permission.objects.get(codename='add_user'),
            Permission.objects.get(codename='change_user'),
            Permission.objects.get(codename='can_add_comment'),
            Permission.objects.get(codename='can_reply_comment'),
        ])
        admin_user.save()

        # Configura permisos para el staff
        staff_user = User.objects.get(username='nombre_staff')
        staff_user.is_staff = True
        staff_user.user_permissions.set([
            Permission.objects.get(codename='can_add_comment'),
            Permission.objects.get(codename='can_reply_comment'),
        ])
        staff_user.save()

        return HttpResponse("Permissions set up successfully.")

    except User.DoesNotExist:
        return HttpResponse("User not found.")
    except Permission.DoesNotExist:
        return HttpResponse("One or more permissions not found.")


#vistas admin y staff
@login_required
@user_passes_test(lambda u: u.is_staff and u.has_perm('auth.add_user'))
def administrador_dashboard(request):
    return render(request, 'administrador_dashboard.html')

@login_required
@user_passes_test(lambda u: u.is_staff and not u.has_perm('auth.add_user'))
def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')

#dashboards
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
@user_passes_test(lambda u: u.is_staff and not u.is_superuser)
def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')


@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('iniciar_sesion')  # Redirigir si no es superusuario

    citas = Cita.objects.all()
    comentarios = Comentario.objects.all()
    contactos = Contacto.objects.all()
    
    context = {
        'citas': citas,
        'comentarios': comentarios,
        'contactos': contactos,
    }
    
    return render(request, 'admin_dashboard.html', context)


@login_required
def staff_dashboard(request):
    if not request.user.is_staff or request.user.is_superuser:
        return redirect('iniciar_sesion')  # Redirigir si no es staff

    citas = Cita.objects.all()
    comentarios = Comentario.objects.all()
    
    context = {
        'citas': citas,
        'comentarios': comentarios,
    }
    
    return render(request, 'staff_dashboard.html', context)


class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    success_message = "Se ha enviado un correo con las instrucciones para restablecer tu contraseña."

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'

# Vista para el formulario de restablecimiento de contraseña
#class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
 #   template_name = 'password_reset.html'
  #  success_url = reverse_lazy('password_reset')
   # success_message = "Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña."

# Vista para la confirmación de restablecimiento de contraseña
#class CustomPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
 #   template_name = 'password_reset_confirm.html'
  #  success_url = reverse_lazy('iniciar_sesion')
   # success_message = "Tu contraseña ha sido restablecida con éxito. Inicia sesión con tu nueva contraseña."

    #def form_valid(self, form):
     #  print(f"Contraseña cambiada para el usuario: {user.username}")
      #  return super().form_valid(form)

#class CustomPasswordResetDoneView(PasswordResetDoneView):
 #   template_name = 'password_reset_done.html'    

@csrf_protect
def registro(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #UserProfile.objects.create(user=user, whatsapp_number=form.cleaned_data.get('whatsapp_number'))
            login(request, user)
            messages.success(request, 'Tu registro ha sido exitoso. Ahora puedes iniciar sesión.')
            return redirect('iniciar_sesion')  # Redirigir a la página de inicio de sesión después del registro
    else:
        form = UserRegistrationForm()
    return render(request, 'registro.html', {'form': form})





def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            print("Formulario válido, guardando contacto...")
            form.save()
            messages.success(request, 'Contacto guardado exitosamente.')
            return redirect('contacto')  # Redirige a la página de éxito
        else:
            print("Formulario no válido:", form.errors)
            #print(form.errors)  # Imprime los errores del formulario en la consola para depuración
    else:
        form = ContactoForm()
    
    return render(request, 'contacto.html', {'form': form})



def contacto_exitoso(request):
    return render(request, 'contacto_exitoso.html')




@login_required
def comentarios_view(request):
    comentarios = Comentario.objects.order_by('-fecha')  # Mostrar los comentarios más recientes primero

    if request.method == 'POST':
        if not request.user.is_authenticated:
            # Si el usuario no está autenticado, mostrar un mensaje de error
            messages.error(request, 'Debes iniciar sesión para dejar un comentario.')
            return redirect('iniciar_sesion')  # Redirige al usuario a la página de inicio de sesión
        form = ComentarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)  # Guardar la cita en la base de datos
            usuario.usuario = request.user
            form.save()
            messages.success(request, 'Comentario enviado exitosamente.')
            return redirect('principal')  # Redirigir a la página de inicio después de guardar
    else:
        form = ComentarioForm()

    # Calcular estrellas llenas y vacías para cada comentario
    comentarios_info = []
    for comentario in comentarios:
        llenas = '☆' * (5 - comentario.rating)
        vacias = '★' * (comentario.rating)
        
        comentarios_info.append({
            'nombre': comentario.nombre,
            'usuario': comentario.usuario.username if comentario.usuario else 'Desconocido',
            'comentario': comentario.comentario,
            'fecha': comentario.fecha,  # Agregamos la fecha
            'estrellas': llenas + vacias,
            'respuesta': comentario.respuesta, 
        })    

    return render(request, 'comentarios.html', {'form': form, 'comentarios_info': comentarios_info})






















    