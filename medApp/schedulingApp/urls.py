 
from . import views
from django.urls import path
#int str path for / stuff slug for under and middle scores and UUID for unique identifiers, these are the ones permitted
urlpatterns = [
   
    path('',views.presentation,name="home"),
    path('presentation',views.presentation,name="generalPresentation"),
    path('PrepareOrdonnance',views.prepareOrdonnance,name="PrepareOrdonnance"),
    
]
