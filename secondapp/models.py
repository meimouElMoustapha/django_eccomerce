from django.db import models
from django.contrib.auth.models import User
import datetime

class Student(models.Model):
    c =(
        ("M","Male"),("F","Female")
    )
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=200)
    roll_no = models.IntegerField(unique=True)
    # date_of_birth = models.DateField(blank=True,default=None)
    fee = models.FloatField()
    gender = models.CharField(max_length=150,choices=c)
    address = models.TextField(blank=True)
    is_registered = models.BooleanField()

    def __str__(self):
        return self.name+" "+str(self.roll_no)
    
    class Meta:
        verbose_name_plural="Student"

class Contact_Us(models.Model):
    name = models.CharField(max_length=250)
    contact_number = models.IntegerField(blank=True,unique=True)
    subject = models.CharField(max_length=250)
    message = models.TextField()
    added_on =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Contact Us"

class Category(models.Model):
    cat_name = models.CharField(max_length=250)
    cover_pic = models.FileField(upload_to="media/%Y/%m/%d")
    description = models.TextField()
    added_on =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cat_name

class register_table(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    contact_number = models.IntegerField()
    profile_pic =models.ImageField(upload_to = "profiles/%Y/%m/%d",null=True,blank=True)
    age = models.CharField(max_length=250,null=True,blank=True)
    city = models.CharField(max_length=250,null=True,blank=True)
    about = models.TextField(blank=True,null=True)
    gender = models.CharField(max_length=250,default="Male")
    occupation = models.CharField(max_length=250,null=True,blank=True)
    added_on =models.DateTimeField(auto_now_add=True,null=True)
    update_on = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.user.username

