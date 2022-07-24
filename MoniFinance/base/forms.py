from django import forms as form_django
from django.core.exceptions import ValidationError


class AtivoCreate(form_django.Form):
    
    b3 = form_django.CharField(label='Código do Ativo:', widget=form_django.widgets.TextInput(attrs={'placeholder' : 'Ex: MGLU3'}))
    lim_sup = form_django.FloatField(label='Limite superior:', widget=form_django.widgets.TextInput(attrs={'placeholder' : 'Ex: 15'}))
    lim_inf = form_django.FloatField(label='Limite inferior:',widget=form_django.widgets.TextInput(attrs={'placeholder' : 'Ex: 5'}))

    
    def clean(self):
        cleaned_data = self.cleaned_data
        lim_sup = cleaned_data.get('lim_sup')
        lim_inf = cleaned_data.get('lim_inf')

        if lim_inf > lim_sup:
            raise form_django.ValidationError('O limite inferior não pode ser maior que o superior...')
        elif lim_sup <= 0:
            raise form_django.ValidationError('Limite superior inválido...')
        elif lim_inf < 0:
            raise form_django.ValidationError('Limite inferior inválido...')
            
        return cleaned_data

class AtivoUpdate(form_django.Form):

    lim_sup = form_django.FloatField(label='Limite para venda:', widget=form_django.widgets.TextInput(attrs={'placeholder' : 'Ex.: 20'}))
    lim_inf = form_django.FloatField(label='Limite para compra:',widget=form_django.widgets.TextInput(attrs={'placeholder' : 'Ex.: 5'}))

    
    def clean(self):
        cleaned_data = self.cleaned_data # individual field's clean methods have already been called
        lim_sup = cleaned_data.get('lim_sup')
        lim_inf = cleaned_data.get('lim_inf')

        if lim_inf > lim_sup:
            raise form_django.ValidationError('O limite inferior não pode ser maior que o superior...')
        elif lim_sup <= 0:
            raise form_django.ValidationError('Limite superior inválido...')
        elif lim_inf < 0:
            raise form_django.ValidationError('Limite inferior inválido...')
            
        return cleaned_data
