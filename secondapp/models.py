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

