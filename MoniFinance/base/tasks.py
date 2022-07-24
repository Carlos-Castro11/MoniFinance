
from apscheduler.schedulers.background import BackgroundScheduler
import schedule
import time


from .models import Ativo, HistAtivo
from users.models import User


import requests
import json


from django.utils import timezone

from django.core.mail import send_mail



def update_histAtivo():
    
    b3_list = Ativo.objects.values('b3').distinct()

    for b3 in b3_list:
        ativo = b3['b3']
       
        hist_list = HistAtivo.objects.filter(fk_ativo__b3 = ativo, ultimo_hist=True)
        
        
        url = 'https://api.hgbrasil.com/finance/stock_price?key=5b52b69a&symbol=' + ativo
        request_api = requests.get(url).json()

        percent = request_api['results'][ativo]['change_percent']
        val = request_api['results'][ativo]['price']

        
        if percent == 0:
            percent2 = 1
        else:
            percent2 = 1 + (percent / 100)

        valor_anterior = round((val / percent2), 2)
            
        
        for hist in hist_list:
            histAtivo = HistAtivo.objects.create(
                fk_ativo = hist.fk_ativo,
                valor =  val,
                data_atualizacao = timezone.now(),
                porcentagem = percent,
                valor_anterior = round((valor_anterior / percent2),2),
                ultimo_hist = True
            )
            histAtivo.save()

            
            hist.ultimo_hist = False
            hist.save()

    print('Historico dos ativos atualizado...')


def send_emails():
    
    user_list = User.objects.all()

    for user in user_list:
        
        hist_list = HistAtivo.objects.filter(ultimo_hist=True, fk_ativo__fk_user__id__exact=user.id)

        
        ativos_compra = ''
        ativos_venda = ''

        for hist in hist_list:
            
            if hist.valor < hist.fk_ativo.lim_inf:
                ativos_compra += hist.fk_ativo.b3 + ' '
                
           
            elif hist.valor > hist.fk_ativo.lim_sup:  
                ativos_venda += hist.fk_ativo.b3 + ' '
                
        
        if len(ativos_compra) > 0:
            send_mail(
            'Oportunidade de compra de ativo | Monifinance',
            'Ola prezado cliente, \n\n' + 'O(s) ativo(s) ' + ativos_compra +'esta(o) com oportunidade de compra!!\n\n' + 'Atenciosamente,\n\n' + 'Equipe Monifinance',
            'contato@monifinance.com.br',
            [user.email],
            fail_silently=False,
            )
        if len(ativos_venda) > 0:
            send_mail(
            'Oportunidade de venda de ativo | Monifinance',
            'Ola prezado cliente, \n\n' + 'O(s) ativo(s) ' + ativos_venda +'esta(o) com oportunidade de venda!!\n\n' + 'Atenciosamente,\n\n' + 'Equipe Monifinance',
            'contato@monifinance.com.br',
            [user.email],
            fail_silently=False,
            )

    print("E-mails enviados...")



def start():  
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_histAtivo, "interval", minutes = 1)
    scheduler.add_job(send_emails, "interval",  minutes = 1)
    scheduler.start()
