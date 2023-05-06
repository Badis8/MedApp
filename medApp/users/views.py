from django.shortcuts import render,redirect
from django.contrib.auth import authenticate ,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from django.contrib.auth.models import User
from .models import PendingDoctors

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
                print(user.email)
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
                redirect('DoctorRegistration')


    return render(request, 'authentification/register_user.html', {
      
    })
def registreDoctor(request,username,firstname,lastname,password,email):
    return render(request,'authentification/register_doctor.html',{})
 