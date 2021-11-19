from django.shortcuts import render
from django.http import HttpResponse
from .forms import ConnectForm, NewUserForm, CreateTicketForm, CreateReviewForm, SubscriptionForm
from django.contrib.auth import logout, login
#from models import Ticket, Review, UserFollows

# Create your views here.
#Sur toutes les pages#

def logout_view(request):
    logout(request)
    return redirect('templates:connexion')

#Fin de sur toutes les pages#
#Page d'accueil#

def get_pair_to_connect(request):
    if request.method == 'POST':
        form = ConnectForm(request.POST)
        if form.is_valid():
            user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('templates/flux/')
            else:
                form.add_error(
                    'username',
                    "Ce compte n'existe pas ou vous vous êtes trompés dans vos credentials.")

    # If a GET (or any other method) we'll create a blank form
    else:
        form = ConnectForm()
    return render(request, 'connexion.html', {'form': form})


#Fin Page d'accueil#


def inscription(request):
    #changer le nom en obtenir_inscription_info
    # faire un form dans forms.py pour ca
    if request.method == 'Post':
        form = NewUserForm(request.POST)
        if form.isvalid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé pour utilisateur {username}')
            return redirect ('flux')
    else:
        form = NewUserForm()
    return render(request, 'inscription.html', {'form': form})



# ce truc juste en dessous il faudra le mettre en dessous de chaque fonction permettant d'accéder à du dossier ou il doit y avoir du monde de connecté
#@login_required(login_url='templates:connexion')
def flux(request):
    return render(request, 'flux.html',)

def creationticket(request):
    return render(request, 'creationticket.html', )

def creationcritique(request):
    return render(request, 'creationcritique.html', )

def critiquefromscratch(request):
    return render(request, 'critiquefromscratch.html', )

def abonnements(request):
    return render(request, 'abonnements.html', )

def main(request):
    pass


# Page de déconnexion #
def logout(request):
    return