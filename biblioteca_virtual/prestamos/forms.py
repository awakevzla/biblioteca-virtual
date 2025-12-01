from django import forms
from .models import Prestamo
from usuarios.models import Usuario
from libros.models import Libro

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['usuario', 'libro']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'libro': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].queryset = Usuario.objects.filter(activo=True)
        self.fields['libro'].queryset = Libro.objects.filter(en_prestamo=False)