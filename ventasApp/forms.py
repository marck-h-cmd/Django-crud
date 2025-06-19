from django import forms 
from django.forms import fields 
from .models import Categoria,  Producto, Cliente
class CategoriaForm(forms.ModelForm):
 
    class Meta:
        model=Categoria
        fields=['descripcion'] 
        
        
        
class ProductoForm(forms.ModelForm):  
        class Meta:   
                model=Producto         
    
                fields=['descripcion','idcategoria','precio','stock']
        
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['idcategoria'].queryset = Categoria.objects.filter(estado=True)
                self.fields['idcategoria'].label = "Categoria"
                self.fields['idcategoria'].label_from_instance = lambda obj: f"{obj.descripcion}"
                self.fields['idcategoria'].empty_label = "-- Selecciona una categoría --"
                self.fields['idcategoria'].help_text = "Elige la categoría del producto"
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['apellido', 'nombre', 'direccion', 'sexo']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['apellido'].widget.attrs.update({'placeholder': 'Apellido'})
        self.fields['nombre'].widget.attrs.update({'placeholder': 'Nombre'})
        self.fields['direccion'].widget.attrs.update({'placeholder': 'Dirección'})
        self.fields['sexo'].choices = [
            ('M', 'Masculino'),
            ('F', 'Femenino')
        ]
        