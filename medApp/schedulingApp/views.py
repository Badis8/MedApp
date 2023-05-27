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
from .models import UserPendingOrdoannance,PharmacistPendingOrdoannance,Medicament
from django.shortcuts import redirect
from django.http import JsonResponse
import pandas as pd

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
    return render(request,"schedulingApp/generalPresentation.html",{"isChecker":isChecker,"isDoctor":isDoctor,"isNormalUser":isNormalUserr,"isPharmacist":isPharmacist})
def is_in_group_Doctors(user):
    return user.groups.filter(name='Doctors').exists()
@login_required(login_url='login')
@user_passes_test(is_in_group_Doctors)
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
            newOrodonnance.etat="unsent"
            newOrodonnance.decision="neutre"
            newOrodonnance.save()
            for medicine in medicines_list:
                medicines = Medicament.objects.filter(name=medicine['name'])
                if medicines.exists():
                    medicines = Medicament.objects.filter(name=medicine['name']).first()
                else:
                    messages.success(request,'ordannance sent unsuccessfuly: medecine named: '+medicine['name']+"does not exist")
                    isDoctor=request.user.groups.filter(name="Doctors").exists()
                    return render(request,"schedulingApp/prepareOrdonnance.html",{"isDoctor":isDoctor})
                
                ligneToAdd=LigneOrdonnance(quantity=medicine['quantity'],Medicament=medicines,Ordonnance=newOrodonnance)
                ligneToAdd.save()
                 
            messages.success(request,'ordannance sent successful')
             

    isDoctor=request.user.groups.filter(name="Doctors").exists()
    meds=Medicament.objects.all
    return render(request,"schedulingApp/prepareOrdonnance.html",{"isDoctor":isDoctor,"meds":meds} )
def is_in_group_NormalUser(user):
    return user.groups.filter(name='normalUsers').exists()
@login_required(login_url='login')
@user_passes_test(is_in_group_NormalUser)
def visualiseOrdonnance(request):
    if request.method == 'POST':
      
        PharmacistRequested=request.POST.get("Pharmacist")
        OrdonnanceId=request.POST.get("medicId")
        Users = get_user_model()
        user = Users.objects.filter(username=PharmacistRequested).first()
        if(user==None):
            messages.success(request,'no pharmacist '+PharmacistRequested+' is present in our database')
            isNormalUser=request.user.groups.filter(name="normalUsers").exists()
            user = User.objects.get(username=request.user.username)
            ordonnances = Ordonnance.objects.filter(usernameDestination=user)
            return render(request,"schedulingApp/visualiseOrdonnance.html",{"isNormalUser":isNormalUser,"Ordonnances":ordonnances})
        PendingOrdonnanceRequested=PharmacistPendingOrdoannance()
        PendingOrdonnanceRequested.Pharmaciste=user
        try:
            ordonnance = Ordonnance.objects.get(id=OrdonnanceId)
        except Ordonnance.DoesNotExist:
            messages.success(request,'aucune ordonnoce trouve')
            isNormalUser=request.user.groups.filter(name="normalUsers").exists()
            user = User.objects.get(username=request.user.username)
            ordonnances = Ordonnance.objects.filter(usernameDestination=user)
            return render(request,"schedulingApp/visualiseOrdonnance.html",{"isNormalUser":isNormalUser,"Ordonnances":ordonnances})
        PendingOrdonnanceRequested.Ordonnance=ordonnance
        ordonnance.etat="sent"
        ordonnance.decision="neutre"
        ordonnance.save()
        PendingOrdonnanceRequested.save()
        messages.success(request,'ordannance sent successful to pharmacist') 
    isNormalUser=request.user.groups.filter(name="normalUsers").exists()
    user = User.objects.get(username=request.user.username)
    ordonnances = Ordonnance.objects.filter(usernameDestination=user)
    return render(request,"schedulingApp/visualiseOrdonnance.html",{"isNormalUser":isNormalUser,"Ordonnances":ordonnances})
def visualiseWaitingOrdonnance(request):
    isNormalUser=request.user.groups.filter(name="normalUsers").exists()
    user = User.objects.get(username=request.user.username)
    ordonnances = Ordonnance.objects.filter(usernameDestination=user)
    return render(request,"schedulingApp/visualiseOrdonnanceWaiting.html",{"isNormalUser":isNormalUser,"Ordonnances":ordonnances})

def visualisePendingPharmacistOrdonnance(request):
    if request.method=='POST':
        if request.POST['action'] == 'accept':
            acceptedOrdonnace=request.POST.get('ordonnanceAccepted')
            acceptedOrdonnace=Ordonnance.objects.get(id=acceptedOrdonnace)
            acceptedOrdonnace.decision="Accepted"
            acceptedOrdonnace.save()
            user = User.objects.get(username=request.user.username)
            UnboundOrdonnance=PharmacistPendingOrdoannance.objects.get(Pharmaciste=user,Ordonnance=acceptedOrdonnace)
            UnboundOrdonnance.delete()
            messages.success(request,'ordonnance accepted') 

        if request.POST['action'] == 'Deny':
            deniedOrodonnance=request.POST.get('ordonnanceDenied')
            deniedOrodonnance=Ordonnance.objects.get(id=deniedOrodonnance)
            deniedOrodonnance.decision="neutre"
            deniedOrodonnance.etat="unsent"
            deniedOrodonnance.save()
            user = User.objects.get(username=request.user.username)
            UnboundOrdonnance=PharmacistPendingOrdoannance.objects.get(Pharmaciste=user,Ordonnance=deniedOrodonnance)
            UnboundOrdonnance.delete()


    isPharmacist=request.user.groups.filter(name="Pharmacists").exists()
    user = User.objects.get(username=request.user.username)
    ordonnancesPending = PharmacistPendingOrdoannance.objects.filter(Pharmaciste=user)
   
    return render(request,"schedulingApp/PharmacistesViewing.html",{"isPharmacist":isPharmacist,"Ordonnances":ordonnancesPending})
def visualiseAcceptedOronnance(request):
    isNormalUser=request.user.groups.filter(name="normalUsers").exists()
    user = User.objects.get(username=request.user.username)
    ordonnances = Ordonnance.objects.filter(usernameDestination=user,decision="Accepted")
    return render(request,"schedulingApp/accepted.html",{"isNormalUser":isNormalUser,"Ordonnances":ordonnances})
    