from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout, login
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'app'

urlpatterns = [
    path('', views.connexion, name='connexion'),
    path('inscription/', views.inscription, name='inscription'),
    path('flux/', views.flux, name='flux'),
    path('posts/', views.posts, name='posts'),
    path('creationticket/', views.creationticket, name='creationticket'),
    path('creationticket/<id_ticket>', views.creationticket, name='creationticket'),
    path('deleteticket/<id_ticket>', views.deleteticket, name='deleteticket'),
    path('creationreview/<id_ticket>', views.creationreview, name='creationreview'),
    path('reviewfromscratch/', views.reviewfromscratch, name='reviewfromscratch'),
    path('modifyreview/<id_review>', views.modifyreview, name='modifyreview'),
    path('deletereview/<id_review>', views.deletereview, name='deletereview'),
    path('abonnements/', views.abonnements, name='abonnements'),
    path('unfollow/<id_user>', views.unfollow, name='unfollow'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
