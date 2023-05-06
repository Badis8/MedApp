from django.db import models
class PendingDoctors(models.Model):
    username=models.CharField("username",max_length=50)
    First_name=models.CharField("First_name",max_length=50)
    Last_name=models.CharField("Last_name",max_length=50)
    Email=models.EmailField("email")
    Specialty=models.CharField("Last_name",max_length=50)
    address=models.CharField("address",max_length=50)
    phoneNumber=models.CharField("phone number",max_length=8)
    def __str__(self):
        return self.username

class PendingPharmacists(models.Model):
    username=models.CharField("username",max_length=50)
    First_name=models.CharField("First_name",max_length=50)
    Last_name=models.CharField("Last_name",max_length=50)
    Email=models.EmailField("email")
    address=models.CharField("address",max_length=50)
    phoneNumber=models.CharField("phone number",max_length=8)
    def __str__(self):
        return self.username

# Create your models here.
