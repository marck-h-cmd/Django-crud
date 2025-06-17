from django.db import models

# Create your models here.

class Categoria(models.Model):
 idcategoria=models.IntegerField(primary_key=True,)
 descripcion=models.CharField(max_length=30)
 estado=models.BooleanField()