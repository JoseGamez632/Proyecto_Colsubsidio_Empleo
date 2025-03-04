from django.db import models
from django.core.exceptions import ValidationError
import uuid
from datetime import date
from django.contrib.auth.models import User  # Importa el modelo User
from django.utils.timezone import now



def generate_unique_codigo():
    """Genera un código de vacante único de la forma COD-XXXXXXXX."""
    return f'COD-{uuid.uuid4().hex[:8].upper()}'

# Modelos para departamentos y ciudades

class Departamento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    class Meta:
        ordering = ["nombre"]  # Ordenar siempre por nombre alfabéticamente

    def __str__(self):
        return self.nombre

class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="ciudades")
    
    class Meta:
        ordering = ["nombre"]  # Ordenar siempre por nombre alfabéticamente

    def __str__(self):
        return self.nombre

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
        null=True, 
        blank=True, 
        choices=[
            ('Administración', 'Administración'),
            ('Finanzas', 'Finanzas'),
            ('Tecnología', 'Tecnología'),
            ('Recursos Humanos', 'Recursos Humanos'),
            ('Ventas', 'Ventas'),
        ]
    )
    numero_puestos = models.IntegerField(
        null=True, 
        blank=True, 
        default=1  
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
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True, blank=True)
    rango_salarial = models.IntegerField(null=True, blank=True)
    fecha_publicacion = models.DateField(auto_now_add=True)
    empresa_usuaria = models.CharField(max_length=100)
    candidatos_registrados = models.ManyToManyField('RegistroCandidato', related_name='vacantes', blank=True)
    estado = models.BooleanField(default=True)  # True para activa, False para inactiva

    # Datos de auditoría
    usuario_publicador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='vacantes_publicadas')
    usuario_actualizador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='vacantes_actualizadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Solo se guarda al crear
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)  # Se actualizará manualmente

    class Meta:
        verbose_name = "Vacante"
        verbose_name_plural = "Vacantes"

    def save(self, *args, **kwargs):
        """ Sobrescribir save para actualizar fecha_actualizacion solo si hubo cambios """
        if self.pk:  # Si ya existe en la base de datos
            vacante_anterior = Vacante.objects.get(pk=self.pk)
            if any([
                getattr(vacante_anterior, field) != getattr(self, field)
                for field in [
                    'cargo', 'area', 'numero_puestos', 'modalidad_trabajo',
                    'tipo_contrato', 'jornada_trabajo', 'descripcion_vacante',
                    'tiempo_experiencia', 'nivel_estudios', 'departamento',
                    'ciudad', 'rango_salarial', 'empresa_usuaria', 'estado'
                ]
            ]):
                self.fecha_actualizacion = now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.codigo_vacante}] {self.cargo} - Publicado por {self.usuario_publicador.username if self.usuario_publicador else 'Desconocido'}"





# ✅ Registro de candidatos

def validar_aspiracion_salarial(value):
    if value < 1000000:
        raise ValidationError("La aspiración salarial debe ser mayor a 1,000,000.")

class RegistroCandidato(models.Model):
    # Opciones para los campos
    SEX_CHOICES = [
        ('Mujer', 'Mujer'),
        ('Hombre', 'Hombre'),
        ('Intersexual', 'Intersexual'),
    ]

    DOCUMENT_TYPE_CHOICES = [
        ('CEDULA DE CIUDADANIA', 'CEDULA DE CIUDADANIA'),
        ('PERMISO ESPECIAL DE PERMANENCIA', 'PERMISO ESPECIAL DE PERMANENCIA'),
        ('TARJETA DE IDENTIDAD', 'TARJETA DE IDENTIDAD'),
        ('DOCUMENTO NACIONAL DE IDENTIFICACION', 'DOCUMENTO NACIONAL DE IDENTIFICACION'),
        ('PASAPORTE', 'PASAPORTE'),
        ('CEDULA DE EXTRANJERIA', 'CEDULA DE EXTRANJERIA'),
    ]

    EDUCATION_LEVEL_CHOICES = [
        ('BASICA PRIMARIA', 'BASICA PRIMARIA'),
        ('BASICA SECUNDARIA', 'BASICA SECUNDARIA'),
        ('BACHILLER ACADEMICO', 'BACHILLER ACADEMICO'),
        ('ESTUDIANTE BACHILLER ACADEMICO', 'ESTUDIANTE BACHILLER ACADEMICO'),
        ('TECNICO LABORAL/PROFESIONAL', 'TECNICO LABORAL/PROFESIONAL'),
        ('ESTUDIANTE TECNICO LABORAL/PROFESIONAL', 'ESTUDIANTE TECNICO LABORAL/PROFESIONAL'),
        ('TECNOLOGO', 'TECNOLOGO'),
        ('ESTUDIANTE TECNOLOGO', 'ESTUDIANTE TECNOLOGO'),
        ('PROFESIONAL', 'PROFESIONAL'),
        ('ESTUDIANTE PROFESIONAL', 'ESTUDIANTE PROFESIONAL'),
        ('POSGRADO', 'POSGRADO'),
    ]

    SCHEDULE_CHOICES = [
        ('TIEMPO COMPLETO', 'TIEMPO COMPLETO'),
        ('MEDIO TIEMPO', 'MEDIO TIEMPO'),
        ('FINES DE SEMANA', 'FINES DE SEMANA'),
    ]

    DISABILITY_CHOICES = [
        ('SI', 'Sí'),
        ('NO', 'No'),
    ]

    SISE_CHOICES = [
        ('SI', 'Sí'),
        ('NO', 'No'),
    ]

    RECRUITER_CHOICES = [
        ('No conoce el nombre', 'No conoce el nombre'),
        ('Angel Andres Moyano Molano', 'Angel Andres Moyano Molano'),
        ('Diego Alejandro Parra Pinto', 'Diego Alejandro Parra Pinto'),
        ('Erika Julieth Cristancho Pérez', 'Erika Julieth Cristancho Pérez'),
    ]

    # Campos
    feria = models.CharField(max_length=100, blank=True, null=True)
    fecha_feria = models.DateField(default=date(2025, 1, 1), blank=True, null=True)
    sexo = models.CharField(max_length=16, choices=SEX_CHOICES)
    tipo_documento = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    numero_documento = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    numero_celular = models.CharField(max_length=15)
    correo_electronico = models.EmailField()
    fecha_nacimiento = models.DateField()
    formacion_academica = models.CharField(max_length=40, choices=EDUCATION_LEVEL_CHOICES)
    programa_academico = models.CharField(max_length=100)
    experiencia_laboral = models.TextField(blank=True, null=True)
    interes_ocupacional = models.TextField(blank=True, null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True, blank=True)
    candidato_discapacidad = models.CharField(max_length=2, choices=DISABILITY_CHOICES)
    tipo_discapacidad = models.CharField(max_length=100, blank=True, null=True)
    horario_interesado = models.CharField(max_length=20, choices=SCHEDULE_CHOICES)

    # Aspiración salarial como número entero con validación
    aspiracion_salarial = models.IntegerField(
        validators=[validar_aspiracion_salarial],
        help_text="Ingrese un valor numérico mayor a 1,000,000."
    )

    registrado_en_sise = models.CharField(max_length=2, choices=SISE_CHOICES)
    tecnico_seleccion = models.CharField(max_length=40, choices=RECRUITER_CHOICES, blank=True, null=True)
    vacantes_disponibles = models.ManyToManyField("Vacante", related_name="candidatos", blank=True)

# Campo para comentarios del reclutador
    comentarios = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Registro de Candidato"
        verbose_name_plural = "Registros de Candidatos"

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.tipo_documento}: {self.numero_documento}"


class EstadoAplicacion(models.Model):
    ESTADO_CHOICES = [
        ('No visto', 'No visto'),
        ('Visto', 'Visto'),
        ('Descartado', 'Descartado'),
    ]

    candidato = models.ForeignKey('RegistroCandidato', on_delete=models.CASCADE, related_name='aplicaciones')
    vacante = models.ForeignKey('Vacante', on_delete=models.CASCADE, related_name='aplicaciones')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='No visto')
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('candidato', 'vacante')

    def __str__(self):
        return f"{self.candidato.nombres} - {self.vacante.cargo} - {self.estado}"
