from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=15)
    birth_date = models.DateField(null=True)

    class Meta:
        db_table = 'custom_users'