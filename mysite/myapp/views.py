from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserFollowsForm, CreateTicketForm, CreateReviewForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Ticket, Review, UserFollows
from itertools import chain
from django.urls import reverse


#from models import Ticket, Review, UserFollows


def deconnexion(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'deconnexion.html')


def connexion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('app:flux')
    else:
        form = AuthenticationForm()
    return render(request, 'connexion.html', {'form': form})


def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)
            login(request, new_user)
            return redirect('app:flux')
    else:
        form = UserCreationForm()
    return render(request, 'inscription.html', {'formnew': form})

# ce truc juste en dessous il faudra le mettre en dessous de chaque fonction permettant d'accéder à du dossier ou il doit y avoir du monde de connecté
#@login_required(login_url='templates:connexion')



@login_required(login_url='app:connexion')
def abonnements(request):
    if request.method == 'GET':
        form = UserFollowsForm()
        user_follows= UserFollows.followed_user
        user_follows = UserFollows.objects.filter(user=request.user)
        print(user_follows)
        infos = {'details:': user_follows}
        return render(request, 'abonnements.html', infos)
    elif request.method == 'POST':
        form = UserFollowsForm(request.POST, request.FILES)
        if form.is_valid():
            followed_user = form.cleaned_data['followed_user']


    #list = UserFollows.objects.filter(user_info == request.user)
    return render(request, 'abonnements.html', {'follows': list})


@login_required(login_url='app:connexion')
def display_followed(request):
    current_user = request.user
    followed = UserFollows.objects.all().order_by('user')
    return render(request, 'abonnements.html', {'follows or followed by': followed})


def follow(request):
    pass


#Flux page
@login_required(login_url="app:connexion")
def flux(request):
    #doit contenir les derniers tickets et reviews des utilisateurs suivis, Last In on Top
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    context = {'tickets': tickets, 'reviews': reviews}
    return render(request, 'flux.html', context)


@login_required(login_url='app:connexion')
def posts(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'posts.html', {'tickets': tickets})


@login_required(login_url='app:connexion')
def creationticket(request, id_ticket=None):
    instance_ticket = Ticket.objects.get(pk=id_ticket) if id_ticket is not None else None
    #   displays the page
    if request.method == 'GET':
        form = CreateTicketForm(instance=instance_ticket)
        return render(request, 'creationticket.html', {'form': form})
    # captures the data entered, saves it to db and redirects the user to flux
    elif request.method == 'POST':
        form = CreateTicketForm(request.POST, instance=instance_ticket)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('app:flux')


@login_required(login_url='app:connexion')
def deleteticket(request, id_ticket):
    if request.method == "POST":
        ticket = get_object_or_404(Ticket, id=id_ticket)
        if ticket:
            ticket.delete()
            return redirect('app:posts')


@login_required(login_url='app:connexion')
def deletereview(request, id_review):
    if request.method == 'POST':
        review = get_object_or_404(Review, id=id_review)
        review.delete()
        return redirect('app:posts')
# End of Page Creation Ticket


#Page Creation Critique (permet de créer et modifier une critique)
@login_required(login_url='app:connexion')
def creationreview(request, id_review=None, id_ticket=None):
    instance_review = Review.objects.get(pk=id_review) if id_review is not None else None
    instance_ticket = Ticket.objects.get(pk=id_ticket)
    if request.method == 'GET':
        if instance_review is None:
            form_review = CreateReviewForm()
            ticket = instance_ticket
            context = {'ticket': ticket, 'formreview': form_review}
            return render(request, 'creationcritique.html', context)
        elif instance_review is not None:
            pass
            # Modifier une review d'un ticket existant, display ticket
            # Entreti
        elif instance_review is None and instance_ticket is None:
            pass
            # créer review et ticket, soit launch createreviewfromscratch(request)

        form = CreateReviewForm(instance=instance_review)
        return render(request, 'creationcritique.html', locals())
    elif request.method == 'POST':
        form = CreateReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
            return redirect('app:flux')


@login_required(login_url='app:connexion')
def reviewfromscratch(request):
    if request.method =="GET":
        form_ticket = CreateTicketForm()
        form_review = CreateReviewForm()
        context = {'formticket': form_ticket, 'formreview': form_review}
        return render(request, 'critiquefromscratch.html', context)
    elif request.method == "POST":
        form_ticket=CreateTicketForm(request.POST, request.FILES)
        form_review=CreateReviewForm(request.POST)
        if form_ticket.is_valid() and form_review.is_valid():
            form_ticket.instance.user = request.user
            new_ticket = form_ticket.save()
            form_review.instance.user = request.user
            form_review.instance.ticket = Ticket.objects.get(pk=new_ticket.pk)
            form_review.save()
            return redirect('app:flux')