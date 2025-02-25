from django import forms
from .models import Vacante, RegistroCandidato, Departamento, Ciudad
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
        exclude = ['usuario_publicador', 'usuario_actualizador', 'fecha_creacion', 'fecha_actualizacion']
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
            'departamento': forms.Select(attrs={'class': 'form-control', 'id': 'departamento-select'}),
            'ciudad': forms.Select(attrs={'class': 'form-control', 'id': 'ciudad-select'}),
            'rango_salarial': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa_usuaria': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Recibir el usuario como argumento
        super().__init__(*args, **kwargs)
        self.fields['departamento'].queryset = Departamento.objects.all()
        self.fields['ciudad'].queryset = Ciudad.objects.none()  # Inicialmente vacío

        if user and not self.instance.pk:
            self.instance.usuario_publicador = user  # Asignar usuario al crear

        # Si ya hay un departamento seleccionado (edición de formulario)
        if 'departamento' in self.data:
            try:
                departamento_id = int(self.data.get('departamento'))
                self.fields['ciudad'].queryset = Ciudad.objects.filter(departamento_id=departamento_id)
            except (ValueError, TypeError):
                pass  # En caso de error, dejar vacío
        elif self.instance.pk:
            # Si estamos editando una instancia existente
            self.fields['ciudad'].queryset = Ciudad.objects.filter(departamento_id=self.instance.departamento_id)
            self.fields['ciudad'].initial = self.instance.ciudad
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
    
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'departamento-select'}),
        required=False
    )

    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.none(),  # Inicialmente vacío
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'ciudad-select'}),
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['departamento'].queryset = Departamento.objects.all()
        self.fields['ciudad'].queryset = Ciudad.objects.none()  # Inicialmente vacío

        # Si se envió un departamento en el formulario
        if 'departamento' in self.data:
            try:
                departamento_id = int(self.data.get('departamento'))
                self.fields['ciudad'].queryset = Ciudad.objects.filter(departamento_id=departamento_id)
            except (ValueError, TypeError):
                pass  # Si hay un error, se deja vacío

        # Si estamos editando un candidato con un departamento ya asignado
        elif self.instance.pk:
            self.fields['ciudad'].queryset = Ciudad.objects.filter(departamento=self.instance.departamento)
            self.fields['ciudad'].initial = self.instance.ciudad

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = RegistroCandidato
        fields = '__all__'
        
        
#registro de ciudad y departamento
        

# def clean_vacantes_disponibles(self):
#     vacantes = self.cleaned_data.get('vacantes_disponibles', [])
#     return ','.join(vacantes)  # Guarda como una lista separada por comas


