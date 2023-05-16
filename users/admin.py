from django.contrib import admin
from .models import CustomUser, UserConfirmation

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(UserConfirmation)