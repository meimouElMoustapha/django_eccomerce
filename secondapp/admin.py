from django.contrib import admin
from secondapp.models import Student

admin.site.site_header="My Website"
# Register your models here.

admin.site.register(Student)
