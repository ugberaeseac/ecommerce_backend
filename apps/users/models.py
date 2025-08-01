from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import Timestamp
import uuid



class User(AbstractUser, Timestamp):
    """
    
    """
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    #username = models.CharField(max_length=100, unique=True, blank=False, null=False)
    #password = models.CharField(max_length=128, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email} - {self.created_at}'


