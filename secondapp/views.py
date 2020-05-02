from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from secondapp.models import Contact_Us, Category, register_table, add_product
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from secondapp.forms import add_product_form

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
            else:
                return HttpResponseRedirect("/cust_dashboard")
            # if user.is_active:
            #     return HttpResponseRedirect("/cust_dashboard")
                
        else:
            return render(request,"home.html",{"status":"Invalid Username or Password"})

    return HttpResponse("Called")

@login_required
def cust_dashboard(request):
    context = {}
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    return render(request,"cust_dashboard.html",context)

@login_required
def seller_dashboard(request):
    return render(request,"seller_dashboard.html")
    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

def edit_profile(request):
    context = {}
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"]=data    
    if request.method=="POST":
        fn = request.POST["fname"]
        ln = request.POST["lname"]
        em = request.POST["email"]
        con = request.POST["contact"]
        age = request.POST["age"]
        ct = request.POST["city"]
        gen = request.POST["gender"]
        occ = request.POST["occ"]
        abt = request.POST["about"]

        usr = User.objects.get(id=request.user.id)
        usr.first_name = fn
        usr.last_name = ln
        usr.email = em
        usr.save()

        data.contact_number = con
        data.age = age
        data.city = ct
        data.gender = gen
        data.occupation = occ
        data.about = abt
        data.save()

        if "image" in request.FILES:
            img = request.FILES["image"]
            data.profile_pic = img
            data.save()


        context["status"] = "Changes Saved Successfully"
    return render(request,"edit_profile.html",context)

def change_password(request):
    context={}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    if request.method=="POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]
        
        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check==True:
            user.set_password(new_pas)
            user.save()
            context["msz"] = "Password Changed Successfully!!!"
            context["col"] = "alert-success"
            user = User.objects.get(username=un)
            login(request,user)
        else:
            context["msz"] = "Incorrect Current Password"
            context["col"] = "alert-danger"

    return render(request,"change_password.html",context)


def add_product_view(request):
    context={}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    form = add_product_form()
    if request.method=="POST":
        form = add_product_form(request.POST,request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            login_user =User.objects.get(username=request.user.username)
            data.seller = login_user
            data.save()
            context["status"] ="{} Added Successfully".format(data.product_name)

    context["form"] = form

    return render(request,"addproduct.html",context)

def my_products(request):
    context = {}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
        
    all = add_product.objects.filter(seller__id=request.user.id).order_by("-id")
    context["products"] = all
    return render(request,"myproducts.html",context)

def single_product(request):
    context = {}
    id = request.GET["pid"]
    obj = add_product.objects.get(id=id)
    context["product"] = obj
    return render(request,"single_product.html",context)

def update_product(request):
    context ={}
    cats = Category.objects.all().order_by("cat_name")
    context["category"] = cats

    pid = request.GET["pid"]
    product = get_object_or_404(add_product,id=pid)
    context["product"] = product

    if request.method=="POST":
        pn = request.POST["pname"]
        ct_id = request.POST["pcat"]
        pr = request.POST["pp"]
        sp = request.POST["sp"]
        des = request.POST["des"]
        
        cat_obj = Category.objects.get(id=ct_id)

        product.product_name =pn
        product.product_category =cat_obj
        product.product_price =pr
        product.sale_price =sp
        product.details =des
        if "pimg" in request.FILES:
            img = request.FILES["pimg"]
            product.product_image = img
        product.save()
        context["status"] = "Changes Saved Successfully"
        context["id"] = pid
    return render(request,"update_product.html",context)

def delete_product(request):
    context = {}
    if "pid" in request.GET:
        pid = request.GET["pid"]
        prd = get_object_or_404(add_product, id=pid)
        context["product"] = prd

        if "action" in request.GET:
            prd.delete()
            context["status"] = str(prd.product_name)+" removed Successfully!!!"
    return render(request,"deleteproduct.html",context)

def all_products(request):
    context = {}
    all_products = add_product.objects.all().order_by("product_name")
    context["products"] = all_products
    return render(request,"allproducts.html",context)