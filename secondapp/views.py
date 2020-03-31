from django.shortcuts import render

def index(request):
    return render(request,"home.html")

def aboutpage(request):
    return render(request,"about.html")

def contactpage(request):
    return render(request,"contact.html")

