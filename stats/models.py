from django.core.validators import validate_comma_separated_integer_list
from django.contrib.auth.models import User
from django.db import models
from functools import reduce
import uuid
import datetime
import statistics


class UserProfile( models.Model ):
    user = models.OneToOneField(User)


class Client( models.Model ):
    # Track the user which created this client
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.SET_DEFAULT, verbose_name="Input by User")

    client_number       = models.IntegerField(verbose_name="Client Number", unique=True)
    date_of_birth       = models.DateField('Date of Birth (yyyy-mm-dd)')
    age                 = models.IntegerField(null=True, blank=True, default=None, verbose_name="Age at time of visit")
    number_of_abuses    = models.IntegerField(null=True, blank=True, default=None, verbose_name="Number of Abuses")


    def __str__(self):
        return str(self.client_number)

    # Iterate over field values. 
    def __iter__(self):
        for field in self._meta.fields:
            if field.name != 'id' and field.name != 'user':
                yield field.value_to_string(self)    
        
    @classmethod
    def create(cls, num, dob, age, num_abuses, user):
        client = Client(client_number=num, 
                        date_of_birth=dob, 
                        age=age, 
                        number_of_abuses=num_abuses, 
                        user=user)
        client.save()

    # Return total number of abuses    
    @classmethod
    def total_abuses(cls):
        return reduce(lambda x,y: x+y.number_of_abuses, Client.objects.all(), 0)

    # Return median of number of abuses
    @classmethod 
    def median_abuses(cls):
        abuses = list(map(lambda x: x.number_of_abuses, Client.objects.all()))
        return statistics.median(abuses)

    # Return average age of all clients
    @classmethod
    def average_age(cls):
        if Client.objects.all().count() == 0:
            return 0
        age = reduce(lambda x,y: x+y.age, Client.objects.all(), 0)
        return round(age/float(Client.objects.all().count()),2)

    # Return median age of all client
    @classmethod
    def median_age(cls):
        ages = list(map(lambda x: x.age, Client.objects.all()))
        return statistics.median(ages)


    # Return data for age vs number of abuses
    @classmethod
    def age_vs_abuse_data(cls):
        # Array contains age intervals
        # Each interval is 10 years starting at 0-9
        ages = [0,0,0,0,0,0]
        abuses = [0,0,0,0,0,0]
        for client in Client.objects.all():
            num = client.number_of_abuses
            if abuses:
                age = client.age
                if age:
                    if age <= 9: ages[0] += 1; abuses[0] += num
                    elif age <= 19: ages[1] += 1; abuses[1] += num
                    elif age <= 29: ages[2] += 1; abuses[2] += num
                    elif age <= 39: ages[3] += 1; abuses[3] += num
                    elif age <= 49: ages[4] += 1; abuses[4] += num
                    else: ages[5] += 1; abuses[5] += num
        return  [
            ['Age', 'Average Number of Abuses'],
            ['Less than 10', round(abuses[0]/float(ages[0]),2) if ages[0]!=0 else 0],
            ['10 - 19', round(abuses[1]/float(ages[1]),2) if ages[1]!=0 else 0],
            ['20 - 29', round(abuses[2]/float(ages[2]),2) if ages[2]!=0 else 0],
            ['30 - 39', round(abuses[3]/float(ages[3]),2) if ages[3]!=0 else 0],
            ['40 - 49', round(abuses[4]/float(ages[4]),2) if ages[4]!=0 else 0],
            ['50+',     round(abuses[5]/float(ages[5]),2) if ages[5]!=0 else 0],
        ]



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
        return  [
            ['Age', 'Range'],
            ['Less than 10', ages[0]],
            ['10 - 19', ages[1]],
            ['20 - 29', ages[2]],
            ['30 - 39', ages[3]],
            ['40 - 49', ages[4]],
            ['50+', ages[5]]
        ]

    # Override save method to store age on creation
    def save(self, *args, **kwargs):
        cur_date = datetime.datetime.now()
        dob = self.date_of_birth
        if not self.age: 
            self.age = cur_date.year - dob.year
            if dob.month >= cur_date.month:
                if dob.day > cur_date.day:
                    self.age -= 1
        super().save(*args,**kwargs)


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
    group_therapy       = models.BooleanField(blank=True, verbose_name="Group Therapy")           

    
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
            if field.name == 'client':
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
    stop_date           = models.CharField(max_length=4, blank=True, verbose_name="Stop Date (Year)")
    role_of_abuser      = models.CharField(max_length=100, null=True, blank=True, verbose_name="Role of Abuser")
    reported_date       = models.CharField(max_length=4, blank=True, verbose_name="Reported Date (Year)")
    family_context      = models.CharField(max_length=12, blank=True, verbose_name="Family Context")

    def __str__(self):
        return str(self.client.client_number)

    # Iterate over field values. 
    def __iter__(self):
        for field in self._meta.fields:
            if field.name != 'id':
                val = field.value_to_string(self)
                if field.name == 'client':
                    yield Client.objects.get(pk=int(val))
                else:
                    yield val

    # Return length of abuse (if recorded)
    def length_of_abuse(self):
        try: 
            return int(self.stop_date) - int(self.start_date) 
        except(ValueError):
            return 0

    # Return time until abuse was reported (if recorded)
    def length_until_recorded(self):
        try:
            return int(self.reported_date) - int(self.stop_date)
        except(ValueError):
            return 0

    # Return true if abuse has stop and end date
    def abuse_dates(self):
        if (not self.start_date) or (not self.stop_date):
            return 0
        return 1

    # Return true if abuse has reported and end dates
    def reported_dates(self):
        if (not self.reported_date) or (not self.stop_date):
            return 0
        return 1

    # Return median abuse length
    @classmethod
    def median_abuse_length(cls):
        lengths = list(map(lambda x: x.length_of_abuse(), Abuse.objects.all()))
        return statistics.median(lengths)


    # Return average time until abuse reported 
    @classmethod
    def avg_time_until_reported(self):
        count = reduce(lambda x,y: x+y.reported_dates(), Abuse.objects.all(),0)
        if count == 0:
            return 0
        length = reduce(lambda x,y: x+y.length_until_recorded(), Abuse.objects.all(), 0)
        return round(length/float(count),2)


    # Return average length of abuse
    @classmethod
    def average_abuse_length(cls):
        count = reduce(lambda x,y: x+y.abuse_dates(), Abuse.objects.all(),0)
        if count == 0:
            return 0
        length = reduce(lambda x,y: x+y.length_of_abuse(), Abuse.objects.all(), 0)
        return round(length/float(count),2)


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
    abuse               = models.ForeignKey( Abuse, on_delete=models.CASCADE, verbose_name="Associated Client Number")

    # Sexual Orientation Choices
    # Set variables for easier stats gathering
    het = "Heterosexual"
    hom = "Homosexual"
    bi = "Bisexual"
    trans = "Transexual"
    other = "Other"
    sex_choices = [ (het, het), 
                    (hom, hom), 
                    (bi, bi),
                    (trans, trans),
                    (other, other)]

    # Level of Education Choices
    # Set variables for stats gathering
    edu1 = "Secondary education or less"
    edu2 = "Diploma Program"
    edu3 = "Post-graduate - Bachelors"
    edu4 = "Post-graduate - Graduate"
    edu5 = "Post-graduate - Professional"
    edu6 = "Post-graduate - Doctorate"
    edu_choices = [ (edu1, edu1),
                    (edu2, edu2),
                    (edu3, edu3),
                    (edu4, edu4),
                    (edu5, edu5),
                    (edu6, edu6) ]

    # Income bracket choices
    inc1 = "Less than $20,000"
    inc2 = "$20,000 - $34,999"
    inc3 = "$35,000 - $49,999"
    inc4 = "$50,000 - $75,999"
    inc5 = "$75,000 - $99,999"
    inc6 = "$100,000 - $149,999"
    inc7 = "$150,000 - $199,999"
    inc8 = "$200,000 or more"
    income_choices = [ (inc1, inc1), 
                        (inc2, inc2),
                        (inc3, inc3),
                        (inc4, inc4),
                        (inc5, inc5),
                        (inc6, inc6),
                        (inc7, inc7),
                        (inc8, inc8)]
    
    # Fields
    medication1         = models.CharField(max_length=50,   blank=True, verbose_name="Medication 1")
    purpose1            = models.CharField(max_length=150,  blank=True, verbose_name="Purpose of 1st Med.")
    medication2         = models.CharField(max_length=50,   blank=True, verbose_name="Medication 2")
    purpose2            = models.CharField(max_length=150,  blank=True, verbose_name="Purpose of 2nd Med.")
    sexual_orientation  = models.CharField(max_length=10,   blank=True, verbose_name="Sexual Orientation" ,choices=sex_choices, null=True)
    income              = models.CharField(max_length=50,   blank=True, verbose_name="Income", choices=income_choices, null=True)
    level_of_education  = models.CharField(max_length=50,   blank=True, verbose_name="Level of Education", choices=edu_choices, null=True)
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

    # Generate data for education distribution
    @classmethod
    def education_data(cls):
        ed_level = [0,0,0,0,0,0]
        for sitch in CurrentSituation.objects.all():
            if sitch.level_of_education == CurrentSituation.edu1: ed_level[0] += 1
            elif sitch.level_of_education == CurrentSituation.edu2: ed_level[1] += 1
            elif sitch.level_of_education == CurrentSituation.edu3: ed_level[2] += 1
            elif sitch.level_of_education == CurrentSituation.edu4: ed_level[3] += 1
            elif sitch.level_of_education == CurrentSituation.edu5: ed_level[4] += 1
            elif sitch.level_of_education == CurrentSituation.edu6: ed_level[5] += 1

        return [
            ["Education Level", "count"],
            [CurrentSituation.edu1, ed_level[0]],
            [CurrentSituation.edu2, ed_level[1]],
            [CurrentSituation.edu3, ed_level[2]],
            [CurrentSituation.edu4, ed_level[3]],
            [CurrentSituation.edu5, ed_level[4]],
            [CurrentSituation.edu6, ed_level[5]],
        ]



    # Generate data for income distribution
    @classmethod
    def income_data(cls):
        # Counter for different income brackets
        incomes = [0,0,0,0,0,0,0,0]
        for sitch in CurrentSituation.objects.all():
            if sitch.income == CurrentSituation.inc1: incomes[0] += 1
            elif sitch.income == CurrentSituation.inc2: incomes[1] += 1
            elif sitch.income == CurrentSituation.inc3: incomes[2] += 1
            elif sitch.income == CurrentSituation.inc4: incomes[3] += 1
            elif sitch.income == CurrentSituation.inc5: incomes[4] += 1
            elif sitch.income == CurrentSituation.inc6: incomes[5] += 1
            elif sitch.income == CurrentSituation.inc7: incomes[6] += 1
            elif sitch.income == CurrentSituation.inc8: incomes[7] += 1

        return [
            ["Income", "count"],
            [CurrentSituation.inc1, incomes[0]],
            [CurrentSituation.inc2, incomes[1]],
            [CurrentSituation.inc3, incomes[2]],
            [CurrentSituation.inc4, incomes[3]],
            [CurrentSituation.inc5, incomes[4]],
            [CurrentSituation.inc6, incomes[5]],
            [CurrentSituation.inc7, incomes[6]],
            [CurrentSituation.inc8, incomes[7]],
        ]




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
