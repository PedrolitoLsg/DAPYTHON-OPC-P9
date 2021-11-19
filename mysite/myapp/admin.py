from django.contrib import admin
from myapp.models import Ticket, Review, UserFollows
# Register your models here.
admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollows)