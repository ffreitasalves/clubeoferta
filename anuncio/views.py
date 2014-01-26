# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from models import anuncios,fotos, destaques, regras,enderecos, valores,filtros
from datetime import datetime, timedelta
from django.template import RequestContext
from clubeoferta.cadastro.forms import form_login_direto, form_empresas, form_cadastro_direto
from clubeoferta.cadastro.models import usuarios
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, logout as authlogout, login as authlogin
from clubeoferta.compra.models import compras,nomes, cadastro_pagseguro
from django.contrib.auth.decorators import login_required
from clubeoferta.pagseguropy.pagseguro import *
from clubeoferta.settings import *
from django import forms
from clubeoferta.pagseguropy.pagamentolib import PagSeguro
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_unicode
from django.core.mail import send_mail
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
from models import OrderedModel
from django.db import transaction
from settings import TOKEN

@staff_member_required
@transaction.commit_on_success
def admin_move_ordered_model(request, direction, model_type_id, model_id):
    """
    Faz a Ordenação no Admin
    """
    if direction == "up":
        OrderedModel.move_up(model_type_id, model_id)
    else:
        OrderedModel.move_down(model_type_id, model_id)
    
    ModelClass = ContentType.objects.get(id=model_type_id).model_class()
    
    app_label = ModelClass._meta.app_label
    model_name = ModelClass.__name__.lower()

    url = "/admin/%s/%s/" % (app_label, model_name)
    
    return HttpResponseRedirect(url)


def index(request):
    """
    Descrição:
    Página inicial, mostra sempre o anúncio ativo, caso contrário mostra o último
    """
    #filtro para o anuncio ativo
    anuncio_valido = anuncios.objects.filter(inicio__lt = datetime.now(),fim__gt = datetime.now())
    if anuncio_valido.count() >= 1:
        anuncio_valido = anuncio_valido[0]
        delta_tempo = anuncio_valido.fim - datetime.now()
        tempo_restante = 86400*delta_tempo.days + delta_tempo.seconds
    else:
        #mostrar o ultimo anuncio, caso nenhum este ativo
        anuncio_valido = anuncios.objects.filter(fim__lt = datetime.now()).order_by("-fim")[0]
        tempo_restante = 0
    
    fotos_validas = fotos.objects.filter(anuncio=anuncio_valido)
    destaques_validos = destaques.objects.filter(anuncio=anuncio_valido)
    regras_validas = regras.objects.filter(anuncio=anuncio_valido)

    vendidos = 0
    for compra in compras.objects.filter(anuncio=anuncio_valido, status="Em análise"):
        vendidos += nomes.objects.filter(compra = compra).count()
    for compra in compras.objects.filter(anuncio=anuncio_valido, status="Completo"):
        vendidos += nomes.objects.filter(compra = compra).count()
    for compra in compras.objects.filter(anuncio=anuncio_valido, status="Aprovado"):
        vendidos += nomes.objects.filter(compra = compra).count()

    #Montar texto com o número de vendas e se a oferta está ativa ou não.
    if vendidos < anuncio_valido.minimo:
        if vendidos ==1:
            texto_venda = "%d Vendido - Faltam %d para valer a oferta!" % (vendidos, anuncio_valido.minimo - vendidos)
        else:
            texto_venda = "%d Vendidos - Faltam %d para valer a oferta!" % (vendidos, anuncio_valido.minimo - vendidos)
    elif vendidos >= anuncio_valido.maximo:
        texto_venda = "%d Vendidos - Vendas Encerradas!" % vendidos
    else:
        if vendidos <=1 :
            texto_venda = "%d Vendido - Oferta Valendo!" % vendidos
        else:
            texto_venda = "%d Vendidos - Oferta Valendo!" % vendidos
        

    
    
    return render_to_response(
        'index.html',
        {'anuncio':anuncio_valido,
         'fotos':fotos_validas,
         'destaques':destaques_validos,
         'regras':regras_validas,
         'tempo_restante':tempo_restante,
         'enderecos': enderecos.objects.filter(anuncio=anuncio_valido),
         'texto_venda':texto_venda,
         },
        context_instance = RequestContext(request)
        )

@login_required
def pre_compra(request,anuncio_id):
    """
    Descrição:
    Nossa Página de compra.
    Ela verifica se o anúncio ainda é válido
    cadastra o usuário, caso ele seja novo no site
    faz o login
    salva a compra na tabela compras
    envia para a página de redirecionamento ao pagseguro
    """
    anuncio_valido = get_object_or_404(anuncios,pk=anuncio_id)
    delta_tempo = anuncio_valido.fim - datetime.now()
    valores_validos = valores.objects.filter(anuncio = anuncio_valido)


    # se o tempo acabou, mando pra primeira página
    if delta_tempo <= timedelta(0):
        return HttpResponseRedirect('/')  

    vendidos = 0
    for compra in compras.objects.filter(anuncio=anuncio_valido, status="Em análise"):
        vendidos += nomes.objects.filter(compra = compra).count()
    for compra in compras.objects.filter(anuncio=anuncio_valido, status="Completo"):
        vendidos += nomes.objects.filter(compra = compra).count()
    for compra in compras.objects.filter(anuncio=anuncio_valido, status="Aprovado"):
        vendidos += nomes.objects.filter(compra = compra).count()

    #Se deu o máximo de vendas, mando pra página inicial
    if anuncio_valido.maximo and vendidos >= anuncio_valido.maximo:
        return HttpResponseRedirect('/')  
        
    if request.method =='POST':
        lista_nomes = unicode(request.POST['nomes']).strip(";").split(";")
        if anuncio_valido.tem_filtro():
            lista_filtros = unicode(request.POST['filtros']).strip(";").split(";")

        #salvar em compras
        u = usuarios.objects.get(email = request.user.email)
        valor_total = anuncio_valido.preco_desconto * len(lista_nomes)
        nova_compra = compras(usuario = u, anuncio = anuncio_valido, status = "Encaminhando", total = valor_total)
        nova_compra.save()


        for i,n in enumerate(lista_nomes):
            novo_nome = nomes(compra = nova_compra, nome = n)
            novo_nome.save()
            if anuncio_valido.tem_filtro():
                novo_nome.filtro = filtros.objects.filter(anuncio = anuncio_valido)[0].nome_filtro
                novo_nome.valor = valores.objects.get(pk=int(lista_filtros[i])).valor
                novo_nome.save()
                
        
        #enviar para pre_pagseguro
        request.session['compra_id'] = nova_compra.id
        return HttpResponseRedirect('/redireciona-pagseguro/')                    

        
    return render_to_response(
        'pre_compra.html',
        {'anuncio':anuncio_valido,
         'valores':valores_validos,
         },
        context_instance = RequestContext(request)
        )

@login_required
def pre_pagseguro(request):
    """
    Descrição:
    Página que redirecionará para o pagamento no pagseguro.
    Ela contém o formulário que será enviado com os nomes escolhidos no nosso site
    """
    compra_id  = request.session.get('compra_id',"")
    if not compra_id:
        return HttpResponseRedirect('/')
    
    compra_id = int(compra_id)
    nova_compra = get_object_or_404(compras,pk=compra_id)
    request.session['compra_id'] = ""
    
    carrinho = Pagseguro(tipo='CP',email_cobranca = E_MAIL_COBRANCA, ref_transacao = nova_compra.id, encoding='UTF-8')
    nomes_compra = nomes.objects.filter(compra=nova_compra)
    if not nomes_compra:
        return HttpResponseRedirect('/')  
    for n in nomes_compra:
        descricao = ("%s - %s") % (nova_compra.anuncio.empresa, n.nome)
        carrinho.item(id = n.id, descr = descricao, quant=1, valor=nova_compra.anuncio.preco_desconto)
    return render_to_response(
        'redireciona.html',
        {'carrinho':carrinho,
         },
        context_instance = RequestContext(request)
        )

def anuncie(request):
    """
    Descrição:
    Página de contato de empresas que querem anunciar
    """
    if request.method =='POST':
        form = form_empresas(request.POST)
        if form.is_valid():
            nova_empresa = form.save()
            #colocar código pra enviar e-mail depois que configurar
            send_mail( "[ClubeOferta]Contato de Empresa", #titulo
                u"""Nome:%s\n
                Cidade:%s\n
                Ramo de Atuação:%s\n
                Site:%s\n
                Nome para Contato:%s\n
                Email:%s\n
                Telefone:%s\n
                Comentario:%s\n
                """ % (smart_unicode(request.POST.get("nome")),
                       smart_unicode(request.POST.get("cidade")),
                       smart_unicode(request.POST.get("ramo")),
                       smart_unicode(request.POST.get("site")),
                       smart_unicode(request.POST.get("contato")),
                       smart_unicode(request.POST.get("email")),
                       smart_unicode(request.POST.get("telefone")),
                       smart_unicode(request.POST.get("comentario"))), #corpo
                'clubeoferta@clubeoferta.com.br', #quem envia
                ['ffreitasalves@gmail.com',
                 ] #lista de destinatários
            )
            return HttpResponseRedirect('/enviado-com-sucesso/')
    else:
        form = form_empresas()

    return render_to_response(
        'anuncie.html',
        {
            'form': form,
         },
        context_instance = RequestContext(request)
        )

def cadastro(request): 
    """
    Descrição:
    Página de cadastro de usuário sem que o mesmo esteja realizando alguma compra
    """
    if request.method =='POST':
        form = form_cadastro_direto(request.POST)
        if form.is_valid():
            novo_usuario = form.save()
            novo_usuario = authenticate(username = novo_usuario.email, password=novo_usuario.senha)
            authlogin(request, novo_usuario)
            #envia email de boas vindas!
            form.enviar_boasvindas()
            return HttpResponseRedirect("/cadastro/boasvindas/")
    else:
        form = form_cadastro_direto()

    return render_to_response(
        'cadastro.html',
        {
            'form': form,
         },
        context_instance = RequestContext(request)
        )

@csrf_exempt
def retorno_pagseguro(request):
    """
    Descricao:
    Armazena os dados do pedido e exibe a tela de pedido concluido.
    Verifica se o robo do PagSeguro enviou os dados do pedido via POST, e
    então armazena no banco de dados.
    Por fim, exibe a tela de pedido concluido com sucesso.
    """ 
    if request.method == 'POST':
        # token gerado no painel de controle do PagSeguro - 27/08/2010
        token = TOKEN
	request.encoding = "latin-1"
        p = PagSeguro()
        retorno = p.processar(token, request.POST)
        if retorno == True:
            try:
                # Cadastra os dados recebidos no banco de dados.
                # Utilize o request.POST.get('nomedocampo') para obter os valores
                request.encoding = "latin-1"
                dic = {}
                dic["VendedorEmail"]=request.POST.get("VendedorEmail").encode("iso-8859-1") 
                dic["TransacaoID"]=request.POST.get("TransacaoID").encode("iso-8859-1") 
                dic["Referencia"]=request.POST.get("Referencia").encode("iso-8859-1") 
                dic["Extras"]=request.POST.get("Extras").encode("iso-8859-1") 
                dic["Anotacao"]=request.POST.get("Anotacao").encode("iso-8859-1") 
                dic["TipoPagamento"]=request.POST.get("TipoPagamento").encode("iso-8859-1") 
                dic["StatusTransacao"]=request.POST.get("StatusTransacao").encode("iso-8859-1") 
                dic["CliNome"]=request.POST.get("CliNome").encode("iso-8859-1") 
                dic["CliEmail"]=request.POST.get("CliEmail").encode("iso-8859-1") 
                dic["CliEndereco"]=request.POST.get("CliEndereco").encode("iso-8859-1") 
                dic["CliNumero"]=request.POST.get("CliNumero").encode("iso-8859-1") 
                dic["CliComplemento"]=request.POST.get("CliComplemento").encode("iso-8859-1") 
                dic["CliBairro"]=request.POST.get("CliBairro").encode("iso-8859-1") 
                dic["CliCidade"]=request.POST.get("CliCidade").encode("iso-8859-1") 
                dic["CliEstado"]=request.POST.get("CliEstado").encode("iso-8859-1") 
                dic["CliCEP"]=request.POST.get("CliCEP").encode("iso-8859-1") 
                dic["CliTelefone"]=request.POST.get("CliTelefone").encode("iso-8859-1") 
                send_mail(
                    "[ClubeOferta]Pagseguro Dicionário", #titulo
                    "Dicionário:\n%s" %(dic), #corpo
                    'ClubeOferta@clubeoferta.com.br', #quem envia
                    ['ffreitasalves@gmail.com',
                     ] #lista de destinatários
                )

                teste_existe = cadastro_pagseguro.objects.filter(Referencia=int(dic["Referencia"]))
                if teste_existe.count():
                    novo_cadastro = cadastro_pagseguro.objects.get(Referencia=int(dic["Referencia"]))
                else:
                    novo_cadastro = cadastro_pagseguro()
                novo_cadastro.VendedorEmail=dic["VendedorEmail"].decode("latin-1")
                novo_cadastro.TransacaoID=dic["TransacaoID"].decode("latin-1")
                novo_cadastro.Referencia=dic["Referencia"].decode("latin-1")
                novo_cadastro.Extras=dic["Extras"].decode("latin-1")
                novo_cadastro.Anotacao=dic["Anotacao"].decode("latin-1")
                novo_cadastro.TipoPagamento=dic["TipoPagamento"].decode("latin-1")
                novo_cadastro.StatusTransacao=dic["StatusTransacao"].decode("latin-1")
                novo_cadastro.CliNome=dic["CliNome"].decode("latin-1")
                novo_cadastro.CliEmail=dic["CliEmail"].decode("latin-1")
                novo_cadastro.CliEndereco=dic["CliEndereco"].decode("latin-1")
                novo_cadastro.CliNumero=dic["CliNumero"].decode("latin-1")
                novo_cadastro.CliComplemento=dic["CliComplemento"].decode("latin-1")
                novo_cadastro.CliBairro=dic["CliBairro"].decode("latin-1")
                novo_cadastro.CliCidade=dic["CliCidade"].decode("latin-1")
                novo_cadastro.CliEstado=dic["CliEstado"].decode("latin-1")
                novo_cadastro.CliCEP=dic["CliCEP"].decode("latin-1")
                novo_cadastro.CliTelefone=dic["CliTelefone"].decode("latin-1")

                novo_cadastro.save()
                
                #atualizando o status da compra
                compra = compras.objects.get(pk=int(dic["Referencia"]))
                compra.status = novo_cadastro.StatusTransacao
                compra.save()
                
                
            except Exception as inst:
                #Em caso de Erro manda um email com os erros pra mim.
                send_mail(
                    "[ClubeOferta]Erro de Retorno Pagseguro", #titulo
                    """Tipo:%s\n
                    Args:%s\n
                    Inst:%s\n""" %(type(inst),inst.args,inst), #corpo
                    'contato@clubeoferta.com.br', #quem envia
                    ['ffreitasalves@gmail.com',
                     ] #lista de destinatários
                )
                                
            return HttpResponse('Ok')
        else:
            return HttpResponse('Error')
 
    else:
        # Carrega tela contendo a mensagem de compra realizada
        return HttpResponseRedirect("/confirmacao-compra/")

def recentes(request):
    """
    Descrição:
    Devolve os últimos anúncios para mostrar como portifólio no site.
    """
    anuncios_recentes = anuncios.objects.filter(fim__lt = datetime.now())
    
    return render_to_response(
        'recentes.html',
        {'recentes':anuncios_recentes,
         
         },
        context_instance = RequestContext(request)
        )

@login_required
def conta(request):
    """
    Descrição:
    Mostra a conta do usuário com as compras realizadas.
    """
    filtro_compras = compras.objects.filter(usuario = request.user)
    return render_to_response(
        'conta.html',
        {
            'compras': filtro_compras,
         },
        context_instance = RequestContext(request)
        )

def login(request):
    msg_erro = ""
    prox = request.GET.get('next')
    if not prox:
        prox ="/"
    if request.method =='POST':
        login = form_login_direto(request.POST)
        if login.is_valid():
            usuario = authenticate(username = request.POST.get('email'), password=request.POST.get('senha'))
            if usuario is not None:
                authlogin(request, usuario)
                return HttpResponseRedirect(prox)
            else:
                msg_erro = "Senha incorreta!"
                
            
    else:
        login = form_login_direto()

    return render_to_response(
        'login.html',
        {
         'form_login':login,
         'erro': msg_erro,
         },
        context_instance = RequestContext(request)
        )

def logout(request):
    authlogout(request)
    return HttpResponseRedirect('/')
