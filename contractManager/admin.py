from django.contrib import admin

from .models import Role, CustomUser, Client, Contract, Event

# Register your models here.

admin.site.register(Role)
admin.site.register(CustomUser)
admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)
