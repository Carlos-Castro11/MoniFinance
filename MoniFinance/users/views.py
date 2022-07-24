from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib import messages
from base.models import Ativo, HistAtivo
from .forms import UserCreate, UserUpdate
from django.contrib.auth.decorators import login_required



def LoginPage(request):

    page = 'login'
    flag = 0
    if request.user.is_authenticated: 
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.filter(username=username)
        except:
            messages.error(request, 'Usuário não encontrado.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            flag = 1

    context = {'page': page, 'flag': flag}
    return render(request, 'base/login_register.html', context)


def LogoutUser(request):
    logout(request)
    return redirect('home')


def RegisterUser(request):
    form = UserCreate()

    if request.method == 'POST':
        form = UserCreate(request.POST)
        if form.is_valid():
            users = User.objects.create(
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
                username=form.cleaned_data['username'],
                profession=form.cleaned_data["profession"],
            )
            users.set_password(form.cleaned_data["password1"])
            users.save()
            
            login(request, users)
            return redirect('home')
            
    return render(request, 'base/login_register.html', {'form': form})


def ProfilePage(request, pk):
    user = User.objects.get(id=pk)
    ativo = Ativo.objects.filter(fk_user = request.user.id)
    result = HistAtivo.objects.filter(fk_ativo__in = ativo, ultimo_hist = True)
    
    context = {
    'ativo_list': result,
    }

    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def UpdateUser(request):
    user = request.user
    form = UserUpdate()

    if request.method == 'POST':
        form = UserUpdate(request.POST)
        if form.is_valid():
            user.username=form.cleaned_data["username"]
            user.first_name=form.cleaned_data["first_name"]
            user.last_name=form.cleaned_data["last_name"]
            user.email=form.cleaned_data["email"]
            user.profession=form.cleaned_data["profession"]
            user.save()
            
            return redirect('profile', pk=user.id)

    return render(request, 'base/update_user.html', {'form': form})

