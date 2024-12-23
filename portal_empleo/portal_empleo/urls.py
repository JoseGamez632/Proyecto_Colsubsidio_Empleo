from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el panel de administración.
    path('', include('vacantes.urls')),  # Ruta para las vistas de la aplicación `vacantes`.
]
