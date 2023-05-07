from django.contrib import admin
from .models import Medicament,Ordonnance,LigneOrdonnance
admin.site.register(Medicament)
admin.site.register(Ordonnance)
admin.site.register(LigneOrdonnance)
# Register your models here.
