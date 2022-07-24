from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutUser, name='logout'),
    path('register/', views.RegisterUser, name='register'),
    path('profile/<str:pk>/', views.ProfilePage, name='profile'),
    path('update-user/', views.UpdateUser, name='update-user'),

]
