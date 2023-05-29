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
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import mimetypes
from django.http import FileResponse
from django.http.response import HttpResponse

def generate_patient_report(patient_info, medication_list,uniqueId):
    toDwonloadPath="doctorsPrescriptions/newPrescriptionPDF"+uniqueId+".pdf"
    pdf = canvas.Canvas(toDwonloadPath,pagesize=letter)
    pdf.setFont("Helvetica", 12)
    left_margin = 50
    line_spacing = 20
    y_position = 700

    pdf.drawString(left_margin, y_position, "Patient Name: " + patient_info["name"])
    y_position -= line_spacing
    pdf.drawString(left_margin, y_position, "Patient Last Name: " + patient_info["last_name"])
    y_position -= 2 * line_spacing
    pdf.drawString(left_margin, y_position, "Medication Details:")
    y_position -= line_spacing
    for medication in medication_list:
        pdf.drawString(left_margin + 20, y_position, "Name: " + medication["name"])
        pdf.drawString(left_margin + 20, y_position - line_spacing, "Quantity: " + str(medication["quantity"]))
        pdf.drawString(left_margin + 20, y_position - 2 * line_spacing, "Quantity per day: " + medication["quantityPerDay"])
        pdf.drawString(left_margin + 20, y_position - 3 * line_spacing, "Remarks: " + medication["remarks"])
        y_position -= 4 * line_spacing
        pdf.line(left_margin, y_position + 5, left_margin + 400, y_position + 5)
        y_position -= line_spacing
    pdf.drawString(left_margin + 20, y_position - 2 * line_spacing, "Date: " + medication["date"])
    pdf.save()



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
                
                ligneToAdd=LigneOrdonnance(quantity=medicine['quantity'],Medicament=medicines,Ordonnance=newOrodonnance,remarks=medicine['Remarks'],qauntityPerDay=medicine['quantityPerDay'])
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
def visualiseHistory(request):
    isDoctor=request.user.groups.filter(name="Doctors").exists()
    ordonnances=Ordonnance.objects.filter(Doctor=request.user)      
    return render(request,"schedulingApp/viewHistory.html",{"isDoctor":isDoctor,"Ordonnances":ordonnances})
def downlaoad(request,param):
    medication_list=[]
 
    isDoctor=request.user.groups.filter(name="Doctors").exists()
    ordonnances=Ordonnance.objects.filter(id=int(param)) 
    dateOfOrdonnace=ordonnances.first().date
    patient_info={"name":ordonnances.first().usernameDestination.first_name,"last_name":ordonnances.first().usernameDestination.last_name}
    for ligne in ordonnances.first().ligne.all():
        uniqueMedicationInstance={"name":ligne.Medicament.name,"quantity":int(ligne.quantity),"date":str(dateOfOrdonnace.year)+"-"+str(dateOfOrdonnace.month)+"-"+str(dateOfOrdonnace.day),"quantityPerDay":str(ligne.qauntityPerDay),"remarks":ligne.remarks}
        medication_list.append(uniqueMedicationInstance)
    generate_patient_report(patient_info,medication_list,str(ordonnances.first().id))
    toDwonloadPath="doctorsPrescriptions/newPrescriptionPDF"+str(ordonnances.first().id)+".pdf"
    fileName=str(ordonnances.first().id)+".pdf"
    path = open(toDwonloadPath, 'r')
    mime_type, _ = mimetypes.guess_type(toDwonloadPath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % fileName
    return response
   
