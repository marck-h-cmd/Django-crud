from django.db import models

# Create your models here.

class Categoria(models.Model):
    idcategoria = models.AutoField(primary_key=True)
    descripcion=models.CharField(max_length=30)
    estado=models.BooleanField(default=True)
    

class Unidad(models.Model):
    idunidad = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

class Producto(models.Model): 
    idproducto = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    idcategoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='idcategoria') 
    idunidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, db_column='idunidad')
    precio = models.FloatField()
    stock = models.IntegerField()
    estado = models.BooleanField(default=True)

class Cliente(models.Model):
    idcliente = models.AutoField(primary_key=True)
    apellido = models.CharField(max_length=80)
    nombre = models.CharField(max_length=80)
    direccion = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    ruc_dni=models.CharField(max_length=11)
    estado = models.BooleanField(default=True)
    

from django.db import models

class Tipo(models.Model):
    idtipo= models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Tipo"
        verbose_name_plural = "Tipos"

    def __str__(self):
        return self.descripcion

class Parametro(models.Model):
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    numeracion = models.CharField(max_length=15)
    serie = models.CharField(max_length=3)

    class Meta:
        verbose_name = "Parámetro"
        verbose_name_plural = "Parámetros"

    def __str__(self):
        return f"{self.tipo.descripcion} - {self.serie}{self.numeracion}"

class CabeceraVenta(models.Model):
    idventa = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        db_column='idcliente',
        related_name='ventas'     
    )
    fecha_venta = models.DateField()
    tipo        = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    estado      = models.BooleanField(default=True)
    subtotal    = models.FloatField()
    igv         = models.FloatField()
    total       = models.FloatField()
    nrodoc      = models.CharField(max_length=12)

    class Meta:
        verbose_name = "CabeceraVenta"
        verbose_name_plural = "CabeceraVentas"

    def __str__(self):
        return f"Venta {self.idventa} - {self.nrodoc}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(CabeceraVenta, on_delete=models.CASCADE)
    idproducto = models.IntegerField()
    precio = models.FloatField()
    cantidad = models.FloatField()

    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Venta"

    def __str__(self):
        return f"Detalle {self.id} para Venta {self.venta.venta_id}"
    
    
    