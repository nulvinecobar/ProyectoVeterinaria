from django.db import models

from django.contrib.auth.models import User,AbstractUser, Group, Permission
#from django.contrib.auth.forms import UserCreationForm
from django import forms
#from .models import CustomUser
#from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.backends import ModelBackend
#from .models import CustomUser
#from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.utils import timezone




class Veterinaria(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    #veterinaria = models.ForeignKey(Veterinaria, on_delete=models.CASCADE)
    veterinaria = models.CharField(max_length=255, default='ValorPredeterminado')  # Definir un valor predeterminado
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()


    def __str__(self):
        return self.nombre



class Cita(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mascota = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.CharField(max_length=100)
    cancelada = models.BooleanField(default=False)
    confirmada = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"Cita para {self.usuario.username}- {self.fecha} {self.hora}"


class DiaDisponible(models.Model):
    fecha = models.DateField(unique=True)
    disponible = models.BooleanField(default=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dias_disponibles', null=True, blank=True)

    def __str__(self):
        return f"{self.fecha} - {'Disponible' if self.disponible else 'No Disponible'}"


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')
    #whatsapp_number = models.CharField(max_length=20, default='N/A')

    def clean(self):
        super().clean()
        password = self.password
        if password and len(password) < 8:
            raise ValidationError(
                _("La contraseña debe tener al menos 8 caracteres."),
                code='password_too_short'
            )
        elif password and password.isdigit():
            raise ValidationError(
                code='password_entirely_numeric'
            )
        elif password and password.isalpha():
            raise ValidationError(
                _("La contraseña no puede consistir únicamente en letras."),
                code='password_entirely_alpha')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    whatsapp_number = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15, blank=True, null=True)
    comentario = models.TextField()
    respuesta = models.TextField(blank=True, null=True)  # Campo para la respuesta del staff
    fecha_contacto = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre} - {self.email}"




class Comentario(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, default=None)  # Permitir nulos y sin valor predeterminado
    comentario = models.TextField()
    rating = models.PositiveIntegerField(default=1)  # Solo el número de estrellas, entre 1 y 5
    fecha = models.DateTimeField(default=timezone.now)
    respuesta = models.TextField(blank=True, null=True)  # Campo para la respuesta del staff
    

    def __str__(self):
        return f"{self.usuario.username} - {self.fecha}"
    #def __str__(self):
     #   return self.nombre













    