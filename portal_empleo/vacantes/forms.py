from django import forms
from .models import Vacante, RegistroCandidato
import json
from django.forms import modelformset_factory


#Agregado por Jose

class VacanteForm(forms.ModelForm):
    class Meta:
        model = Vacante
        fields = '__all__'  # O especifica los campos que quieres mostrar en el formulario

# Registro de candidatos

class RegistroCandidatoForm(forms.ModelForm):
    vacantes_disponibles = forms.ModelMultipleChoiceField(
        queryset=Vacante.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control select2',  # Clase personalizada para Select2
            'multiple': 'multiple'  # Habilita selección múltiple
        }),
        label="Vacantes disponibles",
        required=False
    )


    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha de Nacimiento"
    )

    fecha_feria = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha de Feria",
        required=False
    )

    experiencia_laboral = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describa su experiencia laboral'}),
        label="Experiencia Laboral",
        required=False
    )

    interes_ocupacional = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describa su interés ocupacional'}),
        label="Interés Ocupacional",
        required=False
    )
    

    class Meta:
        model = RegistroCandidato
        fields = '__all__'

# def clean_vacantes_disponibles(self):
#     vacantes = self.cleaned_data.get('vacantes_disponibles', [])
#     return ','.join(vacantes)  # Guarda como una lista separada por comas


