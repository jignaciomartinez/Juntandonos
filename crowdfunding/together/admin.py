from django.contrib import admin
from .models import *

class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    list_editable = ("nombre", )
    ordering = ("id", )


class ComunaAdmin(admin.ModelAdmin):
    list_filter = ("region",)
    list_display = ("id", "nombre", "region")
    list_editable = ("nombre", "region")
    ordering = ("id", )


admin.site.register(Region, RegionAdmin)
admin.site.register(Comuna, ComunaAdmin)
admin.site.register(Producto)
admin.site.register(Proyecto)
admin.site.register(Categoria)
admin.site.register(TipoCuenta)
admin.site.register(CuentaBancaria)
admin.site.register(DetalleUsuario)
