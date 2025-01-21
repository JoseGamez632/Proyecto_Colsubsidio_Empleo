from django import forms
from .models import Vacante, RegistroCandidato
import json
from django.forms import modelformset_factory


#Agregado por Jose

from django import forms
from .models import Vacante

class VacanteForm(forms.ModelForm):
    class Meta:
        model = Vacante
        fields = [
            'cargo', 'area', 'numero_puestos', 'modalidad_trabajo',
            'tipo_contrato', 'jornada_trabajo', 'descripcion_vacante',
            'tiempo_experiencia', 'nivel_estudios', 'departamento',
            'ciudad', 'rango_salarial', 'empresa_usuaria'
        ]
        widgets = {
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.Select(attrs={'class': 'form-control'}),
            'numero_puestos': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'modalidad_trabajo': forms.Select(attrs={'class': 'form-control'}),
            'tipo_contrato': forms.Select(attrs={'class': 'form-control'}),
            'jornada_trabajo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion_vacante': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'tiempo_experiencia': forms.Select(attrs={'class': 'form-control'}),
            'nivel_estudios': forms.Select(attrs={'class': 'form-control'}),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
            'ciudad': forms.Select(attrs={'class': 'form-control'}),
            'rango_salarial': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa_usuaria': forms.TextInput(attrs={'class': 'form-control'}),
        }
# Registro de candidatos

class RegistroCandidatoForm(forms.ModelForm):
    vacantes_disponibles = forms.ModelMultipleChoiceField(
        queryset=Vacante.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control select2',
            'multiple': 'multiple'
        }),
        label="Vacantes disponibles",
        required=False
    )

    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        input_formats=['%Y-%m-%d']
    )
    
    fecha_feria = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        required=False,
        input_formats=['%Y-%m-%d']
    )

    experiencia_laboral = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Describa su experiencia laboral'
        }),
        label="Experiencia Laboral",
        required=False
    )

    interes_ocupacional = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Describa su interés ocupacional'
        }),
        label="Interés Ocupacional",
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = RegistroCandidato
        fields = '__all__'
# def clean_vacantes_disponibles(self):
#     vacantes = self.cleaned_data.get('vacantes_disponibles', [])
#     return ','.join(vacantes)  # Guarda como una lista separada por comas


