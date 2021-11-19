from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout, login


urlpatterns = [
    path('', views.get_pair_to_connect, name='connexion'),
    path('inscription/', views.inscription, name='inscription'),
    path('flux/', views.flux, name='flux'),
    path('creationticket/', views.creationticket, name='creationticket'),
    path('creationcritique/', views.creationcritique, name='creationcritique'),
    path('critiquefromscratch/', views.critiquefromscratch, name='critiquefromscratch'),
    path('abonnements/', views.abonnements, name='abonnements'),
    path('main/', views.main, name='main'),
    #path('connexion/', auth_views.LoginView.as_view(template_name='connexion.html'), name='connexion'),
    path('deconnexion/', auth_views.LogoutView.as_view(template_name='deconnexion.html'), name='deconnexion'),
]