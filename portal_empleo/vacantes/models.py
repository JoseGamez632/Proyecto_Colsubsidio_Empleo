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


# ✅ Registro de candidatos

class RegistroCandidato(models.Model):
    # Opciones para los campos
    SEX_CHOICES = [
        ('M', 'Mujer'),
        ('H', 'Hombre'),
        ('I', 'Intersexual'),
    ]

    DOCUMENT_TYPE_CHOICES = [
        ('CC', 'CEDULA DE CIUDADANIA'),
        ('PEP', 'PERMISO ESPECIAL DE PERMANENCIA'),
        ('TI', 'TARJETA DE IDENTIDAD'),
        ('DNI', 'DOCUMENTO NACIONAL DE IDENTIFICACION'),
        ('PAS', 'PASAPORTE'),
        ('CE', 'CEDULA DE EXTRANJERIA'),
    ]

    EDUCATION_LEVEL_CHOICES = [
        ('BP', 'BASICA PRIMARIA'),
        ('BS', 'BASICA SECUNDARIA'),
        ('BA', 'BACHILLER ACADEMICO'),
        ('EBA', 'ESTUDIANTE BACHILLER ACADEMICO'),
        ('TL', 'TECNICO LABORAL/PROFESIONAL'),
        ('ETL', 'ESTUDIANTE TECNICO LABORAL/PROFESIONAL'),
        ('T', 'TECNOLOGO'),
        ('ET', 'ESTUDIANTE TECNOLOGO'),
        ('P', 'PROFESIONAL'),
        ('EP', 'ESTUDIANTE PROFESIONAL'),
        ('PG', 'POSGRADO'),
    ]

    SCHEDULE_CHOICES = [
        ('FT', 'TIEMPO COMPLETO'),
        ('PT', 'MEDIO TIEMPO'),
        ('WE', 'FINES DE SEMANA'),
    ]

    SALARY_CHOICES = [
        ('<1', 'Menos de 1 SMMLV'),
        ('1-2', '1 a 2 SMMLV'),
        ('2-4', '2 a 4 SMMLV'),
        ('4-6', '4 a 6 SMMLV'),
        ('6-9', '6 a 9 SMMLV'),
        ('9-12', '9 a 12 SMMLV'),
        ('12-15', '12 a 15 SMMLV'),
        ('15-19', '15 a 19 SMMLV'),
        ('>20', '20 SMMLV en adelante'),
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
        ('NN', 'No conoce el nombre'),
        ('AAM', 'Angel Andres Moyano Molano'),
        ('DAP', 'Diego Alejandro Parra Pinto'),
        ('EJC', 'Erika Julieth Cristancho Pérez'),
        # Agrega el resto de nombres
    ]

    # Campos
    feria = models.CharField(max_length=100)
    fecha_feria = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEX_CHOICES)
    tipo_documento = models.CharField(max_length=3, choices=DOCUMENT_TYPE_CHOICES)
    numero_documento = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    numero_celular = models.CharField(max_length=15)
    correo_electronico = models.EmailField()
    fecha_nacimiento = models.DateField()
    formacion_academica = models.CharField(max_length=3, choices=EDUCATION_LEVEL_CHOICES)
    programa_academico = models.CharField(max_length=100)
    experiencia_laboral = models.TextField(blank=True, null=True)
    interes_ocupacional = models.TextField(blank=True, null=True)
    localidad_municipio = models.CharField(max_length=100)
    candidato_discapacidad = models.CharField(max_length=2, choices=DISABILITY_CHOICES)
    tipo_discapacidad = models.CharField(max_length=100, blank=True, null=True)
    horario_interesado = models.CharField(max_length=2, choices=SCHEDULE_CHOICES)
    aspiracion_salarial = models.CharField(max_length=5, choices=SALARY_CHOICES)
    registrado_en_sise = models.CharField(max_length=2, choices=SISE_CHOICES)
    tecnico_seleccion = models.CharField(max_length=3, choices=RECRUITER_CHOICES)
    vacantes_disponibles = models.TextField(blank=True, null=True)  # Almacena como texto

    class Meta:
        verbose_name = "Registro de Candidato"
        verbose_name_plural = "Registros de Candidatos"

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.tipo_documento}: {self.numero_documento}"
