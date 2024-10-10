from django.forms import ModelForm
from .models import Vehicle, Viaje
from django import forms
class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = ['marca','model','year','license_plate']
        
class ViajeForm(forms.ModelForm):
    class Meta:
        model = Viaje
        fields = ['origen', 'destino', 'fecha']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={
                'type': 'datetime-local',  # Esto permite seleccionar fecha y hora
            }),
        }
        
        
        
     
        
      