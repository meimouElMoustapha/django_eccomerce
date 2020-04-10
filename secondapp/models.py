from django.db import models

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




