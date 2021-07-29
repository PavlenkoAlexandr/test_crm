from django.contrib import admin
from .models import User, Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
