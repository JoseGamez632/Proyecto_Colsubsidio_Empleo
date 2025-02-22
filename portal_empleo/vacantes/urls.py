from django.urls import path
from django.urls import include
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.auth import views as auth_views
from .views import registro_candidato_view
from .views import cargar_ciudades, RegistrationGuideView, exportar_candidatos_excel, descargar_candidatos


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('lista_vacantes/', views.lista_vacantes, name='lista_vacantes'), #agregado por Jose
    path('agregar/', views.agregar_vacante, name='agregar_vacante'), #agregado por Jose
    path('eliminar_vacante/<int:id>/', views.eliminar_vacante, name='eliminar_vacante'),
    path('editar_vacante/<int:id>/', views.editar_vacante, name='editar_vacante'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('registro/', views.registro_candidato_view, name='registro_candidato'),  # El nombre de la URL para el formulario
    path('descargar_excel/', views.descargar_excel, name='descargar_excel'),
    path('vacantes/<int:id>/candidatos/', views.lista_candidatos, name='lista_candidatos'),
    path('registros/', views.lista_registros, name='lista_registros'),
    path('editar/<int:pk>/', views.editar_registro, name='editar_registro'),
    path('cambiar_estado_vacante/<int:vacante_id>/', views.cambiar_estado_vacante, name='cambiar_estado_vacante'),
    path('cargar-ciudades/', cargar_ciudades, name="cargar_ciudades"),
    path('registration-guide/', RegistrationGuideView.as_view(), name='registration_guide'),
    path("exportar-candidatos/", exportar_candidatos_excel, name="exportar_candidatos"),
    path('descargar-candidatos/', descargar_candidatos, name='descargar_candidatos'),












] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)