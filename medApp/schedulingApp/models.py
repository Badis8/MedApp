from django.db import models
from  django.contrib.auth.models import User
class Medicament(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return str(self.id)
    
class Ordonnance(models.Model):
    id = models.AutoField(primary_key=True)
    usernameDestination=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_Destination")
    Doctor=models.ForeignKey(User,on_delete=models.CASCADE,related_name="Doctor_Destination")
    def __str__(self):
        return str(self.id)


class LigneOrdonnance(models.Model):
    id = models.AutoField(primary_key=True)
    Medicament = models.ForeignKey(Medicament,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    Ordonnance=models.ForeignKey(Ordonnance,on_delete=models.CASCADE,related_name="ligne")
    def __str__(self):
        return str(self.id)


# Create your models here.
 