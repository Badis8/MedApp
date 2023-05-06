from django.shortcuts import render,redirect
from django.contrib.auth import authenticate ,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from django.contrib.auth.models import User,Group
from .models import PendingDoctors
from .models import PendingPharmacists
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
def is_in_group_Checker(user):
    return user.groups.filter(name='Checkers').exists()
def login_user(request):
    if request.method=="POST":
        userName=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=userName,password=password)
        if user is not None:
            login(request,user)
            return redirect('generalPresentation')
        else:
            messages.success(request,"error logging in , try again !")
            return redirect('login')
    else:
        return render(request,'authentification/authentification.html',{}) 

# Create your views here.
def logout_user(request):
    logout(request)
    messages.success(request,("successfully logged out!"))
    return redirect('home')
def registerRequestForm(request):
    if request.method == "POST":
             
            username=request.POST.get('username')  
            first=request.POST.get('firstName')  
            last=request.POST.get('LastName')  
            email=request.POST.get('EmailAddress')  
            password=request.POST.get('password')  
            typeSelected=request.POST.get('flexRadioDefault')
            users = User.objects.all()
            for user in users:
                if((user.email==email) or (user.username==username)):
                       messages.success(request,'email or username already used on our data base,please use another one')
                       return render(request, 'authentification/register_user.html', { 
      
                })
            if(typeSelected=="Normal"):
                new_user = User.objects.create_user(username=username, password=password,email=email)
                new_user.first_name = first
                new_user.last_name = last
                new_user.save()
            if(typeSelected=="Doctor"):
                phoneNumber=request.POST.get('PhoneNumber')    
                address =request.POST.get('DoctorAddress')  
                specialite =request.POST.get('Speciality') 
                PendingDoctor=PendingDoctors()
                PendingDoctor.username=username
                PendingDoctor.First_name=first
                PendingDoctor.Last_name=last
                PendingDoctor.Email=email
                PendingDoctor.phoneNumber=phoneNumber
                PendingDoctor.Specialty=specialite
                PendingDoctor.address=address
                PendingDoctor.password=password
                PendingDoctor.save()
                messages.success(request,"pending doctor success")
            if(typeSelected=="pharmacist"):
                 
                phoneNumber =request.POST.get('PharmacistAddress')  
                address=  request.POST.get('PhoneNumberPharmacist')  
                PendingPharmacist=PendingPharmacists()
                PendingPharmacist.username=username
                PendingPharmacist.First_name=first
                PendingPharmacist.Last_name=last
                PendingPharmacist.Email=email
                PendingPharmacist.phoneNumber=phoneNumber
                PendingPharmacist.address=address
                PendingPharmacist.password=password
                PendingPharmacist.save()
                messages.success(request,"pending pharmacist success")
                 


    return render(request, 'authentification/register_user.html', {
      
    })  
@login_required(login_url='login')
@user_passes_test(is_in_group_Checker)
def PendingDoctor(request):
    if request.method == "POST":
        if request.POST['action'] == 'accept':
            waitingDoctors=PendingDoctors.objects.all()
            
            doctor_id=request.POST.get('doctor_id_Accepted')
            for doctor in waitingDoctors:
                if(doctor.username==doctor_id):
                    user = User.objects.create_user(username=doctor.username, password=doctor.password,email=doctor.Email)
                    user.first_name = doctor.First_name
                    user.last_name = doctor.Last_name
                    user.save()
                    group = Group.objects.get(name='Doctors')
                    group.user_set.add(user)
                    doctor= PendingDoctors.objects.get(username=doctor.username)
                    doctor.delete()
                    messages.success(request,"Doctor accepted")
                    waitingDoctors=PendingDoctors.objects.all()
                    isChecker=request.user.groups.filter(name="Checkers").exists()
                    return render(request,'authentification/pendingDoctor.html',{'doctors':waitingDoctors,'isChecker':isChecker})
    
           
        elif request.POST['action'] == 'Deny':
            doctor_id=request.POST.get('doctor_id_Denied')
            waitingDoctors=PendingDoctors.objects.all()
            for doctor in waitingDoctors:
                if(doctor.username==doctor_id):   
                    doctor= PendingDoctors.objects.get(username=doctor.username)
                    doctor.delete()
                    messages.success(request,"Doctor rejected")
                    waitingDoctors=PendingDoctors.objects.all()
                    isChecker=request.user.groups.filter(name="Checkers").exists()
                    return render(request,'authentification/pendingDoctor.html',{'doctors':waitingDoctors,'isChecker':isChecker})



 
            print(doctor_id)

    waitingDoctors=PendingDoctors.objects.all()
    isChecker=request.user.groups.filter(name="Checkers").exists()
    return render(request,'authentification/pendingDoctor.html',{'doctors':waitingDoctors,'isChecker':isChecker})
 