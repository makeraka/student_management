from django.shortcuts import render

# Create your views here.

def showDemoPage(request):
    return render(request, 'demo.html')

#la page de connexion
def showLoginPage(request):
    return render(request,'login.html' )