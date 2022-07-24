from django.shortcuts import render, redirect
from .models import Ativo, HistAtivo
from users.models import User
from .forms import AtivoCreate, AtivoUpdate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import requests
import json
from django.utils import timezone

def home(request):
    return render(request, 'base/home.html')



@login_required(login_url='login')
def create_ativo(request):
    flag = 0
    user = request.user

    if request.method == 'POST':
        form = AtivoCreate(request.POST)

        if form.is_valid():
            user_id = User.objects.get(id=request.user.id)

            ativo = form.cleaned_data['b3'].upper()
            url = 'https://api.hgbrasil.com/finance/stock_price?key=5b52b69a&symbol=' + ativo
            request_api = requests.get(url).json()

           
            if 'error' in request_api['results'][ativo]:
                flag = 1

            else:
                
                if Ativo.objects.filter(fk_user__exact=user_id,b3__exact=ativo).count() == 0:
                    
                    ativo_insert = Ativo.objects.create(
                        b3= ativo,
                        nome_empresa= request_api['results'][ativo]['company_name'],
                        desc_empresa = request_api['results'][ativo]['description'],
                        lim_inf=form.cleaned_data['lim_inf'],
                        lim_sup=form.cleaned_data['lim_sup'],
                        fk_user = user_id,
                    )
                    ativo_insert.save()

                    
                    percent = request_api['results'][ativo]['change_percent']
                    val = request_api['results'][ativo]['price']

                    
                    if percent == 0:
                        percent2 = 1
                    else:
                        percent2 = 1 + (percent / 100)

                    val_ant = round((val / percent2), 2)

                    
                    histAtivo = HistAtivo.objects.create(
                        fk_ativo = Ativo.objects.get(fk_user=user_id,b3=ativo),
                        valor =  val,
                        data_atualizacao = timezone.now(),
                        porcentagem = percent,
                        valor_anterior = round((val_ant / percent2),2),
                        ultimo_hist = True
                    )
                    histAtivo.save()

                   
                    return redirect('profile', pk=user.id)

                else:
                    flag = 3
    else:
        form = AtivoCreate()
        
    context = {
    'form': form,
    'flag': flag,
    }

    return render(request, 'ativo/create.html', context)



#Update ativo view
@login_required(login_url='login')
def update_ativo(request, pk):
    ativo = get_object_or_404(Ativo, pk=pk)
    user = request.user

    if request.method == 'POST':
        form = AtivoUpdate(request.POST)

        if form.is_valid():
            ativo.lim_sup = form.cleaned_data['lim_sup']
            ativo.lim_inf = form.cleaned_data['lim_inf']
            ativo.save()

            return redirect('profile', pk=user.id)

    else:
        form = AtivoUpdate(initial={'lim_sup': ativo.lim_sup, 'lim_inf': ativo.lim_inf})
        
    context = {
    'form': form,
    'ativo': ativo,
    }

    return render(request, 'ativo/update.html', context)


#Delete ativo view
@login_required(login_url='login')
def delete_ativo(request, pk):
    ativo = get_object_or_404(Ativo, pk=pk)
    user = request.user

    if request.method == 'POST':
        ativo.delete()
        return redirect('profile', pk=user.id)

    context = {
    'ativo': ativo,
    }

    return render(request, 'ativo/delete.html', context)


#List ativo view
@login_required(login_url='login')
def hist_ativo(request,pk):
    ativo = get_object_or_404(Ativo, pk=pk)
    hist_list = HistAtivo.objects.filter( fk_ativo__fk_user__id=request.user.id, fk_ativo=pk ).order_by('-data_atualizacao')
    
    context = {
    'hist_list': hist_list,
    'ativo': ativo
    }

    return render(request, 'ativo/historico/historico.html', context)