from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
#from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetView, PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin
from .views import CustomPasswordResetView, CustomPasswordResetConfirmView
from django.contrib.auth import views as auth_views
from .views import administrador_dashboard, staff_dashboard
from .views import setup_permissions_view
from .views import CustomPasswordResetView, CustomPasswordResetConfirmView, CustomPasswordResetDoneView, CustomPasswordResetCompleteView
#from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from .views import mis_citas


urlpatterns = [
    path('', views.principal, name='principal'),
    path('servicios/', views.servicios, name='servicios'),
    path('Cita/', views.Cita, name='Cita'),
    path('agendar_cita/', login_required(views.agendar_cita), name='agendar_cita'),
    path('cancelar_cita/<int:cita_id>/', views.cancelar_cita, name='cancelar_cita'),
    path('detalle-cita/<int:cita_id>/', views.detalle_cita, name='detalle_cita'),
    path('cita_confirmacion/<int:cita_id>/', views.cita_confirmacion, name='cita_confirmacion'),
    path('mis-citas/', mis_citas, name='mis_citas'),
    path('registro/', views.registro, name='registro'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('urnas/', views.catalogo_urnas, name='catalogo_urnas'),
    path('precios/', views.precios_servicios, name= 'precios_servicios'),
    path('contacto/', views.contacto, name='contacto'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    #path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #path('contacto_exitoso/', views.contacto_exitoso, name='contacto_exitoso'),
    #path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('comentarios/',login_required(views.comentarios_view), name='comentarios_view'),
    #path('administrador/', administrador_dashboard, name='administrador_dashboard'),
    #path('staff/', staff_dashboard, name='staff_dashboard'),
    path('configurar_permisos/', setup_permissions_view, name='setup_permissions'),
    
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


