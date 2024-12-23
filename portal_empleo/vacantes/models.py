from django.db import models
from django.core.exceptions import ValidationError
import uuid

def generate_unique_codigo():
    """Genera un código de vacante único de la forma COD-XXXXXXXX."""
    return f'COD-{uuid.uuid4().hex[:8].upper()}'


class Vacante(models.Model):
    # Datos obligatorios
    codigo_vacante = models.CharField(
        max_length=50, 
        unique=True, 
        default=generate_unique_codigo
    )
    cargo = models.CharField(max_length=100)
    area = models.CharField(
        max_length=100, 
        choices=[
            ('Sin asignar', 'Sin asignar'),
            ('Administración', 'Administración'),
            ('Finanzas', 'Finanzas'),
            ('Tecnología', 'Tecnología'),
            ('Recursos Humanos', 'Recursos Humanos'),
            ('Ventas', 'Ventas'),
        ], 
        default='Sin asignar'
    )
    numero_puestos = models.IntegerField(
        null=True, 
        blank=True, 
        default=1  # ✅ Se asigna 1 por defecto, ya que 0 no tendría sentido.
    )

    modalidad_trabajo = models.CharField(
        max_length=50, 
        choices=[
            ('Presencial', 'Presencial'),
            ('Remoto', 'Remoto'),
            ('Híbrido', 'Híbrido'),
        ]
    )
    tipo_contrato = models.CharField(
        max_length=50, 
        choices=[
            ('Indefinido', 'Indefinido'),
            ('Temporal', 'Temporal'),
            ('Prácticas', 'Prácticas'),
            ('Freelance', 'Freelance'),
        ]
    )
    jornada_trabajo = models.CharField(
        max_length=50, 
        choices=[
            ('Tiempo completo', 'Tiempo completo'),
            ('Medio tiempo', 'Medio tiempo'),
            ('Por horas', 'Por horas'),
        ]
    )
    descripcion_vacante = models.TextField(max_length=6000)
    tiempo_experiencia = models.CharField(
        max_length=50, 
        choices=[
            ('Sin experiencia', 'Sin experiencia'),
            ('1 año', '1 año'),
            ('2 años', '2 años'),
            ('3 años o más', '3 años o más'),
        ]
    )
    nivel_estudios = models.CharField(
        max_length=50, 
        choices=[
            ('Secundaria', 'Secundaria'),
            ('Técnico', 'Técnico'),
            ('Tecnólogo', 'Tecnólogo'),
            ('Profesional', 'Profesional'),
            ('Postgrado', 'Postgrado'),
        ]
    )
    departamento = models.CharField(
        max_length=100, 
        choices=[
            ('Sin asignar', 'Sin asignar'),
            ('Antioquia', 'Antioquia'),
            ('Bogotá', 'Bogotá'),
            ('Valle del Cauca', 'Valle del Cauca'),
            ('Cundinamarca', 'Cundinamarca'),
        ], 
        default='Sin asignar'
    )
    ciudad = models.CharField(
        max_length=100, 
        choices=[
            ('Medellín', 'Medellín'),
            ('Bogotá', 'Bogotá'),
            ('Cali', 'Cali'),
            ('Barranquilla', 'Barranquilla'),
        ]
    )
    rango_salarial = models.CharField(
        max_length=50, 
        blank=True, 
        null=True
    )
    fecha_publicacion = models.DateField(auto_now_add=True)
    empresa_usuaria = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Vacante"
        verbose_name_plural = "Vacantes"

    def __str__(self):
        """Representación legible del objeto."""
        return f"[{self.codigo_vacante}] {self.cargo} ({self.area})"


