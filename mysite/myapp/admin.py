from django.contrib import admin
from .models import Ticket, Review, Product
# Register your models here.
admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(Product)
