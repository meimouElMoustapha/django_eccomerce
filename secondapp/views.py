from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from secondapp.models import Contact_Us, Category, register_table
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

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
    if request.method=="POST":
        fname = request.POST["first"]
        last = request.POST["last"]
        un = request.POST["uname"]
        pwd = request.POST["password"]
        em = request.POST["email"]
        con = request.POST["contact"]
        tp = request.POST["utype"]
        
        usr = User.objects.create_user(un,em,pwd)
        usr.first_name = fname
        usr.last_name = last
        if tp=="sell":
            usr.is_staff = True
        usr.save()

        reg = register_table(user=usr, contact_number=con)
        reg.save()
        return render(request,"register.html",{"status":"Mr/Miss. {} your Account created Successfully".format(fname)})
    return render(request,"register.html")

def check_user(request):
    if request.method=="GET":
        un = request.GET["usern"]
        check = User.objects.filter(username=un)
        if len(check) == 1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")

def user_login(request):
    if request.method=="POST":
        un = request.POST["username"]
        pwd = request.POST["password"]

        user = authenticate(username=un,password=pwd)
        if user:
            login(request,user)
            if user.is_superuser:
                return HttpResponseRedirect("/admin")
            if user.is_staff:
                return HttpResponseRedirect("/seller_dashboard")
            if user.is_active:
                return HttpResponseRedirect("/cust_dashboard")
                
        else:
            return render(request,"home.html",{"status":"Invalid Username or Password"})

    return HttpResponse("Called")

@login_required
def cust_dashboard(request):
    return render(request,"cust_dashboard.html")

@login_required
def seller_dashboard(request):
    return render(request,"seller_dashboard.html")
    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")




