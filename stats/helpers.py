from .models import Client, RequestedService, Referral, Abuse, CurrentSituation 
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart, ColumnChart, PieChart
from graphos.sources.model import ModelDataSource


def create_models(form):
    """
    Create models from form data 
    """
    # Must create client before getting client
    create_client(form)
    client = Client.objects.filter(client_number=form.cleaned_data['client_number'])[0]
    create_services(form, client)
    create_referral(form, client)
    # Create abuse before getting abuse
    create_abuse(form, client)
    abuse = Abuse.objects.filter(client=client)[0]
    create_current_situation(form, abuse)


def create_client(form):
    """
    Create new client from form data
    """
    client_number   = form.cleaned_data['client_number']
    dob             = form.cleaned_data['date_of_birth']
    age             = form.cleaned_data['age']
    number_abuses   = form.cleaned_data['number_of_abuses']
    Client.create(client_number,dob,age,number_abuses)

def create_services(form, client):  
    """
    Create services requested from form data
    """
    vic_services    = form.cleaned_data['victim_services']
    ind_therapy     = form.cleaned_data['individual_therapy']
    gp_therapy      = form.cleaned_data['group_therapy']
    RequestedService.create(vic_services,ind_therapy,gp_therapy,client)

def create_referral(form, client):
    """
    Create new referral model from form info
    """
    web             = form.cleaned_data['web']
    ss              = form.cleaned_data['social_service']
    hp              = form.cleaned_data['health_practitioner']
    aa              = form.cleaned_data['alcoholics_anonymous']
    dtg             = form.cleaned_data['drug_treatment_group']
    ad              = form.cleaned_data['advertisement']
    other_referral  = form.cleaned_data['other_referral']
    Referral.create(web,ss,hp,aa,dtg,ad,other_referral,client)


def create_abuse(form, client):
    """
    Create new abuse model base off form data
    """
    start_date          = form.cleaned_data['start_date']
    stop_date           = form.cleaned_data['stop_date']
    role_of_abuser      = form.cleaned_data['role_of_abuser']
    reported_date       = form.cleaned_data['reported_date']
    family_context      = form.cleaned_data['family_context']
    Abuse.create(client,start_date,stop_date,role_of_abuser,reported_date,family_context)

def create_current_situation(form, abuse):
    """
    Create client_current_situation object from form data
    """
    medication1         = form.cleaned_data['medication1']  
    purpose1            = form.cleaned_data['purpose1']
    medication2         = form.cleaned_data['medication2']
    purpose2            = form.cleaned_data['purpose2']
    sexual_orientation  = form.cleaned_data['sexual_orientation']
    income              = form.cleaned_data['income']
    level_of_education  = form.cleaned_data['level_of_education']
    profession          = form.cleaned_data['profession']
    in_treatment        = form.cleaned_data['in_treatment']
    CurrentSituation.create(medication1, 
                                    purpose1, 
                                    medication2,
                                    purpose2, 
                                    sexual_orientation,
                                    income, 
                                    level_of_education, 
                                    profession, 
                                    in_treatment, 
                                    abuse)

def basic_stats():
    """
    Get basic stats for homepage
    """
    stats = {}
    client_count = Client.objects.all().count()
    num_abuses = Client.total_abuses()
    stats['num_clients'] = client_count
    stats['num_abuses'] = num_abuses
    stats['avg_abuses'] = round(float(num_abuses)/client_count,2) if client_count!=0 else 0
    return stats


def charts():
    """ 
    Generate all charts for homepage
    """
    context = {}
    context['age_vs_abuses'] = age_vs_abuse_chart()
    context['clients_by_age'] = ages()
    context['service_counts'] = services()
    context['referral_counts'] = referrals()
    return context

def age_vs_abuse_chart():
    """
    Create Age vs abuse chart
    """
    clients = Client.objects.all()
    data_source = ModelDataSource(clients, fields=['age', 'number_of_abuses'])
    return ColumnChart(data_source, options={'title': 'Age and Number of Abuses', 
                                            'legend': 'none', 
                                            'width': 650,
                                            'vAxis': {'title': 'Number of Abuses'},
                                            'hAxis': {'title': 'Age'}})

def ages():
    """
    Return pie chart of client ages' 
    """   
    data_source = SimpleDataSource(data=Client.age_data())
    return PieChart(data_source, options={'title': "Client Age"})

def services():
    """
    Return pie chart demonstrating how often each service is requested
    """
    data_source = SimpleDataSource(data=RequestedService.service_data())
    return PieChart(data_source, options={'title': "Services", 
                                            'pieHole': 0.4, 
                                            'width': 650,})


def referrals():
    """
    Return pie chart conveying referral info
    """
    data_source = SimpleDataSource(data=Referral.referral_data())
    return PieChart(data_source, options={'title': "Referral Type",
                                            'width': 650,
                                            'is3D': True})

