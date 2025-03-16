from django import forms
from .models import Vacante, RegistroCandidato, Departamento, Ciudad, ComentarioCandidato
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


# # class RegistroCandidatoForm(forms.ModelForm):
    
#     vacantes_disponibles = forms.ModelMultipleChoiceField(
#         queryset=Vacante.objects.all(),
#         widget=forms.SelectMultiple(attrs={
#             'class': 'form-control select2',
#             'multiple': 'multiple'
#         }),
#         label="Vacantes disponibles",
#         required=False
#     )

#     fecha_nacimiento = forms.DateField(
#         widget=forms.DateInput(attrs={
#             'type': 'date',
#             'class': 'form-control',
#             'id': 'fecha_nacimiento'
#         }),
#         input_formats=['%Y-%m-%d']
#     )
    
#     fecha_feria = forms.DateField(
#         widget=forms.DateInput(attrs={
#             'type': 'date',
#             'class': 'form-control'
#         }),
#         required=False,
#         input_formats=['%Y-%m-%d']
#     )

#     experiencia_laboral = forms.CharField(
#         widget=forms.Textarea(attrs={
#             'class': 'form-control',
#             'placeholder': 'Describa su experiencia laboral'
#         }),
#         label="Experiencia Laboral",
#         required=False
#     )

#     interes_ocupacional = forms.CharField(
#         widget=forms.Textarea(attrs={
#             'class': 'form-control',
#             'placeholder': 'Describa su interés ocupacional'
#         }),
#         label="Interés Ocupacional",
#         required=False
#     )
#     numero_celular = forms.CharField(
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'id': 'numero_celular',
#             'maxlength': '10',
#             'placeholder': 'Ingresa tu número de celular'
#         }),
#         label="Número de Celular",
#         required=True
#     )

    
#     aspiracion_salarial = forms.CharField(
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'id': 'aspiracion_salarial',
#             'placeholder': 'Ingresa tu aspiración salarial'
#         }),
#         label="Aspiración Salarial",
#         required=False
#     )
#     numero_documento = forms.CharField(
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'id': 'numero_documento',
#             'placeholder': 'Ingresa tu número de documento'
#         }),
#         label="Número de Documento",
#         required=True
#     )
    
#     departamento = forms.ModelChoiceField(
#         queryset=Departamento.objects.all(),
#         widget=forms.Select(attrs={'class': 'form-control', 'id': 'departamento-select'}),
#         required=False
#     )

#     ciudad = forms.ModelChoiceField(
#         queryset=Ciudad.objects.none(),  # Inicialmente vacío
#         widget=forms.Select(attrs={'class': 'form-control', 'id': 'ciudad-select'}),
#         required=False
#     )
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.fields['departamento'].queryset = Departamento.objects.all()
#         self.fields['ciudad'].queryset = Ciudad.objects.none()  # Inicialmente vacío

#         # Si se envió un departamento en el formulario
#         if 'departamento' in self.data:
#             try:
#                 departamento_id = int(self.data.get('departamento'))
#                 self.fields['ciudad'].queryset = Ciudad.objects.filter(departamento_id=departamento_id)
#             except (ValueError, TypeError):
#                 pass  # Si hay un error, se deja vacío

#         # Si estamos editando un candidato con un departamento ya asignado
#         elif self.instance.pk:
#             self.fields['ciudad'].queryset = Ciudad.objects.filter(departamento=self.instance.departamento)
#             self.fields['ciudad'].initial = self.instance.ciudad




#     def clean_numero_celular(self):
#         data = self.cleaned_data['numero_celular']
#         # Verificar que solo contenga números
#         if not data.isdigit():
#             raise forms.ValidationError("El número de celular solo debe contener números.")
        
#         # Verificar que tenga exactamente 10 dígitos
#         if len(data) != 10:
#             raise forms.ValidationError("El número de celular debe tener exactamente 10 cifras.")
        
#         return data

#     def clean_aspiracion_salarial(self):
#         data = self.cleaned_data['aspiracion_salarial']
#         # Remover las comas antes de guardar
#         return data.replace(',', '')
    
#     def clean_numero_documento(self):
#         data = self.cleaned_data['numero_documento']
#         # Verificar que solo contenga números
#         if not data.isdigit():
#             raise forms.ValidationError("El número de documento solo debe contener números.")
        
#         return data


#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             if not isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
#                 field.widget.attrs['class'] = 'form-control'

#     class Meta:
#         model = RegistroCandidato
#         fields = '__all__'


# # forms.py



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
            'class': 'form-control',
            'id': 'fecha_nacimiento'
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
    numero_celular = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'numero_celular',
            'maxlength': '10',
            'placeholder': 'Ingresa tu número de celular'
        }),
        label="Número de Celular",
        required=True
    )

    aspiracion_salarial = forms.ChoiceField(
        choices=RegistroCandidato.SALARY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control select2'
        }),
        label="Aspiración Salarial",
        required=False
    )
    numero_documento = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'numero_documento',
            'placeholder': 'Ingresa tu número de documento'
        }),
        label="Número de Documento",
        required=True
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

        for field in self.fields.values():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs['class'] = 'form-control'

    def clean_numero_celular(self):
        data = self.cleaned_data['numero_celular']
        # Verificar que solo contenga números
        if not data.isdigit():
            raise forms.ValidationError("El número de celular solo debe contener números.")
        
        # Verificar que tenga exactamente 10 dígitos
        if len(data) != 10:
            raise forms.ValidationError("El número de celular debe tener exactamente 10 cifras.")
        
        return data

    def clean_numero_documento(self):
        data = self.cleaned_data['numero_documento']
        # Verificar que solo contenga números
        if not data.isdigit():
            raise forms.ValidationError("El número de documento solo debe contener números.")
        
        return data

    class Meta:
        model = RegistroCandidato
        fields = '__all__'
        
        
class ComentarioCandidatoForm(forms.ModelForm):
    class Meta:
        model = ComentarioCandidato
        fields = ['comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Escribe un nuevo comentario...'}),
        }


# def clean_vacantes_disponibles(self):
#     vacantes = self.cleaned_data.get('vacantes_disponibles', [])
#     return ','.join(vacantes)  # Guarda como una lista separada por comas


