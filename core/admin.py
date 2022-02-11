from django.contrib import admin
from core.models import Categoria, Compra, Fabricante, ItensCompra, Pneu

admin.site.register(Categoria)
admin.site.register(Fabricante)
admin.site.register(Pneu)

class ItensInline(admin.TabularInline):
  model = ItensCompra

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
  inlines = (ItensInline,)