# -*- coding: UTF-8 -*-
from django.db import models
from clubeoferta.anuncio.models import localidades
from django.contrib.auth.models import User

class usuarios(models.Model):
    usuario = models.ForeignKey(User, blank=True, null=True, editable=False)
    nome = models.CharField('Nome',max_length=200)
    email = models.EmailField('Email')
    senha = models.CharField('Senha',max_length=10)
    recebe_oferta = models.BooleanField("Quero receber a oferta do dia",default=True)
    localidades = models.ManyToManyField(localidades,null=True,blank=True)
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
    def save(self):
        if not self.id:
            c = usuarios.objects.filter(email = self.email).count()
            if c:
                raise EmailExistente

            usr = User.objects.filter(username = self.email)
            if usr:
                u = usr[0]
            else:
                u = User.objects.create_user(self.email, self.email, self.senha)
            u.save()
            self.user = u
        else:
            self.user = User.objects.get(email=self.email)
            self.user.username = self.email
            self.user.email = self.email
            self.user.set_password(self.senha)
            self.user.save()

        super(usuarios, self).save()

    def __unicode__(self):
        return self.nome

class empresas(models.Model):
    nome = models.CharField('Nome',max_length=200)
    cidade = models.CharField('Cidade',max_length=200)
    ramo = models.CharField('Ramo de Atuação',max_length=200)
    site = models.CharField('Site',max_length=200)
    contato = models.CharField('Nome para Contato',max_length=200) #Nome para Contato
    email = models.EmailField('Email')
    telefone = models.CharField('Telefone',max_length=200)
    comentario = models.TextField()
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
    def __unicode__(self):
        return self.nome
