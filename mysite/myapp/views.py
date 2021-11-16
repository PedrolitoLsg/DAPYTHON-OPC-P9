from django.shortcuts import render
from django.http import HttpResponse
#from models import Ticket, Review, UserFollows


def index(request):
    return HttpResponse("Hello World")

# Create your views here.
