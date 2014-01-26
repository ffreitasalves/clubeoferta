# -*- coding: utf-8 -*-
from django.core.management import BaseCommand
from random import sample
from string import join, ascii_uppercase as letras
from clubeoferta.compra.models import compras, nomes


def gera_voucher():
    voucher = join(sample(letras,8),"")
    return voucher


class Command(BaseCommand):
    def handle(self, **kwargs):
        concluidas = compras.objects.filter(status = "Completo")| compras.objects.filter(status = "Aprovado")
        for c in concluidas:
            for n in c.nomes():
                if not n.voucher:
                    while 1:
                        novo_voucher = gera_voucher()
                        #verifico se ja existe um voucher daquele existente
                        verif_voucher = nomes.objects.filter(voucher=novo_voucher)
                        if not verif_voucher:
                            break
                    n.voucher = novo_voucher
                    n.save()
            #Enviar email com o Voucher:
            c.enviar_voucher()
                    


                
                

