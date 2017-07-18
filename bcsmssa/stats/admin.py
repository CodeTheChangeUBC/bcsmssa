from django.contrib import admin
from .models import Client ,Abuse, CurrentSituation, RequestedService, Referral


# Admin class for Client Model
class ClientAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['client_number', 'date_of_birth', 'age', 'number_of_abuses']}),
	]
	list_display = ('client_number', 'date_of_birth', 'age', 'number_of_abuses')
	list_filter = ['client_number', 'date_of_birth', 'age', 'number_of_abuses']
	search_fields = ['client_number', 'date_of_birth', 'age', 'number_of_abuses']

# Admin Class for Abuse model
class AbuseAdmin(admin.ModelAdmin):
	fieldsets = [
		('Client', {'fields':['client']}),
		('Details', {'fields': ['start_date', 'stop_date', 'role_of_abuser', 'reported_date', 'family_context']}),
	]
	list_display = ['client', 'start_date', 'stop_date', 'role_of_abuser', 'reported_date', 'family_context']
	list_filter = list_display
	search_fields = ['client__client_number', 'start_date', 'stop_date', 'role_of_abuser', 'reported_date', 'family_context']

# Admin class for CurrentSituation model
class CSAdmin(admin.ModelAdmin):
	fieldsets = [
		('Abuse', {'fields': ['abuse']}),
		('Details', {'fields': ['medication1', 'purpose1', 'medication2', 'purpose2', 
								'sexual_orientation', 'income', 'level_of_education',
								'profession', 'in_treatment']})
	]
	list_display = ['abuse', 'medication1', 'purpose1', 'medication2', 'purpose2', 
					'sexual_orientation', 'income', 'level_of_education',
					'profession', 'in_treatment']
	list_filter = list_display
	search_fields = ['abuse__client__client_number', 'medication1', 'purpose1', 'medication2', 'purpose2', 
					'sexual_orientation', 'income', 'level_of_education',
					'profession', 'in_treatment']
	

class RSAdmin(admin.ModelAdmin):
	fieldsets = [
		('Client', {'fields': ['client1']}),
		('Service', {'fields': ['victim_services', 'individual_therapy', 'group_therapy']}),
	]
	list_display = ['client1', 'victim_services', 'individual_therapy', 'group_therapy']
	list_filter = list_display
	search_fields = ['client1__client_number', 'victim_services', 'individual_therapy', 'group_therapy']

class ReferralAdmin(admin.ModelAdmin):
	fieldsets = [
		('Client', {'fields': ['client']}),
		('Referral Info', {'fields': ['web', 'social_service', 'health_practitioner',
										'alcoholics_anonymous', 'drug_treatment_group',
										'advertisement', 'other']}),
	]
	list_display = ['client', 'web', 'social_service', 'health_practitioner',
					'alcoholics_anonymous', 'drug_treatment_group',
					'advertisement', 'other']
	list_filter = list_display
	search_fields = ['client__client_number', 'web', 'social_service', 'health_practitioner',
					'alcoholics_anonymous', 'drug_treatment_group',
					'advertisement', 'other']




admin.site.register(Client, ClientAdmin)
admin.site.register(Abuse, AbuseAdmin)
admin.site.register(CurrentSituation, CSAdmin)
admin.site.register(RequestedService, RSAdmin)          
admin.site.register(Referral, ReferralAdmin)                 

