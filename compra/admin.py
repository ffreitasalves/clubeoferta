from clubeoferta.compra.models import compras, nomes, cadastro_pagseguro
from django.contrib import admin


class nomes_InLine(admin.StackedInline):
    model = nomes

class comprasAdmin(admin.ModelAdmin):
    inlines=[
        nomes_InLine,
        ]
    list_display = ('id','usuario','status',)

class cadastro_pagseguroAdmin(admin.ModelAdmin):
    list_display = ('Referencia','TipoPagamento','StatusTransacao','CliNome')
   
admin.site.register(compras,comprasAdmin)
admin.site.register(cadastro_pagseguro,cadastro_pagseguroAdmin)
