#from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout, login

app_name = 'app'
urlpatterns = [
    url(r'^$', views.connexion, name='connexion'),
    url('inscription/', views.inscription, name='inscription'),
    url('flux/', views.flux, name='flux'),
    url('creationticket/', views.creationticket, name='creationticket'),
    url('creationcritique/', views.creationcritique, name='creationcritique'),
    url('critiquefromscratch/', views.critiquefromscratch, name='critiquefromscratch'),
    url('abonnements/', views.abonnements, name='abonnements'),
    url('posts/', views.posts, name='posts'),
    url('deconnexion/', views.deconnexion, name='deconnexion'),
]