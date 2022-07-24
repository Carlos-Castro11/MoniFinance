from django.db import models
from django.contrib.auth.models import User

class Ativo(models.Model):
    b3 = models.CharField(max_length=10)
    nome_empresa = models.CharField(max_length=200)
    desc_empresa = models.CharField(max_length=200, blank=True)
    lim_inf = models.FloatField()
    lim_sup = models.FloatField()
    fk_user = models.ForeignKey('users.User',on_delete=models.CASCADE,null=True) 

    def __str__(self):
        return f'{self.id} | {self.fk_user.username} | {self.b3} | {self.nome_empresa} | {self.lim_sup} | {self.lim_inf}'

class HistAtivo(models.Model):
    fk_ativo = models.ForeignKey('Ativo',on_delete=models.CASCADE,null=True)
    valor = models.FloatField()
    data_atualizacao =  models.DateTimeField(null=True)
    porcentagem = models.FloatField()
    valor_anterior = models.FloatField()
    ultimo_hist = models.BooleanField(null=True)

    def __str__(self):
        return f'{self.id} | {self.fk_ativo.b3} | {self.fk_ativo.nome_empresa} | {self.valor} | {self.data_atualizacao} | {self.porcentagem} | {self.valor_anterior}'