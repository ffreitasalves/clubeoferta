# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

handler500 = 'clubeoferta.views.server_error'

urlpatterns = patterns('',
    # Example:
    # (r'^clubedesconto/', include('clubedesconto.foo.urls')),
    url(r'^$','clubeoferta.anuncio.views.index',name='index'),
    url(r'^comprar/(?P<anuncio_id>\d+)/$','clubeoferta.anuncio.views.pre_compra',name='pre_compra'),
    url(r'^redireciona-pagseguro/$','clubeoferta.anuncio.views.pre_pagseguro',name='pre_pagseguro'),
    url(r'^anuncie/$','clubeoferta.anuncio.views.anuncie',name='anuncie'),
    url(r'^cadastro/$','clubeoferta.anuncio.views.cadastro',name='cadastro'),
    url(r'^recentes/$','clubeoferta.anuncio.views.recentes',name='recentes'),
    url(r'^conta/$','clubeoferta.anuncio.views.conta',name='conta'),
    url(r'^login/$','clubeoferta.anuncio.views.login',name='login'),
    url(r'^logout/$','clubeoferta.anuncio.views.logout',name='logout'),

    #comentários
    (r'^comments/', include('django.contrib.comments.urls')),
                       
    #Mudar e Resetar Senha
    url(r'^mudar_senha/$', 'django.contrib.auth.views.password_change', name='password_change'),
    url(r'^mudar_senha/ok/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r'^resetar_senha/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^resetar_senha_ok/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^resetar_senha/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': '/resetar_senha/completo/'},name='password_reset_confirm'),
    url(r'^resetar_senha/completo/$', 'django.contrib.auth.views.password_reset_complete',name='password_reset_complete'),

    #erro 500
    url(r'^500/$','clubeoferta.views.server_error',name='server_error'),

    #Url de retorno do pagseguro
    url(r'^retorno/pagseguro/$','clubeoferta.anuncio.views.retorno_pagseguro',name='retorno_pagseguro'),

    #url da pagina de ordenacao do admin
    url(r'^admin/orderedmove/(?P<direction>up|down)/(?P<model_type_id>\d+)/(?P<model_id>\d+)/$', 'clubeoferta.anuncio.views.admin_move_ordered_model', name="admin-move"),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),


    (r'^media/(.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)
