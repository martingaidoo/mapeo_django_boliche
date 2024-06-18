from django.contrib import admin
from boliche.models import Ingrediente, Barra, Consumicion, Venta, DetalleVenta, DetalleConsumicion

admin.site.register(Ingrediente)
admin.site.register(Barra)
admin.site.register(Consumicion)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(DetalleConsumicion)
