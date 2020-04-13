from django.shortcuts import render
from django.http import HttpResponse
from secondapp.models import Contact_Us, Category

def index(request):
    recent = Contact_Us.objects.all().order_by("-id")[:5]
    cats = Category.objects.all().order_by("cat_name")

    return render(request,"home.html",{"messages":recent,"category":cats})

def aboutpage(request):
    cats = Category.objects.all().order_by("cat_name")
    return render(request,"about.html",{"category":cats})

def contactpage(request):
    cats = Category.objects.all().order_by("cat_name")
    all_data = Contact_Us.objects.all().order_by("-id")
    if request.method=="POST":
        nm = request.POST["name"]
        con = request.POST["contact"]
        sub = request.POST["subject"]
        msz = request.POST["message"]

        data = Contact_Us(name=nm,contact_number=con,subject=sub,message=msz)
        data.save()
        res = "Dear {} Thanks for your feedback".format(nm)
        return render(request,"contact.html",{"status":res,"messages":all_data,"category":cats})
        # return HttpResponse("<h1 style='color:green;'>Dear {} Data Saved Successfully!</h1>".format(nm))
        

    return render(request,"contact.html",{"messages":all_data,"category":cats})

def register(request):
    return render(request,"register.html")