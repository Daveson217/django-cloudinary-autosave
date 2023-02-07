from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

class CustomUser(AbstractUser):
    picture = CloudinaryField('Picture', null=True, blank=True)