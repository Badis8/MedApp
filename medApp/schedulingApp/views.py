from django.shortcuts import render
import calendar
from django.contrib.auth import authenticate ,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from calendar import HTMLCalendar 
def home(request,year,month):
    month=month.capitalize()
    monthNumber=list(calendar.month_name).index(month)
    monthNumber=int(monthNumber)
    cal=HTMLCalendar().formatmonth(year,monthNumber)
    return render(request,"schedulingApp/home.html",{'year':year,'month':month,'cal':cal})
def presentation(request):
    isChecker=request.user.groups.filter(name="Checkers").exists()
    isNormalUserr=request.user.groups.filter(name="Doctor").exists()
    isDoctor=request.user.groups.filter(name="pharmacist").exists()
    isPharmacist=request.user.groups.filter(name="normal").exists()
    print(isChecker)
    print(isNormalUserr)
    print(isDoctor)
    print(isPharmacist)
    return render(request,"schedulingApp/generalPresentation.html",{"isChecker":isChecker})