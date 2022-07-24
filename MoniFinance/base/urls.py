from django.urls import path
from . import views


urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    path('create-ativo',views.create_ativo, name='create-ativo'),
    path('update-ativo/<int:pk>',views.update_ativo, name='update-ativo'),
    path('delete-ativo/<int:pk>',views.delete_ativo, name='delete-ativo'),
    path('historico/<int:pk>',views.hist_ativo, name='ativo-hist')
]
