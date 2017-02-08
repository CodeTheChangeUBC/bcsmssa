from django.db import models

# Create your models here.

class Client ( models.Model ):
    client_number = models.IntegerField()
    date_of_birth = models.CommaSeparatedIntegerField( max_length = 3 )
    age = models.IntegerField()
    number_of_abuses = models.IntegerField()
    services_required = models.CommaSeparatedIntegerField( max_length= 4 )

class Abuse ( models.Model ):
    start_date = models.CommaSeparatedIntegerField( max_length = 3 )
    stop_date = models.CommaSeparatedIntegerField( max_length = 3 )
    role_of_abuser = models.IntegerField()
    reported_date = models.CommaSeparatedIntegerField( max_length = 3 )
    family_context = models.CommaSeparatedIntegerField( max_length = 12 )
    client = models.ForeignKey( Client, on_delete = models.CASCADE )

class Client_Current_Situation ( models.Model ):
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


