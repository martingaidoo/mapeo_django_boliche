from django.contrib import admin
from boliche.models import Ingrediente, Barra, Consumicion, Venta, DetalleVenta, DetalleConsumicion

@admin.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'marca')  # Campos a mostrar en la lista

@admin.register(Barra)
class BarraAdmin(admin.ModelAdmin):
    list_display = ('numeroBarra', 'ubicacion')

@admin.register(Consumicion)
class ConsumicionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio')

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'fecha', 'hora', 'barra')

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('venta', 'consumicion', 'cantidad', 'precio')
