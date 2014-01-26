from clubeoferta.cadastro.models import usuarios, empresas
from django.contrib import admin

class usuarios_admin(admin.ModelAdmin):
    exclude = ('senha',)
   
admin.site.register(usuarios,usuarios_admin)
admin.site.register(empresas)
