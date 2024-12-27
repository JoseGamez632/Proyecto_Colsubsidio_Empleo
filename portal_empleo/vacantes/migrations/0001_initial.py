# Generated by Django 5.1.4 on 2024-12-27 17:41

import vacantes.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RegistroCandidato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feria', models.CharField(max_length=100)),
                ('fecha_feria', models.DateField()),
                ('sexo', models.CharField(choices=[('M', 'Mujer'), ('H', 'Hombre'), ('I', 'Intersexual')], max_length=1)),
                ('tipo_documento', models.CharField(choices=[('CC', 'CEDULA DE CIUDADANIA'), ('PEP', 'PERMISO ESPECIAL DE PERMANENCIA'), ('TI', 'TARJETA DE IDENTIDAD'), ('DNI', 'DOCUMENTO NACIONAL DE IDENTIFICACION'), ('PAS', 'PASAPORTE'), ('CE', 'CEDULA DE EXTRANJERIA')], max_length=3)),
                ('numero_documento', models.CharField(max_length=20, unique=True)),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('numero_celular', models.CharField(max_length=15)),
                ('correo_electronico', models.EmailField(max_length=254)),
                ('fecha_nacimiento', models.DateField()),
                ('formacion_academica', models.CharField(choices=[('BP', 'BASICA PRIMARIA'), ('BS', 'BASICA SECUNDARIA'), ('BA', 'BACHILLER ACADEMICO'), ('EBA', 'ESTUDIANTE BACHILLER ACADEMICO'), ('TL', 'TECNICO LABORAL/PROFESIONAL'), ('ETL', 'ESTUDIANTE TECNICO LABORAL/PROFESIONAL'), ('T', 'TECNOLOGO'), ('ET', 'ESTUDIANTE TECNOLOGO'), ('P', 'PROFESIONAL'), ('EP', 'ESTUDIANTE PROFESIONAL'), ('PG', 'POSGRADO')], max_length=3)),
                ('programa_academico', models.CharField(max_length=100)),
                ('experiencia_laboral', models.JSONField()),
                ('interes_ocupacional', models.JSONField()),
                ('localidad_municipio', models.CharField(max_length=100)),
                ('candidato_discapacidad', models.CharField(choices=[('SI', 'Sí'), ('NO', 'No')], max_length=2)),
                ('tipo_discapacidad', models.CharField(blank=True, max_length=100, null=True)),
                ('horario_interesado', models.CharField(choices=[('FT', 'TIEMPO COMPLETO'), ('PT', 'MEDIO TIEMPO'), ('WE', 'FINES DE SEMANA')], max_length=2)),
                ('aspiracion_salarial', models.CharField(choices=[('<1', 'Menos de 1 SMMLV'), ('1-2', '1 a 2 SMMLV'), ('2-4', '2 a 4 SMMLV'), ('4-6', '4 a 6 SMMLV'), ('6-9', '6 a 9 SMMLV'), ('9-12', '9 a 12 SMMLV'), ('12-15', '12 a 15 SMMLV'), ('15-19', '15 a 19 SMMLV'), ('>20', '20 SMMLV en adelante')], max_length=5)),
                ('registrado_en_sise', models.CharField(choices=[('SI', 'Sí'), ('NO', 'No')], max_length=2)),
                ('tecnico_seleccion', models.CharField(choices=[('NN', 'No conoce el nombre'), ('AAM', 'Angel Andres Moyano Molano'), ('DAP', 'Diego Alejandro Parra Pinto'), ('EJC', 'Erika Julieth Cristancho Pérez')], max_length=3)),
                ('vacantes', models.JSONField()),
            ],
            options={
                'verbose_name': 'Registro de Candidato',
                'verbose_name_plural': 'Registros de Candidatos',
            },
        ),
        migrations.CreateModel(
            name='Vacante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_vacante', models.CharField(default=vacantes.models.generate_unique_codigo, max_length=50, unique=True)),
                ('cargo', models.CharField(max_length=100)),
                ('area', models.CharField(choices=[('Sin asignar', 'Sin asignar'), ('Administración', 'Administración'), ('Finanzas', 'Finanzas'), ('Tecnología', 'Tecnología'), ('Recursos Humanos', 'Recursos Humanos'), ('Ventas', 'Ventas')], default='Sin asignar', max_length=100)),
                ('numero_puestos', models.IntegerField(blank=True, default=1, null=True)),
                ('modalidad_trabajo', models.CharField(choices=[('Presencial', 'Presencial'), ('Remoto', 'Remoto'), ('Híbrido', 'Híbrido')], max_length=50)),
                ('tipo_contrato', models.CharField(choices=[('Indefinido', 'Indefinido'), ('Temporal', 'Temporal'), ('Prácticas', 'Prácticas'), ('Freelance', 'Freelance')], max_length=50)),
                ('jornada_trabajo', models.CharField(choices=[('Tiempo completo', 'Tiempo completo'), ('Medio tiempo', 'Medio tiempo'), ('Por horas', 'Por horas')], max_length=50)),
                ('descripcion_vacante', models.TextField(max_length=6000)),
                ('tiempo_experiencia', models.CharField(choices=[('Sin experiencia', 'Sin experiencia'), ('1 año', '1 año'), ('2 años', '2 años'), ('3 años o más', '3 años o más')], max_length=50)),
                ('nivel_estudios', models.CharField(choices=[('Secundaria', 'Secundaria'), ('Técnico', 'Técnico'), ('Tecnólogo', 'Tecnólogo'), ('Profesional', 'Profesional'), ('Postgrado', 'Postgrado')], max_length=50)),
                ('departamento', models.CharField(choices=[('Sin asignar', 'Sin asignar'), ('Antioquia', 'Antioquia'), ('Bogotá', 'Bogotá'), ('Valle del Cauca', 'Valle del Cauca'), ('Cundinamarca', 'Cundinamarca')], default='Sin asignar', max_length=100)),
                ('ciudad', models.CharField(choices=[('Medellín', 'Medellín'), ('Bogotá', 'Bogotá'), ('Cali', 'Cali'), ('Barranquilla', 'Barranquilla')], max_length=100)),
                ('rango_salarial', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha_publicacion', models.DateField(auto_now_add=True)),
                ('empresa_usuaria', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Vacante',
                'verbose_name_plural': 'Vacantes',
            },
        ),
    ]
