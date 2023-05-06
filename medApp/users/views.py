from django.shortcuts import render,redirect
from django.contrib.auth import authenticate ,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm

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
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Registration Successful!"))
			return redirect('home')
	else:
		form = RegisterUserForm()

	return render(request, 'authentification/register_user.html', {
		'form':form,
		})