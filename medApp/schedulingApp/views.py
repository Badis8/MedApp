from django.shortcuts import render
import calendar
from django.contrib.auth import authenticate ,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from calendar import HTMLCalendar 
import json
from django.contrib.auth import get_user_model
from .models import Medicament,Ordonnance,LigneOrdonnance
from django.contrib.auth.models import User
from .models import Ordonnance
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

def home(request,year,month):
    month=month.capitalize()
    monthNumber=list(calendar.month_name).index(month)
    monthNumber=int(monthNumber)
    cal=HTMLCalendar().formatmonth(year,monthNumber)
    return render(request,"schedulingApp/home.html",{'year':year,'month':month,'cal':cal})
def presentation(request):
    isChecker=request.user.groups.filter(name="Checkers").exists()
    isNormalUserr=request.user.groups.filter(name="normalUsers").exists()
    isDoctor=request.user.groups.filter(name="Doctors").exists()
    isPharmacist=request.user.groups.filter(name="Pharmacists").exists()
    return render(request,"schedulingApp/generalPresentation.html",{"isChecker":isChecker,"isDoctor":isDoctor,"isNormalUser":isNormalUserr})
def prepareOrdonnance(request):
    
    if request.method == 'POST':
        medicines = request.POST.get('medicines')
        if medicines:
            newOrodonnance=Ordonnance()
            User = get_user_model()
            username=request.POST.get('patientname')
             
            user = User.objects.filter(username=username).first()
            if(user==None):
                 messages.success(request,'no username '+username+' is present in our database')
                 isDoctor=request.user.groups.filter(name="Doctors").exists()
                 return render(request,"schedulingApp/prepareOrdonnance.html",{"isDoctor":isDoctor})
             
            medicines_list = json.loads(medicines)
            newOrodonnance.usernameDestination=user
            newOrodonnance.Doctor=request.user
            newOrodonnance.save()
            for medicine in medicines_list:
                medicines = Medicament.objects.filter(name=medicine['name'], weight=medicine['weight'])
                if medicines.exists():
                    medicines = Medicament.objects.filter(name=medicine['name'], weight=medicine['weight']).first()
                else:
                    medicines=Medicament(name=medicine['name'], weight=medicine['weight'])
                    medicines.save()
                    print("here")
                    print("here this is the type "+medicines.name)
                ligneToAdd=LigneOrdonnance(quantity=medicine['quantity'],Medicament=medicines,Ordonnance=newOrodonnance)
                ligneToAdd.save()
                messages.success(request,'ligne ordannance sent successful')
            messages.success(request,'ordannance sent successful')
             

    isDoctor=request.user.groups.filter(name="Doctors").exists()
     
    return render(request,"schedulingApp/prepareOrdonnance.html",{"isDoctor":isDoctor})
def is_in_group_NormalUser(user):
    return user.groups.filter(name='normalUsers').exists()
@login_required(login_url='login')
@user_passes_test(is_in_group_NormalUser)
def visualiseOrdonnance(request):
    isNormalUser=request.user.groups.filter(name="normalUsers").exists()
    user = User.objects.get(username=request.user.username)
    ordonnances = Ordonnance.objects.filter(usernameDestination=user)
    return render(request,"schedulingApp/visualiseOrdonnance.html",{"isNormalUser":isNormalUser,"Ordonnances":ordonnances})
