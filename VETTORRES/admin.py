from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Cita, UserProfile, Contacto, Comentario
from .forms import ResponderComentarioForm, ResponderContactoForm
from django.utils.translation import gettext_lazy as _

# Desregistrar el modelo User antes de registrarlo nuevamente
admin.site.unregister(User)

# Define la clase base para restricciones de eliminación
class RestrictDeleteAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        # Solo el superusuario puede eliminar información
        return request.user.is_superuser

    def has_add_permission(self, request):
        # Los superusuarios y administradores pueden agregar
        return request.user.is_superuser #or request.user.is_staff

admin.site.register(UserProfile)

# Admin para Comentario
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'comentario', 'rating', 'fecha', 'respuesta')
    list_filter = ('fecha', 'rating')
    search_fields = ('usuario__username', 'comentario')
    fields = ('usuario', 'comentario', 'rating', 'fecha', 'respuesta')
    readonly_fields = ('usuario', 'comentario', 'rating', 'fecha')

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_staff and obj:
            return ResponderComentarioForm
        return super().get_form(request, obj, **kwargs)

    def has_change_permission(self, request, obj=None):
        if obj and obj.usuario == request.user:
            return True
        return request.user.is_superuser or request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def save_model(self, request, obj, form, change):
        if request.user.is_staff and not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

# Admin para Cita
class CitaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'mascota', 'fecha', 'hora', 'motivo', 'cancelada', 'confirmada')
    list_filter = ('confirmada', 'cancelada', 'fecha')
    actions = ['confirmar_citas']

    def confirmar_citas(self, request, queryset):
        queryset.update(confirmada=True)
        self.message_user(request, "Las citas seleccionadas han sido confirmadas.")

    confirmar_citas.short_description = "Confirmar citas seleccionadas"

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser    

admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(Cita, CitaAdmin)

# Customización de UserAdmin para manejar permisos
class CustomUserAdmin(BaseUserAdmin, RestrictDeleteAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_superuser')

    fieldsets = (
        *BaseUserAdmin.fieldsets,  # Mantén los fieldsets originales
    )

    def has_view_permission(self, request, obj=None):
        # El staff puede ver los usuarios
        return request.user.is_superuser or request.user.is_staff

    def has_change_permission(self, request, obj=None):
        # El staff puede modificar usuarios
        return request.user.is_superuser or request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        # Solo el superusuario puede eliminar usuarios
        return request.user.is_superuser

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.exclude(is_superuser=True)  # Filtrar superusuarios

    def save_model(self, request, obj, form, change):
        if not obj.pk and request.user.is_superuser:
            obj.is_staff = True
        super().save_model(request, obj, form, change)

# Finalmente, registrar el modelo User con tu CustomUserAdmin
admin.site.register(User, CustomUserAdmin)

# Admin para Contacto
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'comentario', 'respuesta', 'fecha_contacto')
    search_fields = ('nombre', 'email', 'comentario')
    fields = ('nombre', 'email', 'telefono', 'comentario', 'respuesta', 'fecha_contacto')
    readonly_fields = ('nombre', 'email', 'telefono', 'comentario', 'fecha_contacto')

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_staff and obj:
            return ResponderContactoForm
        return super().get_form(request, obj, **kwargs)

    def has_change_permission(self, request, obj=None):
        if obj and obj.nombre == request.user.username:
            return True
        return request.user.is_superuser or request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def save_model(self, request, obj, form, change):
        if request.user.is_staff and not obj.pk:
            obj.nombre = request.user.username
        super().save_model(request, obj, form, change)

admin.site.register(Contacto, ContactoAdmin)