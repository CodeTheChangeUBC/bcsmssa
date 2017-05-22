from .models import * 

def create_models(form):
	"""
	Create models from form data 
	"""
	client_number = form.cleaned_data['client_number']
	dob = form.cleaned_data['date_of_birth']
	age = form.cleaned_data['age']
	number_abuses = form.cleaned_data['number_of_abuses']
	Client.create(client_number,dob,age,number_abuses)

	vic_services = form.cleaned_data['victim_services']
	ind_therapy = form.cleaned_data['individual_therapy']
	gp_therapy = form.cleaned_data['group_therapy']
	ServicesRequested.create(vic_services,ind_therapy,gp_therapy)
