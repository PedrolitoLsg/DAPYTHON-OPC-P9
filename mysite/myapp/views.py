from django.shortcuts import render
from django.http import HttpResponse
from models import Ticket, Review, Product


def index(request):
    return HttpResponse("Hello World")

# Create your views here.
