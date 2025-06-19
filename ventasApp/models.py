from django.db import models

# Create your models here.

class Categoria(models.Model):
    idcategoria = models.AutoField(primary_key=True)
    descripcion=models.CharField(max_length=30)
    estado=models.BooleanField(default=True)
    
    
class Producto(models.Model): 
        idproducto=models.AutoField(primary_key=True)
        descripcion=models.CharField(max_length=50) 
        idcategoria=models.ForeignKey(Categoria,on_delete=models.CASCADE, db_column='idcategoria') 
        precio=models.FloatField()
        stock=models.IntegerField() 
        estado=models.BooleanField(default=True)  

class Cliente(models.Model):
    idcliente = models.AutoField(primary_key=True)
    apellido = models.CharField(max_length=80)
    nombre = models.CharField(max_length=80)
    direccion = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    estado = models.BooleanField(default=True)