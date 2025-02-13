from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import Vacante, Ciudad, Departamento, RegistroCandidato
from .forms import VacanteForm, RegistroCandidatoForm
from django.contrib.auth.decorators import login_required # Solicitar ligin para ejecutar funcion
from django.contrib.auth.decorators import permission_required # Solicita login para permisos especificos @permission_required('app_name.add_vacante')
import openpyxl
from django.db.models.functions import Lower
from django.db.models import Count, Q
import unicodedata
from django.db import migrations
from django.views.generic import TemplateView






# Mensaje de éxito

#Agregado por Jose



def normalizar_texto(texto):
    """
    Elimina los acentos y normaliza el texto a minúsculas.
    Si el texto es None, devuelve una cadena vacía.
    """
    if texto is None:
        return ""  # Devolver cadena vacía si el texto es None

    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).lower()
    

def lista_vacantes(request):
    # Obtener los filtros de la solicitud GET
    filtros = {
        'cargo': request.GET.get('cargo'),
        'area': request.GET.get('area'),
        'modalidad_trabajo': request.GET.get('modalidad_trabajo'),
        'tipo_contrato': request.GET.get('tipo_contrato'),
        'jornada_trabajo': request.GET.get('jornada_trabajo'),
        'tiempo_experiencia': request.GET.get('tiempo_experiencia'),
        'nivel_estudios': request.GET.get('nivel_estudios'),
        'departamento': request.GET.get('departamento'),
        'ciudad': request.GET.get('ciudad'),
        'rango_salarial': request.GET.get('rango_salarial'),
    }

    # Obtener el nombre de la ciudad si se ha seleccionado un ID en el filtro
    ciudad_nombre = None
    if filtros['ciudad']:  # Si el usuario seleccionó una ciudad
        ciudad_obj = Ciudad.objects.filter(id=filtros['ciudad']).first()
        if ciudad_obj:
            ciudad_nombre = ciudad_obj.nombre

    # Agregar ciudad_nombre a filtros para que esté disponible en el template
    filtros['ciudad_nombre'] = ciudad_nombre

    # Obtener todas las vacantes activas si el usuario no está autenticado
    vacantes = Vacante.objects.filter(estado=True) if not request.user.is_authenticated else Vacante.objects.all()

    # # Filtrar por cargo (ignorando tildes y mayúsculas/minúsculas)
    # if filtros['cargo']:
    #     palabras_clave = filtros['cargo'].split()
    #     consulta_cargo = Q()
    #     for palabra in palabras_clave:
    #         palabra_normalizada = normalizar_texto(palabra)
    #         consulta_cargo |= Q(cargo__icontains=palabra_normalizada)

    #     # Filtrar manualmente en Python porque SQLite no soporta unaccent
    #     vacantes = [v for v in vacantes if all(
    #         normalizar_texto(palabra) in normalizar_texto(v.cargo) for palabra in palabras_clave
    #     )]
    
    if filtros['cargo']:
        cargo_normalizado = normalizar_texto(filtros['cargo'])  # Normalizar la búsqueda

        # Filtrar todas las vacantes activas
        vacantes_filtradas = vacantes.filter(estado=True) if not request.user.is_authenticated else vacantes

        # Aplicar filtrado manual sin perder el queryset
        ids_vacantes = [
            v.id for v in vacantes_filtradas
            if cargo_normalizado in normalizar_texto(v.cargo)
        ]
        
        vacantes = vacantes.filter(id__in=ids_vacantes)  # Mantiene el QuerySet




    # Aplicar filtros restantes directamente en la consulta
    for campo, valor in filtros.items():
        if valor and campo not in ['cargo', 'ciudad_nombre']:  # Cargo ya se filtró manualmente
            vacantes = vacantes.filter(**{campo: valor})

    # Agregar el conteo de candidatos aplicados
    vacantes = vacantes.annotate(num_candidatos=Count('candidatos'))

    # Mantener el orden alfabético por cargo
    vacantes = sorted(vacantes, key=lambda v: v.cargo.lower())

    # Obtener opciones de los campos con choices
    form = VacanteForm()
    choices_context = {
        'area_choices': form.fields['area'].choices,
        'modalidad_trabajo_choices': form.fields['modalidad_trabajo'].choices,
        'tipo_contrato_choices': form.fields['tipo_contrato'].choices,
        'jornada_trabajo_choices': form.fields['jornada_trabajo'].choices,
        'tiempo_experiencia_choices': form.fields['tiempo_experiencia'].choices,
        'nivel_estudios_choices': form.fields['nivel_estudios'].choices,
        'departamento_choices': form.fields['departamento'].choices,
        'ciudad_choices': form.fields['ciudad'].choices,
    }

    # Renderizar la plantilla con las vacantes filtradas y ordenadas
    return render(request, "vacantes/lista.html", {
        "vacantes": vacantes,
        "filtros": filtros,
        **choices_context  # Pasar los choices al template
    })


    # return render(request, 'vacantes/lista.html', contexto)

# para cambiar el estado de la vacante
def cambiar_estado_vacante(request, vacante_id):
    vacante = get_object_or_404(Vacante, id=vacante_id)
    vacante.estado = not vacante.estado
    vacante.save()
    return redirect('lista_vacantes')


# Create your views here.



# Archivo de migración: 0005_clean_numero_puestos.py



def limpiar_numero_puestos(apps, schema_editor):
    Vacante = apps.get_model('proyecto_negocio', 'Vacante')
    # Convertir los valores de 'n/a' a 0
    Vacante.objects.filter(numero_puestos='n/a').update(numero_puestos=0)
    # Convertir los valores no numéricos en 0
    for vacante in Vacante.objects.all():
        try:
            vacante.numero_puestos = int(vacante.numero_puestos)
            vacante.save()
        except ValueError:
            vacante.numero_puestos = 0
            vacante.save()

class Migration(migrations.Migration):

    dependencies = [
        ('proyecto_negocio', '0004_remove_vacante_empresa_remove_vacante_estudios_and_more'),
    ]

    operations = [
        migrations.RunPython(limpiar_numero_puestos),
    ]


#Agregado por Jose
@login_required
def eliminar_vacante(request, id):
    """Elimina la vacante con el ID proporcionado."""
    if request.method == 'POST':
        vacante = get_object_or_404(Vacante, id=id)
        vacante.delete()
        messages.success(request, 'La vacante ha sido eliminada correctamente.')
    # Cambia 'nombre_de_tu_vista_principal' por la vista principal, por ejemplo, 'lista_vacantes'
    return redirect('lista_vacantes')

@login_required
def agregar_vacante(request):
    if request.method == 'POST':
        form = VacanteForm(request.POST, user=request.user)  # Pasamos el usuario
        if form.is_valid():
            vacante = form.save(commit=False)  # No guardamos aún en la BD
            vacante.usuario_publicador = request.user  # Asignamos el usuario
            vacante.save()  # Ahora sí guardamos
            return redirect('lista_vacantes')  # Redirige a la lista de vacantes
    else:
        form = VacanteForm(user=request.user)  # Pasamos el usuario también en GET

    return render(request, 'vacantes/agregar_vacante.html', {'form': form})

def inicio(request):
    return render(request, "paginas/inicio.html")

@login_required
def editar_vacante(request, id):
    vacante = get_object_or_404(Vacante, id=id)
    if request.method == 'POST':
        form = VacanteForm(request.POST, instance=vacante)
        if form.is_valid():
            form.save()
            return redirect('lista_vacantes')
    else:
        form = VacanteForm(instance=vacante)
    return render(request, 'vacantes/editar_vacante.html', {'form': form, 'vacante': vacante})


#Registro de candidatos (modificado)


def registro_candidato_view(request):
    selected_vacantes = request.GET.get('selected_vacantes', '').split(',')
    if request.method == "POST":
        form = RegistroCandidatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')  # Redirigir a una página de éxito
    else:
        form = RegistroCandidatoForm()

    return render(request, 'registro_candidato.html', {'form': form, 'selected_vacantes': selected_vacantes})



# def registro_candidato_view(request):
#     selected_vacantes_ids = request.GET.get('selected_vacantes', '').split(',')
#     selected_vacantes = Vacante.objects.filter(id__in=selected_vacantes_ids)

#     if request.method == "POST":
#         form = RegistroCandidatoForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('inicio')  # Redirigir a una página de éxito
#     else:
#         form = RegistroCandidatoForm()

#     return render(request, 'registro_candidato.html', {
#         'form': form,
#         'selected_vacantes': selected_vacantes
#     })





#Descargar Excel

def descargar_excel(request):
    # Crear un libro de trabajo y una hoja de trabajo
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Candidatos Registrados"

    # Escribir los encabezados de las columnas
    headers = [
        'Feria', 'Fecha de Feria', 'Sexo', 'Tipo de Documento', 'Número de Documento', 'Nombres', 
        'Apellidos', 'Número de Celular', 'Correo Electrónico', 'Fecha de Nacimiento', 'Formación Académica', 
        'Programa Académico', 'Experiencia Laboral', 'Interés Ocupacional', 'Localidad/Municipio', 
        'Candidato con Discapacidad', 'Tipo de Discapacidad', 'Horario Interesado', 'Aspiración Salarial', 
        'Registrado en SISE', 'Técnico de Selección', 'Vacantes Disponibles'
    ]
    ws.append(headers)

    # Obtener todos los candidatos registrados de la base de datos
    candidatos = RegistroCandidato.objects.all()

    # Mapeo de las opciones para hacer más legible la salida en Excel
    SEX_CHOICES = dict(RegistroCandidato.SEX_CHOICES)
    DOCUMENT_TYPE_CHOICES = dict(RegistroCandidato.DOCUMENT_TYPE_CHOICES)
    EDUCATION_LEVEL_CHOICES = dict(RegistroCandidato.EDUCATION_LEVEL_CHOICES)
    SCHEDULE_CHOICES = dict(RegistroCandidato.SCHEDULE_CHOICES)
    SALARY_CHOICES = dict(RegistroCandidato.SALARY_CHOICES)
    DISABILITY_CHOICES = dict(RegistroCandidato.DISABILITY_CHOICES)
    SISE_CHOICES = dict(RegistroCandidato.SISE_CHOICES)
    RECRUITER_CHOICES = dict(RegistroCandidato.RECRUITER_CHOICES)

    # Escribir los datos de cada candidato en las filas
    for candidato in candidatos:
        vacantes_disponibles = candidato.vacantes_disponibles.all()  # Relación ManyToMany, obtenemos las vacantes
        vacantes_str = ', '.join([vacante.codigo_vacante for vacante in vacantes_disponibles]) if vacantes_disponibles else 'N/A'

        # Agregar la fila con todos los datos
        row = [
            candidato.feria,
            candidato.fecha_feria,
            SEX_CHOICES.get(candidato.sexo, candidato.sexo),
            DOCUMENT_TYPE_CHOICES.get(candidato.tipo_documento, candidato.tipo_documento),
            candidato.numero_documento,
            candidato.nombres,
            candidato.apellidos,
            candidato.numero_celular,
            candidato.correo_electronico,
            candidato.fecha_nacimiento,
            EDUCATION_LEVEL_CHOICES.get(candidato.formacion_academica, candidato.formacion_academica),
            candidato.programa_academico,
            str(candidato.experiencia_laboral),  # Convertir el JSON a cadena para guardarlo
            str(candidato.interes_ocupacional),  # Convertir el JSON a cadena para guardarlo
            candidato.localidad_municipio,
            DISABILITY_CHOICES.get(candidato.candidato_discapacidad, candidato.candidato_discapacidad),
            candidato.tipo_discapacidad or 'N/A',  # Si no tiene tipo de discapacidad, colocar "N/A"
            SCHEDULE_CHOICES.get(candidato.horario_interesado, candidato.horario_interesado),
            SALARY_CHOICES.get(candidato.aspiracion_salarial, candidato.aspiracion_salarial),
            SISE_CHOICES.get(candidato.registrado_en_sise, candidato.registrado_en_sise),
            RECRUITER_CHOICES.get(candidato.tecnico_seleccion, candidato.tecnico_seleccion),
            vacantes_str  # Vacantes disponibles
        ]
        ws.append(row)

    # Crear una respuesta HTTP con el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=candidatos_registrados.xlsx'
    wb.save(response)

    return response



def lista_candidatos(request, id):
    # Obtener la vacante específica
    vacante = get_object_or_404(Vacante, id=id)
    
    # Obtener la lista de candidatos relacionados con esta vacante
    candidatos = vacante.candidatos.all()  # Asumiendo que tienes una relación en el modelo

    # Renderizar la información en el template
    return render(request, 'vacantes/lista_candidatos.html', {'vacante': vacante, 'candidatos': candidatos})


def lista_registros(request):
    query = request.GET.get('q', '')  # Captura el término de búsqueda
    registros = RegistroCandidato.objects.all()

    if query:
        # Ignorar tildes y hacer búsquedas insensibles a mayúsculas
        registros = registros.annotate(
            nombres_lower=Lower('nombres'),
            apellidos_lower=Lower('apellidos'),
            documento_lower=Lower('numero_documento')
        ).filter(
            Q(nombres_lower__icontains=query) |
            Q(apellidos_lower__icontains=query) |
            Q(documento_lower__icontains=query)
        )

    context = {
        'registros': registros,
        'query': query
    }
    return render(request, 'lista_registros.html', context)

def editar_registro(request, pk):
    registro = get_object_or_404(RegistroCandidato, pk=pk)
    
    if request.method == 'POST':
        form = RegistroCandidatoForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            return redirect('lista_registros')
    else:
        form = RegistroCandidatoForm(instance=registro)
        # Formatear las fechas para el input type="date"
        if registro.fecha_nacimiento:
            form.fields['fecha_nacimiento'].initial = registro.fecha_nacimiento.strftime('%Y-%m-%d')
        if registro.fecha_feria:
            form.fields['fecha_feria'].initial = registro.fecha_feria.strftime('%Y-%m-%d')
        
    context = {
        'form': form,
        'selected_vacantes': registro.vacantes_disponibles.all(),
        'is_edit': True
    }
    return render(request, 'registro_candidato.html', context)

# para cargar ciudades por departamento

def cargar_ciudades(request):
    departamento_id = request.GET.get("departamento_id")
    ciudades = Ciudad.objects.filter(departamento_id=departamento_id).values("id", "nombre")
    return JsonResponse(list(ciudades), safe=False)


#def candidatos_por_vacante(request, vacante_id):
#    vacante = get_object_or_404(Vacante, id=vacante_id)
#    candidatos = vacante.candidatos.all()
#    return render(request, 'candidatos_por_vacante.html', {'vacante': vacante, 'candidatos': candidatos})


class RegistrationGuideView(TemplateView):
    template_name = 'registration/guide.html'
    
    