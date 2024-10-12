from django import forms
from .models import Cita
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser
from .models import Contacto
#from .forms import CustomUserCreationForm
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#from .models import AdminUser
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import password_validation
#from .models import Comets
#from .models import Coment
from .models import Comentario
from .models import UserProfile
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.password_validation import password_validators_help_text_html
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm

class CitaForm(forms.ModelForm):
    
    class Meta:
        model = Cita
        fields = ['mascota', 'fecha', 'hora', 'motivo']
    
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        # Aquí puedes agregar validaciones adicionales sobre la fecha
        return fecha

    def clean_hora(self):
        hora = self.cleaned_data.get('hora')
        # Aquí puedes agregar validaciones adicionales sobre la hora
        return hora


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu correo electrónico'
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Aquí puedes agregar validaciones adicionales si es necesario
        return email




class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    whatsapp_number = forms.CharField(max_length=13, required=False, label="Número de WhatsApp")


    class Meta:
        model = User
        fields = ['username', 'email', 'whatsapp_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Crear o actualizar el perfil de usuario con el número de WhatsApp
            UserProfile.objects.create(user=user, whatsapp_number=self.cleaned_data['whatsapp_number'])
        return user    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        valid_domains = ['gmail.com', 'hotmail.com']
        valid_domain_suffix = ['.mx', '.com', '.com.mx']

        if email:
            domain = email.split('@')[-1]

            if domain not in valid_domains and not domain.endswith(tuple(valid_domain_suffix)):
                raise forms.ValidationError("El correo electrónico debe ser de un dominio válido (gmail.com, hotmail.com, o .mx).")

            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Este correo electrónico ya está en uso.")

        return email

    def clean_whatsapp_number(self):
        whatsapp_number = self.cleaned_data.get('whatsapp_number')
        if not whatsapp_number.isdigit() or len(whatsapp_number) != 10:
            raise forms.ValidationError("El número de WhatsApp debe contener solo dígitos.")
        return whatsapp_number
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        # Guarda el número de WhatsApp en el perfil del usuario
        whatsapp_number = self.cleaned_data.get('whatsapp_number')
        print(f"Numero de WhatsApp recibido: {whatsapp_number}")
        UserProfile.objects.update_or_create(user=user, defaults={'whatsapp_number': whatsapp_number})
        return user


    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data
    

    
class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'email', 'telefono', 'comentario']

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')

        if telefono:
            # Elimina cualquier carácter no numérico
            telefono = re.sub(r'\D', '', telefono)

            # Verifica si el número de teléfono tiene exactamente 10 dígitos
            if len(telefono) != 10:
                raise ValidationError("El número de teléfono debe tener exactamente 10 dígitos.")

        return telefono
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        valid_domains = ['gmail.com', 'hotmail.com']
        valid_domain_suffix = '.mx'

        if email:
            domain = email.split('@')[-1]

            # Verificar si el dominio es uno de los válidos
            if domain not in valid_domains and not domain.endswith(valid_domain_suffix):
                # Añadir el error personalizado al campo 'email'
                self.add_error('email', "El correo electrónico debe ser de un dominio válido (gmail.com, hotmail.com, o .mx).")

        return email





class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['comentario', 'rating']



class ResponderComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['respuesta']
        widgets = {
            'respuesta': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }


class ResponderContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['respuesta']
        widgets = {
            'respuesta': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }


#restablecer contrasenia
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Confirmar Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return new_password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data["new_password1"])
            user.save()
        return user

#class CambiarContraseniaForm(PasswordChangeForm):
 #   old_password = forms.CharField(
  #      label="Contraseña actual",
   #     strip=False,
    #    widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    #)
   # new_password1 = forms.CharField(
    #    label="Nueva contraseña",
     #   widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
      #  strip=False,
       # help_text=password_validation.password_validators_help_text_html(),
    #)
    #new_password2 = forms.CharField(
     #   label="Confirmar nueva contraseña",
      #  strip=False,
       # widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    #)

    #def clean_new_password2(self):
     #   new_password1 = self.cleaned_data.get("new_password1")
      #  new_password2 = self.cleaned_data.get("new_password2")
        #if new_password1 and new_password2 and new_password1 != new_password2:
         #   raise forms.ValidationError("Las contraseñas no coinciden.")
        #return new_password2

    #def __init__(self, *args, **kwargs):
     #   super().__init__(*args, **kwargs)
      #  for fieldname in ['old_password', 'new_password1', 'new_password2']:
       #     self.fields[fieldname].widget.attrs.update({'class': 'form-control'})
    

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Confirmar Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return new_password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data["new_password1"])
            user.save()
        return user    


         

            
        


        


