
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

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
            if user.user_type=="1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type=="2":
                return HttpResponse("staff login"+str(user.user_type))
            else:
                return HttpResponse("student login"+str(user.user_type))
        else:
            messages.error(request,"Adresse email ou mot de passe incorrect")
            return HttpResponseRedirect("/")

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
    

