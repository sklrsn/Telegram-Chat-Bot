from django.contrib import admin
from .models import ApplicationUser, MessageHolder

admin.site.register(ApplicationUser)
admin.site.register(MessageHolder)
