from django.urls import path
from django.urls import include
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('lista_vacantes/', views.lista_vacantes, name='lista_vacantes'), #agregado por Jose
    path('agregar/', views.agregar_vacante, name='agregar_vacante'), #agregado por Jose
    path('eliminar_vacante/<int:id>/', views.eliminar_vacante, name='eliminar_vacante'),
    path('editar_vacante/<int:id>/', views.editar_vacante, name='editar_vacante'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)