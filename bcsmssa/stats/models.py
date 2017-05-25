from django.core.validators import validate_comma_separated_integer_list
from django.contrib.auth.models import User
from django.db import models
import uuid

class UserProfile( models.Model ):
    user = models.OneToOneField(User)

class Client( models.Model ):
    # set up client field
    client_number = models.IntegerField()
    date_of_birth = models.DateField('Date of Birth (yyyy-mm-dd)')
    age = models.IntegerField(null=True, blank=True, default=None)
    number_of_abuses = models.IntegerField(null=True, blank=True, default=None)
    #health_professionals = models.BooleanField(default=False, blank=False)
    #services_required = models.CharField( max_length = 4, validators=[validate_comma_separated_integer_list])
    # output client info. when called  
    def __str__(self):
        return str(self.client_number)

    @classmethod
    def create(cls, num, dob, age, num_abuses):
        client = Client(client_number=num, 
                        date_of_birth=dob, 
                        age=age, 
                        number_of_abuses=num_abuses)
        client.save()

class ServicesRequested(models.Model):
    victim_services = models.IntegerField()         #models.BooleanField(default=False)
    individual_therapy = models.IntegerField()      #models.BooleanField(default=False)
    group_therapy = models.IntegerField()           #models.BooleanField(default=False)

    client1 = models.OneToOneField(
         Client,
         on_delete=models.CASCADE,
         primary_key=True,
    )

    def __str__(self):
        return str(self.client1.client_number)

    @classmethod
    def create(cls, vs, it, gt, client):
        sr = ServicesRequested(victim_services=vs,
                                individual_therapy=it, 
                                group_therapy=gt, 
                                client1 = client)

        sr.save()

class Referral(models.Model):
    web = models.BooleanField(default=False, blank=True)
    social_service = models.BooleanField(default=False, blank=True)
    health_practitioner = models.BooleanField(default=False, blank=True)
    alcoholics_anonymous = models.BooleanField(default=False, blank=True)
    drug_treatment_group = models.BooleanField(default=False, blank=True)
    advertisement = models.BooleanField(default=False, blank=True)
    other = models.CharField(max_length=30, blank=True)

    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return str(self.client1.client_number)

    @classmethod
    def create(cls, web, ss, hp, aa, dtg, ad, other, client):
        referral = Referral(web=web, 
                            social_service=ss,
                            health_practitioner=hp,
                            alcoholics_anonymous=aa,
                            drug_treatment_group=dtg,
                            advertisement=ad,
                            other=other,
                            client=client)
        referral.save()


class Abuse ( models.Model ):
    client = models.ForeignKey( Client, on_delete = models.CASCADE )
    start_date = models.CharField( max_length = 3, validators=[validate_comma_separated_integer_list])
    stop_date = models.CharField( max_length = 3, validators=[validate_comma_separated_integer_list] )
    role_of_abuser = models.IntegerField()
    reported_date = models.CharField( max_length = 3, validators=[validate_comma_separated_integer_list] )
    family_context = models.CharField( max_length = 12, validators=[validate_comma_separated_integer_list] )

    def __str__(self):
        return str(self.client)

    @classmethod
    def create(cls, client, start, stop, role, rep_date, context):
        abuse = Abuse(client=client, 
                        start_date=start,
                        stop_date=stop,
                        role_of_abuser=role,
                        reported_date=rep_date,
                        family_context=context)
        abuse.save()

class Client_Current_Situation( models.Model ):
    medication1 = models.CharField(max_length=50)
    purpose1 = models.CharField(max_length=150)
    medication2 = models.CharField(max_length=50)
    purpose2 = models.CharField(max_length=150)
    sexual_orientation = models.IntegerField()
    income = models.IntegerField()
    level_of_education = models.IntegerField()
    profession = models.CharField(max_length=50)
    in_treatment = models.BooleanField()
    abuse = models.ForeignKey( Abuse, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.abuse)

class InviteKey( models.Model ):
    id = models.CharField(max_length=6, primary_key=True)

    def as_json(self):
        return dict(code=self.id)
