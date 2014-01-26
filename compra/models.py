# -*- coding: utf-8 -*-
from django.db import models
from clubeoferta.cadastro.models import usuarios 
from clubeoferta.anuncio.models import anuncios, regras
from django.core.mail import EmailMultiAlternatives
from django.template import loader, Context

class compras(models.Model):
    usuario = models.ForeignKey(usuarios)
    anuncio = models.ForeignKey(anuncios)
    status = models.CharField(max_length=30)
    total= models.DecimalField('Total',max_digits=6, decimal_places=2)
    DataCriacao = models.DateTimeField(auto_now_add=True)
    UltimaModificacao = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return unicode(self.usuario)
    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
    def save(self, *args, **kwargs):
        if self.status == "Aprovado":
            titulo = '[ClubeOferta]Pagamento Aprovado!'
            destino = self.usuario.email
            text_content = u"""
             Olá %(nome)s,



            Quando a oferta “%(anuncio)s” tiver sido fechada com sucesso, enviaremos o voucher e toda a informação relevante num e-mail separado.



            Este procedimento acontece até 24 horas após o encerramento de cada oferta no Clube Oferta.


            As informações sobre as regras e condições de uso da oferta estarão detalhadas neste voucher. Se quiser re-imprimir ou acessar os vouchers, é
            só entrar no ClubeOferta e acessar sua conta.


            Se o número mínimo de compradores não for atingido, a oferta não será concretizada, sendo assim, não haverá cobrança alguma no cartão de
            crédito daqueles que já haviam demonstrado interesse pela oferta.


            Caso tenha dúvidas, entre em contato: sac@clubeoferta.com.br.




            Um abraço,


            Equipe ClubeOferta
            """ % {
                "nome":self.usuario.nome,
                "anuncio":self.anuncio.anuncio,
                }

            msg = EmailMultiAlternatives(
                titulo,
                text_content,
                "ClubeOferta@clubeferta.com.br",
                [destino])
            t = loader.get_template('emails/email_pedidocompra.html')
            c = Context({
                "nome":self.usuario.nome,
                "anuncio":self.anuncio.anuncio,
                })
            html_content = t.render(c)
            msg.attach_alternative(html_content,"text/html")
            msg.send()
        elif self.status == "Cancelado":
            titulo = '[ClubeOferta]Pagamento Cancelado!'
            destino = self.usuario.email
            text_content = u"""
             Olá %(nome)s,



            O seu pedido de compra para “%(anuncio)s” foi cancelado.


            Um abraço,


            Equipe ClubeOferta
            """ % {
                "nome":self.usuario.nome,
                "anuncio":self.anuncio.anuncio,
                }

            msg = EmailMultiAlternatives(
                titulo,
                text_content,
                "ClubeOferta@clubeoferta.com.br",
                [destino])
            t = loader.get_template('emails/email_cancelado.html')
            c = Context({
                "nome":self.usuario.nome,
                "anuncio":self.anuncio.anuncio,
                })
            html_content = t.render(c)
            msg.attach_alternative(html_content,"text/html")
            msg.send()
        super(compras, self).save(*args, **kwargs) # Salva na Base, depois manda o email se o status for aprovado.

    def nomes(self):
        return nomes.objects.filter(compra = self.id)

    def enviar_voucher(self):
        titulo = '[ClubeOferta]Compra Liberada - %s!' % (self.anuncio)
        destino = self.usuario.email
        text_content = u"""
        Olá, %(nome)s
        Parabéns por entrar no ClubeOferta!.
        Acesse sua conta no ClubeOferta para ver os seus vouchers!!!
        
        Atenciosamente,
        Equipe ClubeOferta     """ % {"nome":self.usuario.nome}

        msg = EmailMultiAlternatives(
            titulo,
            text_content,
            "ClubeOferta@clubeoferta.com.br",
            [destino])
        t = loader.get_template('emails/email_voucher.html')
        c = Context({
            'compra': self,
            'regras': regras.objects.filter(anuncio=self.anuncio)
            })
        html_content = t.render(c)
        msg.attach_alternative(html_content,"text/html")
        msg.send()
        

class nomes(models.Model):
    compra = models.ForeignKey(compras)
    nome = models.CharField(max_length=200)
    filtro = models.CharField(max_length=200,null=True,blank=True)
    valor= models.CharField(max_length=200,null=True,blank=True)
    voucher = models.CharField(max_length=10,null=True,blank=True)
    DataCriacao = models.DateTimeField(auto_now_add=True)
    UltimaModificacao = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.nome
    class Meta:
        verbose_name = "Nome"
        verbose_name_plural = "Nomes"

class cadastro_pagseguro(models.Model):
    VendedorEmail = models.CharField(max_length=255,null=True,blank=True)
    TransacaoID = models.CharField(max_length=255,null=True,blank=True)
    Referencia = models.CharField(max_length=255)
    Extras = models.CharField(max_length=8,null=True,blank=True) #vem com , trocar pra .
    Anotacao = models.CharField(max_length=250,null=True,blank=True)
    TipoPagamento = models.CharField(max_length=30,null=True,blank=True)
    StatusTransacao = models.CharField(max_length=30,null=True,blank=True)
    CliNome = models.CharField(max_length=100,null=True,blank=True)
    CliEmail = models.CharField(max_length=255,null=True,blank=True)
    CliEndereco = models.CharField(max_length=200,null=True,blank=True)
    CliNumero = models.CharField(max_length=10,null=True,blank=True)
    CliComplemento = models.CharField(max_length=100,null=True,blank=True)
    CliBairro = models.CharField(max_length=100,null=True,blank=True)
    CliCidade = models.CharField(max_length=100,null=True,blank=True)
    CliEstado = models.CharField(max_length=2,null=True,blank=True)
    CliCEP = models.CharField(max_length=10,null=True,blank=True)
    CliTelefone = models.CharField(max_length=16,null=True,blank=True)
    def __unicode__(self):
        return unicode(self.Referencia)
    class Meta:
        verbose_name = "Cadastro do Pagseguro"
        verbose_name_plural = "Cadastros do Pagseguro"
