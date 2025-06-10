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
            ('Administración y Gestión', 'Administración y Gestión'),
            ('Finanzas y Contabilidad', 'Finanzas y Contabilidad'),
            ('Tecnología e Informática', 'Tecnología e Informática'),
            ('Recursos Humanos', 'Recursos Humanos'),
            ('Ventas y Comercial', 'Ventas y Comercial'),
            ('Atención al Cliente y Servicios', 'Atención al Cliente y Servicios'),
            ('Marketing y Publicidad', 'Marketing y Publicidad'),
            ('Logística y Transporte', 'Logística y Transporte'),
            ('Logística y Bodega', 'Logística y Bodega'),
            ('Producción y Manufactura', 'Producción y Manufactura'),
            ('Ingeniería y Construcción', 'Ingeniería y Construcción'),
            ('Salud y Bienestar', 'Salud y Bienestar'),
            ('Educación y Formación', 'Educación y Formación'),
            ('Legal y Asesoría', 'Legal y Asesoría'),
            ('Hostelería y Turismo', 'Hostelería y Turismo'),
            ('Arte, Cultura y Entretenimiento', 'Arte, Cultura y Entretenimiento'),
            ('Medio Ambiente y Energía', 'Medio Ambiente y Energía'),
            ('Ciencia e Investigación', 'Ciencia e Investigación'),
            ('Seguridad y Defensa', 'Seguridad y Defensa'),
            ('Servicios Generales', 'Servicios Generales'),
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
            ('Fijo', 'Fijo'),
            ('Obra o Labor', 'Obra o Labor'),
            ('Prácticas', 'Prácticas'),
            ('Aprendizaje', 'Aprendizaje'),
            ('Prestación de Servicios', 'Prestación de Servicios'),
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
            ('Menos de 1 año', 'Menos de 1 año'),
            ('1 año', '1 año'),
            ('2 años', '2 años'),
            ('3 años o más', '3 años o más'),
        ]
    )
    nivel_estudios = models.CharField(
        max_length=50,
        choices=[
            ('No Requiere', 'No Requiere'),
            ('Primaria', 'Primaria'),
            ('Bachiller Básico (Hasta 9°)', 'Bachiller Básico (Hasta 9°)'),
            ('Bachiller', 'Bachiller'),
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
    estado = models.BooleanField(default=True) # True = Activa, False = Inactiva


    # Nuevo campo: Tipo Vacante
    tipo_vacante = models.CharField(
        max_length=20,
        choices=[
            ('Tradicional', 'Tradicional'),
            ('Convocatoria', 'Convocatoria'),
        ],
        default='Tradicional'
    )

    # Nuevo campo: Citación Convocatoria (opcional)
    citacion_convocatoria = models.TextField(
        max_length=3000,
        null=True,
        blank=True,
        help_text="Solo se diligencia si la vacante es de tipo Convocatoria"
    )

    # Datos de auditoría
    usuario_publicador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='vacantes_publicadas')
    usuario_actualizador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='vacantes_actualizadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Vacante"
        verbose_name_plural = "Vacantes"

    def save(self, *args, **kwargs):
        if self.pk:
            vacante_anterior = Vacante.objects.get(pk=self.pk)
            if any([
                getattr(vacante_anterior, field) != getattr(self, field)
                for field in [
                    'cargo', 'area', 'numero_puestos', 'modalidad_trabajo',
                    'tipo_contrato', 'jornada_trabajo', 'descripcion_vacante',
                    'tiempo_experiencia', 'nivel_estudios', 'departamento',
                    'ciudad', 'rango_salarial', 'empresa_usuaria', 'estado',
                    'tipo_vacante', 'citacion_convocatoria'
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
        ('Diego Alejandro Parra Pinto', 'Diego Alejandro Parra Pinto'),
        ('Jony Edilberto Chisaba Rojas', 'Jony Edilberto Chisaba Rojas'),
        ('Jose Luis Gamez Torres', 'Jose Luis Gamez Torres'),
        ('Jully Andrea Galindo Fonseca', 'Jully Andrea Galindo Fonseca'),
        ('Maria Alejandra Moreno Pedraza', 'Maria Alejandra Moreno Pedraza'),
        ('Sergio Daniel García Donado', 'Sergio Daniel García Donado'),
        ('Steven Alejandro Arevalo Benitez', 'Steven Alejandro Arevalo Benitez'),
        ('Victor De Jesus Fagua Cogollo', 'Victor De Jesus Fagua Cogollo'),
        ('Yennifer Alexandra Ruiz', 'Yennifer Alexandra Ruiz'),
        ('Erika Julieth Cristancho Pérez', 'Erika Julieth Cristancho Pérez'),
        ('Gabriela Alejandra Milanes Sierra', 'Gabriela Alejandra Milanes Sierra'),
        ('Rosa Milena Pinilla Aldana', 'Rosa Milena Pinilla Aldana'),
        ('Yesica Natalia Lemos Lemos', 'Yesica Natalia Lemos Lemos'),
    ]

    SALARY_CHOICES = [
        ('Menos de 1 SMMLV', 'Menos de 1 SMMLV'),
        ('1 a 2 SMMLV', '1 a 2 SMMLV'),
        ('2 a 4 SMMLV', '2 a 4 SMMLV'),
        ('4 a 6 SMMLV', '4 a 6 SMMLV'),
        ('6 a 9 SMMLV', '6 a 9 SMMLV'),
        ('9 a 12 SMMLV', '9 a 12 SMMLV'),
        ('12 a 15 SMMLV', '12 a 15 SMMLV'),
        ('15 a 19 SMMLV', '15 a 19 SMMLV'),
        ('20 SMMLV en adelante', '20 SMMLV en adelante'),
    ]

    # Nueva opción para tipo de feria
    TIPO_FERIA_CHOICES = [
        ('FERIA PROPIA', 'FERIA PROPIA'),
        ('FERIA INVITADO', 'FERIA INVITADO'),
        ('FERIA MOVIL', 'FERIA MOVIL'),
    ]

    # Campos
    feria = models.CharField(max_length=100, blank=True, null=True)
    fecha_feria = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # Nuevo campo tipo_feria
    tipo_feria = models.CharField(max_length=20, choices=TIPO_FERIA_CHOICES, blank=True, null=True)
    # Nuevos campos para FERIA MOVIL
    codigo_sise = models.CharField(max_length=50, blank=True, null=True)
    empresa_sise = models.CharField(max_length=100, blank=True, null=True)
    cargo_sise = models.CharField(max_length=100, blank=True, null=True)
    # Nuevo campo para interés en prácticas
    interes_practica = models.BooleanField(default=False, blank=True, null=True)
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
    semestre_grado = models.CharField(max_length=100, blank=True, null=True)

    # Aspiración salarial como campo de selección única
    aspiracion_salarial = models.CharField(
        max_length=50,
        choices=SALARY_CHOICES,
        help_text="Seleccione una opción de aspiración salarial.",
        blank=True
    )

    registrado_en_sise = models.CharField(max_length=2, choices=SISE_CHOICES, blank=True, null=True)
    tecnico_seleccion = models.CharField(max_length=40, choices=RECRUITER_CHOICES, blank=True, null=True)
    vacantes_disponibles = models.ManyToManyField("Vacante", related_name="candidatos", blank=True)

    
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
    
    
from django.db import models
from django.contrib.auth.models import User # Asegurate de tenerlo importado
from django.utils.timezone import now



class ComentarioCandidato(models.Model):
    """
    Modelo para almacenar comentarios de los reclutadores sobre un candidato.
    """
    candidato = models.ForeignKey('RegistroCandidato', on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    comentario = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']  # Ordena del más reciente al más antiguo

    def __str__(self):
        return f"Comentario de {self.usuario.username if self.usuario else 'Desconocido'} - {self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}"

