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
    vacantes = forms.ModelMultipleChoiceField(
        queryset=Vacante.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Vacantes disponibles",
        required=False  # Puede ser opcional
    )
    
    # Agregar campo de fecha con widget de calendario
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha de Nacimiento"
    )

    fecha_feria = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha de Feria"
    )

    # Campo para "Experiencia Laboral"
    experiencia_laboral = forms.JSONField(
        label="Experiencia Laboral",
        required=False,  # Puede ser opcional
        widget=forms.Textarea(attrs={'placeholder': 'Ingrese su experiencia en formato JSON'})
    )

    # Campo para "Interés Ocupacional"
    interes_ocupacional = forms.JSONField(
        label="Interés Ocupacional",
        required=False,  # Puede ser opcional
        widget=forms.Textarea(attrs={'placeholder': 'Ingrese su interés ocupacional en formato JSON'})
    )

    class Meta:
        model = RegistroCandidato
        fields = '__all__'

    def clean_experiencia_laboral(self):
        """
        Limpiar y convertir los datos de experiencia laboral en formato JSON
        """
        experiencia_laboral = self.cleaned_data.get('experiencia_laboral', [])
        # Verifica si los datos están en formato JSON adecuado
        if isinstance(experiencia_laboral, str):
            try:
                experiencia_laboral = json.loads(experiencia_laboral)
            except json.JSONDecodeError:
                raise forms.ValidationError("El formato de experiencia laboral no es válido.")
        return experiencia_laboral

    def clean_interes_ocupacional(self):
        """
        Limpiar y convertir los datos de interés ocupacional en formato JSON
        """
        interes_ocupacional = self.cleaned_data.get('interes_ocupacional', [])
        # Verifica si los datos están en formato JSON adecuado
        if isinstance(interes_ocupacional, str):
            try:
                interes_ocupacional = json.loads(interes_ocupacional)
            except json.JSONDecodeError:
                raise forms.ValidationError("El formato de interés ocupacional no es válido.")
        return interes_ocupacional
