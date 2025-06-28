from django import forms 
from django.forms import fields 
from .models import Categoria,  Producto, Cliente, CabeceraVenta,Tipo
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
        fields = ['apellido', 'nombre', 'direccion', 'sexo','ruc_dni']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['apellido'].widget.attrs.update({'placeholder': 'Apellido'})
        self.fields['nombre'].widget.attrs.update({'placeholder': 'Nombre'})
        self.fields['direccion'].widget.attrs.update({'placeholder': 'Dirección'})
        self.fields['sexo'].choices = [
            ('M', 'Masculino'),
            ('F', 'Femenino')
        ]
        
        

class CabeceraVentaForm(forms.ModelForm):
    class Meta:
        model = CabeceraVenta
        fields = ['fecha_venta', 'tipo', 'nrodoc', 'idcliente']
        widgets = {
            'fecha_venta': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control', 'onchange': 'mostrarTipo()'}),
            'nrodoc': forms.TextInput(attrs={'class': 'form-control'}),
            'idcliente': forms.Select(attrs={
                'class': 'form-control selectpicker',
                'data-live-search': 'true',
                'onchange': 'mostrarCliente()'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['idcliente'].queryset = Cliente.objects.filter(estado=True)
        self.fields['tipo'].queryset = Tipo.objects.all()