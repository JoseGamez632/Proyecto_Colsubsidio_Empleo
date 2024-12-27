from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Vacante
from .forms import VacanteForm, RegistroCandidatoForm
from django.contrib.auth.decorators import login_required # Solicitar ligin para ejecutar funcion
from django.contrib.auth.decorators import permission_required # Solicita login para permisos especificos @permission_required('app_name.add_vacante')


# Mensaje de éxito

#Agregado por Jose

from django.db.models import Q
import unicodedata

def normalizar_texto(texto):
    """
    Elimina los acentos y normaliza el texto a minúsculas.
    """
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).lower()

def lista_vacantes(request):
    # Obtener los filtros de la solicitud GET
    cargo = request.GET.get('cargo')
    area = request.GET.get('area')
    modalidad_trabajo = request.GET.get('modalidad_trabajo')
    tipo_contrato = request.GET.get('tipo_contrato')
    jornada_trabajo = request.GET.get('jornada_trabajo')
    tiempo_experiencia = request.GET.get('tiempo_experiencia')
    nivel_estudios = request.GET.get('nivel_estudios')
    departamento = request.GET.get('departamento')
    ciudad = request.GET.get('ciudad')
    rango_salarial = request.GET.get('rango_salarial')

    # Obtener todas las vacantes
    vacantes = Vacante.objects.all()

    # Filtrar por cargo (ignorando tildes y mayúsculas/minúsculas)
    if cargo:
        palabras_clave = cargo.split()
        consulta_cargo = Q()
        for palabra in palabras_clave:
            palabra_normalizada = normalizar_texto(palabra)
            consulta_cargo |= Q(cargo__icontains=palabra_normalizada)

        # Filtrar manualmente en Python porque SQLite no soporta unaccent
        vacantes = [v for v in vacantes if all(
            normalizar_texto(palabra) in normalizar_texto(v.cargo) for palabra in palabras_clave
        )]

    if area:
        vacantes = vacantes.filter(area=area)
    if modalidad_trabajo:
        vacantes = vacantes.filter(modalidad_trabajo=modalidad_trabajo)
    if tipo_contrato:
        vacantes = vacantes.filter(tipo_contrato=tipo_contrato)
    if jornada_trabajo:
        vacantes = vacantes.filter(jornada_trabajo=jornada_trabajo)
    if tiempo_experiencia:
        vacantes = vacantes.filter(tiempo_experiencia=tiempo_experiencia)
    if nivel_estudios:
        vacantes = vacantes.filter(nivel_estudios=nivel_estudios)
    if departamento:
        vacantes = vacantes.filter(departamento=departamento)
    if ciudad:
        vacantes = vacantes.filter(ciudad=ciudad)
    if rango_salarial:
        vacantes = vacantes.filter(rango_salarial=rango_salarial)

    # Renderizar la plantilla con las vacantes filtradas y los filtros aplicados
    contexto = {
        'vacantes': vacantes,
        'filtros': {
            'cargo': cargo,
            'area': area,
            'modalidad_trabajo': modalidad_trabajo,
            'tipo_contrato': tipo_contrato,
            'jornada_trabajo': jornada_trabajo,
            'tiempo_experiencia': tiempo_experiencia,
            'nivel_estudios': nivel_estudios,
            'departamento': departamento,
            'ciudad': ciudad,
            'rango_salarial': rango_salarial,
        }
    }

    return render(request, 'vacantes/lista.html', contexto)


# Create your views here.

# Archivo de migración: 0005_clean_numero_puestos.py

from django.db import migrations

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
        form = VacanteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_vacantes')  # Redirige a la lista de vacantes
    else:
        form = VacanteForm()
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


#Registro de candidatos

def registro_candidato_view(request):
    if request.method == 'POST':
        form = RegistroCandidatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('candidato_exito')  # Redirige a una página de éxito
    else:
        form = RegistroCandidatoForm()
    
    return render(request, 'registro_candidato.html', {'form': form})
