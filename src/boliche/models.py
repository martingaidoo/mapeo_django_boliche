from django.db import models

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    marca = models.CharField(max_length=255, blank=True, null=True)

class Barra(models.Model):
    numeroBarra = models.IntegerField()
    ubicacion = models.CharField(max_length=255)

class Consumicion(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

class Venta(models.Model):
    codigo = models.IntegerField()
    fecha = models.DateField()
    hora = models.TimeField()
    barra = models.ForeignKey(Barra, on_delete=models.CASCADE)

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    consumicion = models.ForeignKey(Consumicion, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

class DetalleConsumicion(models.Model):
    consumicion = models.ForeignKey(Consumicion, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidadLitros = models.DecimalField(max_digits=10, decimal_places=2)
