from django import forms 
from django.forms import fields 
from .models import Categoria,  Producto, Cliente, CabeceraVenta,Tipo, Unidad
class CategoriaForm(forms.ModelForm):
 
    class Meta:
        model=Categoria
        fields=['descripcion'] 
        
class UnidadForm(forms.ModelForm):
    class Meta:
        model = Unidad
        fields = ['descripcion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].label = "Descripción de la unidad"
        self.fields['descripcion'].help_text = "Ej: Kg, Litros, Unidades"       
        
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
        
        

from django import forms
from .models import CabeceraVenta, Cliente, Tipo

class CabeceraVentaForm(forms.ModelForm):

    tipo = forms.ModelChoiceField(
        queryset=Tipo.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'onchange': 'mostrarTipo()',
            'id': 'idtipo'
        }),
        empty_label="-- Seleccione Tipo --",
        label="Tipo de Comprobante"
    )
    class Meta:
        model = CabeceraVenta
        fields = ['fecha_venta', 'tipo', 'nrodoc', 'cliente']
        widgets = {
            'fecha_venta': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            
            'nrodoc': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_nrodoc'
            }),
            'cliente': forms.Select(attrs={
                'class': 'form-control selectpicker',
                'data-live-search': 'true',
                'onchange': 'mostrarCliente()',
                'id': 'idcliente'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        clientes_qs = Cliente.objects.filter(estado=True)
        cliente_choices = [
            (
                f"{c.idcliente}_{c.ruc_dni}_{c.direccion}",
                f"{c.apellido} {c.nombre}"
            )
            for c in clientes_qs
        ]
        qs = Cliente.objects.filter(estado=True)
        print("Clientes activos:", list(qs))      # <-- ¿Qué sale aquí en la terminal?
        
        self.fields['cliente'].queryset = clientes_qs  # ✅ Usamos el campo correcto
        self.fields['cliente'].widget = forms.Select(attrs={
            'class': 'form-control selectpicker',
            'data-live-search': 'true',
            'onchange': 'mostrarCliente()',  
            'id': 'idcliente'                 
        })

        



