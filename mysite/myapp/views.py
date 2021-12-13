from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserFollowsForm, CreateTicketForm, CreateReviewForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Ticket, Review, UserFollows
from itertools import chain
from django.db.models import Value, CharField
from django.db import models
from django.urls import reverse


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


@login_required(login_url='app:connexion')
def abonnements(request):
    if request.method == 'GET':
        form = UserFollowsForm()
        collection = UserFollows.objects.filter(user=request.user)
        context = {'form': form, 'collection': collection}
        return render(request, 'abonnements.html', context)
    elif request.method == 'POST':
        form = UserFollowsForm(request.POST)
        if form.is_valid():
            relation = form.save(commit=False)
            relation.user = request.user
            relation.save()
            return redirect('app:abonnements')


@login_required(login_url='app:connexion')
def unfollow(request, id_user):
    if request.method == 'POST':
        relation = UserFollows.objects.get(user=request.user, followed_user=id_user)
        if relation:
            relation.delete()
    return redirect('app:abonnements')


# Flux page
@login_required(login_url="app:connexion")
def flux(request):
    x = request.user
    followed_users = UserFollows.objects.filter(user=x)
    followed = []
    for user in followed_users:
        followed.append(user.followed_user.id)

    # get tickets
    user_ticket = Ticket.objects.filter(user=x)
    user_ticket = user_ticket.annotate(content_type=Value('TICKET', CharField()))
    followers_tickets = Ticket.objects.filter(pk__in=followed)
    followers_tickets = followers_tickets.annotate(content_type=Value('TICKET', CharField()))
    # get reviews
    user_reviews = Review.objects.filter(user=x)
    user_reviews = user_reviews.annotate(content_type=Value('REVIEW', CharField()))
    followers_reviews = Review.objects.filter(pk__in=followed)
    followers_reviews = followers_reviews.annotate(content_type=Value('REVIEW', CharField()))

    for ticket in user_ticket:
        for review in user_reviews:
            if review.ticket == ticket:
                ticket.already_reviewed = True

    posts = sorted(chain(user_ticket, followers_tickets, user_reviews, followers_reviews), key=lambda post: post.time_created, reverse=True)
    return render(request, 'flux.html', {'posts': posts})


@login_required(login_url='app:connexion')
def posts(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    context = {'tickets': tickets, "reviews": reviews}
    return render(request, 'posts.html', context)


@login_required(login_url='app:connexion')
def creationticket(request, id_ticket=None):
    instance_ticket = Ticket.objects.get(pk=id_ticket) if id_ticket is not None else None
    if request.method == 'GET':
        form = CreateTicketForm(instance=instance_ticket)
        return render(request, 'creationticket.html', {'form': form})
    elif request.method == 'POST':
        form = CreateTicketForm(request.POST, request.FILES, instance=instance_ticket)
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


# Page Creation Critique (permet de créer et modifier une critique)
@login_required(login_url='app:connexion')
def creationreview(request, id_ticket):
    instance_ticket = Ticket.objects.get(pk=id_ticket) if id_ticket is not None else None
    if request.method == 'GET':
        form_review = CreateReviewForm()
        context = {'ticket': instance_ticket, 'formreview': form_review}
        return render(request, 'creationcritique.html', context)
    elif request.method == 'POST':
        form = CreateReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = instance_ticket
            review.user = request.user
            review.save()
            return redirect('app:flux')


@login_required(login_url='app:connexion')
def reviewfromscratch(request):
    if request.method == "GET":
        form_ticket = CreateTicketForm()
        form_review = CreateReviewForm()
        context = {'formticket': form_ticket, 'formreview': form_review}
        return render(request, 'critiquefromscratch.html', context)
    elif request.method == "POST":
        form_ticket = CreateTicketForm(request.POST, request.FILES)
        form_review = CreateReviewForm(request.POST)
        if form_ticket.is_valid() and form_review.is_valid():
            form_ticket.instance.user = request.user
            new_ticket = form_ticket.save()
            form_review.instance.user = request.user
            form_review.instance.ticket = Ticket.objects.get(pk=new_ticket.pk)
            form_review.save()
            return redirect('app:flux')


@login_required(login_url='app:connexion')
def modifyreview(request, id_review):
    instance_review = get_object_or_404(Review, pk=id_review)
    if request.method == 'GET':
        form_review = CreateReviewForm(instance=instance_review)
        context = {'form_review': form_review}
        return render(request, 'modifyreview.html', context)
    elif request.method == 'POST':
        form = CreateReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = Ticket.objects.get(pk=instance_review.ticket.id)
            review.save()
            return redirect('app:posts')
