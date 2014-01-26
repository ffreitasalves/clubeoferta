from clubeoferta.anuncio.models import anuncios,fotos,destaques,enderecos,regras,filtros,valores
from clubeoferta.anuncio.models import localidades
from django.contrib import admin

class fotos_InLine(admin.StackedInline):
    model = fotos
    extra = 3
    max_num = 6

class destaques_InLine(admin.StackedInline):
    model = destaques
    extra = 5
    
class enderecos_InLine(admin.StackedInline):
    model = enderecos
    extra = 1
    fieldsets=(
        (None, {
            'fields':(
                          ('logradouro','numero','complemento'),
                          ('bairro'),
                          ('cidade','uf'),
                          ('telefone'),
                      ),
            }),        
        )

class regras_InLine(admin.StackedInline):
    model = regras
    extra = 5

class valores_InLine(admin.StackedInline):
    model = valores
    extra=2
    
class filtros_InLine(admin.StackedInline):
    model = filtros
    max_num=1
    inlines = [
        valores_InLine,
        ]    
class anuncios_admin(admin.ModelAdmin):
    list_display=('anuncio','preco_original','preco_desconto','inicio','fim','order','order_link')
    save_on_top = True
    list_filter=('empresa','inicio','fim',)
    search_fields  = ('inicio','fim','anuncio','empresa',)
    ordering = ('order',)
    inlines = [
          fotos_InLine,
          destaques_InLine,
          regras_InLine,
          enderecos_InLine,
          filtros_InLine,
          valores_InLine,
        ]
   
admin.site.register(anuncios,anuncios_admin)
admin.site.register(localidades)
