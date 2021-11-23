from django.shortcuts import render, redirect
from django.http import HttpResponse
#from .forms import ConnectForm, NewUserForm, CreateTicketForm, CreateReviewForm, SubscriptionForm
from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Ticket, Review, UserFollows

#from models import Ticket, Review, UserFollows

# Create your views here.
#Sur toutes les pages#

# Page de déconnexion #
@login_required()
def deconnexion(request):
    if request.method == 'POST':
        logout(request)
        return redirect('app:connexion')

#Fin de sur toutes les pages#
#Page d'accueil#

def connexion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            #logger l'user
            user = form.get_user()
            login(request, user)
            return redirect('app:flux')
    else:
        form = AuthenticationForm()
    return render(request, 'connexion.html', {'form': form})
#Fin Page d'accueil#


def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #log the user in
            login(request, user)
            return redirect('app/flux')
    else:
        form = UserCreationForm()
    return render(request, 'inscription.html', {'form': form})




# ce truc juste en dessous il faudra le mettre en dessous de chaque fonction permettant d'accéder à du dossier ou il doit y avoir du monde de connecté
#@login_required(login_url='templates:connexion')

@login_required(login_url='app')
def flux(request):
    tickets = Ticket.objects.all().order_by('time_created')
    return render(request, 'flux.html', {'tickets': tickets})

@login_required()
def abonnements(request):
    follows = UserFollows.objects.all().order_by('user')
    return render(request, 'abonnements.html', {'follows or followed by': follows})

@login_required()
def posts(request):
    return render(request, 'posts.html', )

@login_required()
def creationticket(request):
    return render(request, 'creationticket.html', )

@login_required()
def creationcritique(request):
    return render(request, 'creationcritique.html', )

@login_required()
def critiquefromscratch(request):
    return render(request, 'critiquefromscratch.html', )




