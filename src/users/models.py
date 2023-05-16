from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

#CustomUser model (AbstractUser + JWT)->
class CustomUser(AbstractUser):
    godel_jwt = models.CharField(max_length=300, default ='None') #default jwt for a user is 'None'

    def __str__(self):
        return self.username #username = eth address of user
    