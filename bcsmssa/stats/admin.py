from django.contrib import admin

# Register your models here.
from .models import Client ,Abuse, CurrentSituation, RequestedService, Referral

admin.site.register(Client)
admin.site.register(Abuse)
admin.site.register(CurrentSituation)
admin.site.register(RequestedService)          
admin.site.register(Referral)                 