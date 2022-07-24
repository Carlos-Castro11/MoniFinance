from django.contrib.auth import forms as form_auth
from django import forms as form_django
from django.core.exceptions import ValidationError
from .models import User


class UserCreate(form_django.Form):
    
    first_name = form_django.CharField(label='Primeiro nome:', widget=form_django.widgets.TextInput(attrs={'placeholder' : 'Digite seu primeiro nome'}))
    last_name = form_django.CharField(label='Último nome:', widget=form_django.widgets.TextInput(attrs={'placeholder' : 'Digite seu último nome'}))
    email = form_django.EmailField(label='E-mail:',widget=form_django.widgets.EmailInput(attrs={'placeholder' : 'Ex.: contato@inoa.com.br'}))
    username = form_django.CharField(label='Usuário:', widget=form_django.widgets.TextInput(attrs={'placeholder' : 'Digite um usuário'}))
    password1 = form_django.CharField(widget=form_django.widgets.PasswordInput(attrs={'placeholder' : 'Digite uma Senha'}), label='Senha:')
    password2 = form_django.CharField(widget=form_django.widgets.PasswordInput(attrs={'placeholder' : 'Confirme a senha'}), label='Confirmação de senha:')
    profession = form_django.CharField(label='Profissão:', widget=form_django.widgets.TextInput(attrs={'placeholder' : 'Ex.: Desenvolvedor'}))

   
    def clean_username(self):
        user_name = self.cleaned_data['username']
        
        if User.objects.filter(username__exact=user_name).count() > 0:
            raise ValidationError('Este usuário já esta sendo utilizado...')

        return user_name

    def clean(self):
        
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise form_django.ValidationError("Senhas inválidas...")

        return cleaned_data


class UserUpdate(form_django.Form):
   
    username = form_django.CharField(label='Usuário:')
    first_name = form_django.CharField(label='Primeiro nome:')
    last_name = form_django.CharField(label='Último nome:')
    email = form_django.EmailField(label='E-mail:')
    profession = form_django.CharField(label='Profissão:')

class UserChangeForm(form_auth.UserChangeForm):
    class Meta(form_auth.UserChangeForm.Meta):
        model = User

class UserCreationForm(form_auth.UserCreationForm):
    class Meta(form_auth.UserCreationForm.Meta):
        model = User

