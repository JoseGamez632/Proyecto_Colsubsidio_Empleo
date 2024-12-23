from django import forms
from .models import Vacante

#Agregado por Jose

class VacanteForm(forms.ModelForm):
    class Meta:
        model = Vacante
        fields = '__all__'  # O especifica los campos que quieres mostrar en el formulario
