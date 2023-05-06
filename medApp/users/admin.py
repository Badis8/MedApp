from django.contrib import admin
from .models import PendingDoctors
from .models import PendingPharmacists
admin.site.register(PendingDoctors)
admin.site.register(PendingPharmacists)
# Register your models here.
