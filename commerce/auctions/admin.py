from django.contrib import admin

# Register your models here.
from .models import User, Listing, Bid, Comment

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)