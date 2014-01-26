# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.localflavor.br.br_states import STATE_CHOICES
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

#classe de modelo ordenado
class OrderedModel(models.Model):
    order = models.PositiveIntegerField(editable=False)

    def save(self):
        if not self.id:
            try:
                self.order = self.__class__.objects.all().order_by("-order")[0].order + 1
            except IndexError:
                self.order = 0
        super(OrderedModel, self).save()
        

    def order_link(self):
        model_type_id = ContentType.objects.get_for_model(self.__class__).id
        model_id = self.id
        kwargs = {"direction": "up", "model_type_id": model_type_id, "model_id": model_id}
        url_up = reverse("admin-move", kwargs=kwargs)
        kwargs["direction"] = "down"
        url_down = reverse("admin-move", kwargs=kwargs)
        return '<a href="%s">up</a> | <a href="%s">down</a>' % (url_up, url_down)
    
    order_link.allow_tags = True
    order_link.short_description = 'Move'
    order_link.admin_order_field = 'order'


    @staticmethod
    def move_down(model_type_id, model_id):
        try:
            ModelClass = ContentType.objects.get(id=model_type_id).model_class()

            lower_model = ModelClass.objects.get(id=model_id)
            higher_model = ModelClass.objects.filter(order__gt=lower_model.order)[0]
            
            lower_model.order, higher_model.order = higher_model.order, lower_model.order

            higher_model.save()
            lower_model.save()
        except IndexError:
            pass
        except ModelClass.DoesNotExist:
            pass
                
    @staticmethod
    def move_up(model_type_id, model_id):
        try:
            ModelClass = ContentType.objects.get(id=model_type_id).model_class()

            higher_model = ModelClass.objects.get(id=model_id)
            lower_model = ModelClass.objects.filter(order__lt=higher_model.order)[0]

            lower_model.order, higher_model.order = higher_model.order, lower_model.order

            higher_model.save()
            lower_model.save()
        except IndexError:
            pass
        except ModelClass.DoesNotExist:
            pass

    class Meta:
        ordering = ['order',]
        abstract = True

class localidades(models.Model):
    uf =models.CharField('UF',max_length=2,choices=STATE_CHOICES)
    cidade = models.CharField('Nome da cidade:',max_length=200)
    cidade_url = models.CharField('Nome da Url da cidade',max_length=200,unique=True)
    class Meta:
        verbose_name = "Localidade"
        verbose_name_plural = "Localidades"
    def __unicode__(self):
        return self.cidade_url


class anuncios(OrderedModel):
    anuncio = models.CharField('Anuncio',max_length=200)
    empresa = models.CharField('Empresa',max_length=200, help_text="Também será usado como Produto no Pagseguro!")
    twitt = models.CharField('Compartilhe no Twitter',max_length=140, help_text="Não pode ter porcentagem!")
    #preços até 9.999,99
    preco_original = models.DecimalField('Preço Original',max_digits=6, decimal_places=2, help_text="Use (.) como separador decimal")
    preco_desconto= models.DecimalField('Preço com Desconto',max_digits=6, decimal_places=2, help_text="Use (.) como separador decimal")
    site =  models.CharField('Site',max_length=200)
    minimo = models.IntegerField('Venda Mínima',help_text="Venda mínima para valer a oferta.")
    maximo = models.IntegerField('Venda Máxima',blank=True,null=True,help_text="Nesse valor a oferta pára de ser vendida.")
    texto = models.TextField()
    validade = models.DateField('Validade da Promoção')
    duracao = models.IntegerField('Duração do Anúncio em Horas')
    

    #parâmetros de data -- Importante
    inicio = models.DateTimeField('Iniciar em')
    fim = models.DateTimeField('Terminar em')
    DataCriacao = models.DateTimeField(auto_now_add=True)
    UltimaModificacao = models.DateTimeField(auto_now=True)

    #localidades em que valem a promoção
    localidades = models.ManyToManyField(localidades)

    class Meta:
        ordering = ('-inicio','-fim')
        verbose_name = "Anuncio"
        verbose_name_plural = "Anuncios"
    def __unicode__(self):
        return self.anuncio
    def foto_principal(self):
        f = fotos.objects.filter(anuncio = self)[0]
        return f.foto
    def tem_filtro(self):
        filtro = filtros.objects.filter(anuncio = self).count()
        return filtro

class enderecos(models.Model):
    anuncio = models.ForeignKey(anuncios)
    logradouro = models.CharField('Logradouro',max_length=200,blank=True,null=True)
    numero = models.IntegerField('Número',blank=True,null=True)
    complemento = models.CharField('Complemento',max_length=200,blank=True,null=True)
    bairro = models.CharField('Bairro',max_length=200,blank=True,null=True)
    cidade = models.CharField('Cidade',max_length=200,blank=True,null=True)
    uf =models.CharField('UF',max_length=2,choices=STATE_CHOICES,blank=True,null=True)
    telefone = models.CharField('Telefone',max_length=200,blank=True,null=True)
    def endereco(self):
        return "%s, %d %s" % (self.logradouro,self.numero,self.complemento)
    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"
    def __unicode__(self):
        return self.logradouro

class destaques(models.Model):
    anuncio = models.ForeignKey(anuncios)
    destaque = models.CharField('Destaque',max_length=200)
    class Meta:
        verbose_name = "Destaque"
        verbose_name_plural = "Destaques"
    def __unicode__(self):
        return self.destaque

class regras(models.Model):
    anuncio = models.ForeignKey(anuncios)
    regra = models.CharField('Regra',max_length=200)
    class Meta:
        verbose_name = "Regra"
        verbose_name_plural = "Regras"
    def __unicode__(self):
        return self.regra

class fotos(models.Model):
    anuncio = models.ForeignKey(anuncios)
    foto = models.ImageField('Imagem',max_length=200,upload_to='imagens_anuncios/')
    class Meta:
        verbose_name = "Fotos"
        verbose_name_plural = "Foto"
    def __unicode__(self):
        return unicode(self.foto)

class filtros(models.Model):
    anuncio = models.ForeignKey(anuncios)
    nome_filtro = models.CharField('Nome do Filtro',max_length=200)
    class Meta:
        verbose_name = "Filtro"
        verbose_name_plural = "Filtros"
    def __unicode__(self):
        return self.nome_filtro

class valores(models.Model):
    anuncio = models.ForeignKey(anuncios)
    filtro =  models.ForeignKey(filtros)
    valor = models.CharField('Valor do Filtro',max_length=200)
    qtd = models.IntegerField(null=True, blank=True)
    class Meta:
        verbose_name = "Valor"
        verbose_name_plural = "Valores"
    def __unicode__(self):
        return self.valor
