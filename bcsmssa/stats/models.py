from django.core.validators import validate_comma_separated_integer_list
from django.contrib.auth.models import User
from django.db import models
import uuid

class UserProfile( models.Model ):
    user = models.OneToOneField(User)

class Client( models.Model ):
    client_number       = models.IntegerField(verbose_name="Client Number", unique=True)
    date_of_birth       = models.DateField('Date of Birth (yyyy-mm-dd)')
    age                 = models.IntegerField(null=True, blank=True, default=None, verbose_name="Age")
    number_of_abuses    = models.IntegerField(null=True, blank=True, default=None, verbose_name="Number of Abuses")
    
    def __str__(self):
        return str(self.client_number)

    # Iterate over field values. 
    def __iter__(self):
        for field in self._meta.fields:
            if field.name != 'id':
                yield field.value_to_string(self)
        
    @classmethod
    def create(cls, num, dob, age, num_abuses):
        client = Client(client_number=num, 
                        date_of_birth=dob, 
                        age=age, 
                        number_of_abuses=num_abuses)
        client.save()

    # Create bins for pie chart based on user ages
    @classmethod
    def age_data(cls):
        # Array contains age intervals
        # Each interval is 10 years starting at 0-9
        ages = [0,0,0,0,0,0]
        for client in Client.objects.all():
            age = client.age
            if age:
                if age <= 9: ages[0] += 1
                elif age <= 19: ages[1] += 1
                elif age <= 29: ages[2] += 1
                elif age <= 39: ages[3] += 1
                elif age <= 49: ages[4] += 1
                else: ages[5] += 1
        data =  [
            ['Age', 'Range'],
            ['Less than 10', ages[0]],
            ['10 - 19', ages[1]],
            ['20 - 29', ages[2]],
            ['30 - 39', ages[3]],
            ['40 - 49', ages[4]],
            ['50+', ages[5]]
        ]
        return data


class RequestedService(models.Model):
    # Client Foreign Key
    client1 = models.OneToOneField(
         Client,
         on_delete=models.CASCADE,
         primary_key=True,
         verbose_name='Associated Client Number'
    )

    # Fields
    victim_services     = models.BooleanField(blank=True, verbose_name="Victim Services")         
    individual_therapy  = models.BooleanField(blank=True, verbose_name="Individual Therapy")         
    group_therapy       = models.IntegerField(blank=True, null=True, verbose_name="Group Therapy")           

    
    def __str__(self):
        return str(self.client1.client_number)

    # Iterate over field values. 
    def __iter__(self):
        for field in self._meta.fields:
            val = field.value_to_string(self)
            if field.name == 'client1':
                yield Client.objects.get(pk=int(val))
            else:
                yield val


    @classmethod
    def create(cls, vs, it, gt, client):
        RequestedService(victim_services=vs,
                                individual_therapy=it, 
                                group_therapy=gt, 
                                client1 = client).save()



    # Create bins for pie chart based on requested service
    @classmethod
    def service_data(cls):
        # S corresponds to services in order
        # S[0] is victim_services, etc
        S = [0,0,0]
        for service in RequestedService.objects.all():
            if service.victim_services:
                S[0] += 1
            if service.individual_therapy:
                S[1] += 1
            if service.group_therapy:
                S[2] += 1
        data = [
            ['Service', 'Count'],
            ['Victim Services', S[0]],
            ['Individual Therapy', S[1]],
            ['Group Therapy', S[2]]
        ]
        return data



class Referral(models.Model):
    # Client Foreign Key
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='Associated Client Number'
    )

    # Fields
    web                     = models.BooleanField(default=False, blank=True, verbose_name="Web")
    social_service          = models.BooleanField(default=False, blank=True, verbose_name="Social Service")
    health_practitioner     = models.BooleanField(default=False, blank=True, verbose_name="Health Practitioner")
    alcoholics_anonymous    = models.BooleanField(default=False, blank=True, verbose_name="Alcoholics Anonymous")
    drug_treatment_group    = models.BooleanField(default=False, blank=True, verbose_name="Drug Treatment Group")
    advertisement           = models.BooleanField(default=False, blank=True, verbose_name="Advertisement")
    other                   = models.CharField(max_length=30, blank=True, verbose_name="Other")

    
    def __str__(self):
        return str(self.client.client_number)

    # Iterate over field values. 
    def __iter__(self):
        for field in self._meta.fields:
            val = field.value_to_string(self)
            if field.name == 'client1':
                yield Client.objects.get(pk=int(val))
            else:
                yield val


    @classmethod
    def create(cls, web, ss, hp, aa, dtg, ad, other, client):
        Referral(web=web, 
                social_service=ss,
                health_practitioner=hp,
                alcoholics_anonymous=aa,
                drug_treatment_group=dtg,
                advertisement=ad,
                other=other,
                client=client).save()

    # Return data on how many referrals of each type are given
    @classmethod
    def referral_data(cls):
        # Array indices correspond to type of referral
        # R[0] is count of web referrals, R[1] of social_service, etc
        R = [0,0,0,0,0,0,0]
        for referral in Referral.objects.all():
            if referral.web:
                R[0] += 1
            if referral.social_service:
                R[1] += 1
            if referral.health_practitioner:
                R[2] += 1
            if referral.alcoholics_anonymous:
                R[3] += 1
            if referral.drug_treatment_group:
                R[4] += 1
            if referral.advertisement:
                R[5] += 1
            if referral.other:
                R[6] += 1
        data = [
            ['Referral Type', 'Count'],
            ['Web', R[0]],
            ['Social Service', R[1]],
            ['Health Practitioner', R[2]],
            ['Alcoholics Anonymous', R[3]],
            ['Drug Treatment Group', R[4]],
            ['Advertisement', R[5]],
            ['Other', R[6]]
        ]
        return data


class Abuse ( models.Model ):
    # Client Foreign Key
    client              = models.ForeignKey( 
        Client, on_delete = models.CASCADE, 
        verbose_name='Associated Client Number' 
    )

    # Fields
    start_date          = models.CharField(max_length=4, blank=True, verbose_name="Start Date (Year)")
    stop_date           = models.CharField(max_length=4, blank=True, verbose_name="Start Date (Year)")
    role_of_abuser      = models.IntegerField(null=True, blank=True, verbose_name="Role of Abuser")
    reported_date       = models.CharField(max_length=4, blank=True, verbose_name="Reported Date (Year)")
    family_context      = models.CharField(max_length=12, blank=True, verbose_name="Family Context")

    def __str__(self):
        return str(self.client)

    # Iterate over field values. 
    def __iter__(self):
        for field in self._meta.fields:
            if field.name != 'id':
                val = field.value_to_string(self)
                if field.name == 'client1':
                    yield Client.objects.get(pk=int(val))
                else:
                    yield val


    @classmethod
    def create(cls, client, start, stop, role, rep_date, context):
        abuse = Abuse(client=client, 
                        start_date=start,
                        stop_date=stop,
                        role_of_abuser=role,
                        reported_date=rep_date,
                        family_context=context)
        abuse.save()

class CurrentSituation( models.Model ):
    # Abuse Foreign key
    abuse               = models.ForeignKey( Abuse, on_delete=models.CASCADE, verbose_name="Associated Client ID")
    
    # Fields
    medication1         = models.CharField(max_length=50,   blank=True, verbose_name="Medication 1")
    purpose1            = models.CharField(max_length=150,  blank=True, verbose_name="Purpose of 1st Med.")
    medication2         = models.CharField(max_length=50,   blank=True, verbose_name="Medication 2")
    purpose2            = models.CharField(max_length=150,  blank=True, verbose_name="Purpose of 2nd Med.")
    sexual_orientation  = models.CharField(max_length=10,   blank=True, verbose_name="Sexual Orientation" )
    income              = models.IntegerField(null=True,    blank=True, verbose_name="Income")
    level_of_education  = models.IntegerField(null=True,    blank=True, verbose_name="Level of Education")
    profession          = models.CharField(max_length=50,   blank=True, verbose_name="Profession")
    in_treatment        = models.BooleanField(              blank=True, verbose_name="In Treatment?")
    

    def __str__(self):
        return str(self.abuse)

    # Iterate over field values. 
    def __iter__(self):
        for field in self._meta.fields:
            if field.name != 'id':
                val = field.value_to_string(self)
                if field.name == 'abuse':
                    yield Abuse.objects.get(pk=int(val))
                else:
                    yield val


    @classmethod
    def create(cls, med1, purp1, med2, purp2, so, income, loe, prof, treament, abuse):
        sitch = CurrentSituation(medication1    =med1, 
                                         purpose1       =purp1, 
                                         medication2    =med2,
                                         purpose2       =purp2,
                                         sexual_orientation=so,
                                         income         =income, 
                                         level_of_education=loe,
                                         profession     =prof, 
                                         in_treatment   =treament, 
                                         abuse          =abuse)
        sitch.save()

class InviteKey( models.Model ):
    id = models.CharField(max_length=6, primary_key=True)

    def as_json(self):
        return dict(code=self.id)
