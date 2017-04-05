from django.contrib import admin

# Register your models here.
from .models import Client ,Abuse, Client_Current_Situation, ServicesRequested, ReferredBy

admin.site.register(Client)
admin.site.register(Abuse)
admin.site.register(Client_Current_Situation)
admin.site.register(ServicesRequested)          #justAdded
admin.site.register(ReferredBy)                 #justAdded