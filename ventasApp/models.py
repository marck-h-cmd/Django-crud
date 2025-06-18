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