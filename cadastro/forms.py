# -*- coding: UTF-8 -*-
from django import forms
from models import usuarios, empresas
from django.core.mail import EmailMultiAlternatives
from django.template import loader, Context


class form_login_direto(forms.ModelForm):
    class Meta:
        model = usuarios
        exclude = ('recebe_propagandas','recebe_oferta','nome')
        fields = ['email','senha',]    
    def __init__(self,*args,**kwargs):
        self.base_fields['senha'].widget = forms.PasswordInput()        
        super(form_login_direto,self).__init__(*args,**kwargs)
    def clean_email(self):
        if usuarios.objects.filter(email=self.cleaned_data['email']).count() != 1:
            raise forms.ValidationError('E-mail não cadastrado')
        return self.cleaned_data['email']

class form_empresas(forms.ModelForm):
    class Meta:
        model = empresas


class form_cadastro_direto(forms.ModelForm):
    confirme_a_senha = forms.CharField(max_length=10,widget = forms.PasswordInput)
    compromisso = forms.BooleanField(label="Li e aceito os termos de compromisso do ClubeOferta",initial=True)
    class Meta:
        model = usuarios
        exclude = ('recebe_propagandas',)
        fields = ['nome','email','senha','confirme_a_senha','recebe_oferta', 'compromisso']    

    def __init__(self,*args,**kwargs):
        self.base_fields['senha'].widget = forms.PasswordInput()        
        super(form_cadastro_direto,self).__init__(*args,**kwargs)
        
    def clean_email(self):
        if usuarios.objects.filter(email=self.cleaned_data['email']).count():
            raise forms.ValidationError('Já existe um usuário com este e-mail')
        return self.cleaned_data['email']

    def clean_confirme_a_senha(self):
        if self.cleaned_data['confirme_a_senha'] != self.data['senha']:
            raise forms.ValidationError('Confirmação de senha não confere')
        return self.cleaned_data['confirme_a_senha']

    def clean_compromisso(self):
	if not self.cleaned_data['compromisso']:
	    raise forms.ValidationError('Você não aceitou o termo de compromisso')
	return self.cleaned_data['compromisso']

    def enviar_boasvindas(self):
        titulo = '[ClubeOferta]Bem vindo ao Clube Oferta!'
        destino = self.cleaned_data['email']
        text_content = u"""
        Olá, %(nome)s
        Parabéns por entrar no ClubeOferta.
        Fique sempre atento, pois temos as melhores ofertas da sua cidade pra você se divertir gastando pouco.
        
        Atenciosamente,
        Equipe ClubeOferta     """ % {"nome":self.cleaned_data['nome']}

        msg = EmailMultiAlternatives(
            titulo,
            text_content,
            "ClubeOferta@clubeoferta.com.br",
            [destino])
        t = loader.get_template('emails/email_boasvindas.html')
        c = Context({
            'nome': self.cleaned_data['nome'],
            })
        html_content = t.render(c)
        msg.attach_alternative(html_content,"text/html")
        msg.send()
