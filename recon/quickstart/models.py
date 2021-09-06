from django.db import models
from django.db.models.base import Model

# Create your models here.
class subdomain(models,Model):
    id = models.BigAutoField(primary_key=True)
    # Useful info
    ip = models.TextField()
    target = models.TextField()
    subdomain = models.TextField()
    asn = models.TextField() 
    isp = models.TextField()
    organization = models.TextField()
    country = models.TextField()
    region = models.TextField()
    city = models.TextField()
    latitude = models.TextField()
    longuitude = models.TextField()
    timezone = models.TextField()
    user = models.TextField()
    date_found = models.TextField()
    last_seen = models.TextField()
