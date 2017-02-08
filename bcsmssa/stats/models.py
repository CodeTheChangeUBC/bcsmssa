from django.core.validators import validate_comma_separated_integer_list
from django.db import models

# Create your models here.

class Client ( models.Model ):
    client_number = models.IntegerField()
    date_of_birth = models.CharField( max_length = 3, validators=[validate_comma_separated_integer_list])
    age = models.IntegerField()
    number_of_abuses = models.IntegerField()
    services_required = models.CharField( max_length = 4, validators=[validate_comma_separated_integer_list])

class Abuse ( models.Model ):
    start_date = models.CharField( max_length = 3, validators=[validate_comma_separated_integer_list])
    stop_date = models.CharField( max_length = 3, validators=[validate_comma_separated_integer_list] )
    role_of_abuser = models.IntegerField()
    reported_date = models.CharField( max_length = 3, validators=[validate_comma_separated_integer_list] )
    family_context = models.CharField( max_length = 12, validators=[validate_comma_separated_integer_list] )
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
