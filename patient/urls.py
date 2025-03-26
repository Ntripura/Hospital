from django.urls import path
from patient import views
from patient import models

urlpatterns = [ 
    
   path('signup/', views.Register.as_view()),
   path('login/', views.Login.as_view()),
   
   #path('userdetails/<str:pk>/', views.Login.as_view()),
   path('createdoctor/',views.DoctorDetails.as_view()),
   path('loginuser/',views.LoginUser.as_view()),
 #  path('userupdate/<str:pk>/',views.UpdateConsumer.as_view()), 
   
]