
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout

from student_management_app.EmailBackEnd import EmailBackEnd

# Create your views here.

def showDemoPage(request):
    return render(request, 'demo.html')

#la page de connexion
def showLoginPage(request):
    return render(request,'login.html' )

#action de login 
def loginAction(request):
    if request.method!="POST":
        return HttpResponse("<h2> Method not  allowed  </h2>")
    else:
        user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if(user)!=None:
            login(request,user)
            return HttpResponse("Email :" + request.POST.get("email")+"Password :" + request.POST.get("password"))
        else:
            return HttpResponse("Erreur d'athentification!!")

#action pour les details des info de l'utilisateur
def GetUserDetail(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.email+ " usertype : "+request.user.user_type)
    else:
        return HttpResponse("please Login first")

#methode de deconnection
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")
    

