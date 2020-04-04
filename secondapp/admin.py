from django.contrib import admin
from secondapp.models import Student,Contact_Us

admin.site.site_header="My Website | Second Project"

class StudentAdmin(admin.ModelAdmin):
    # fields = ["roll_no","email","name"]
    list_display = ["name","roll_no","email","fee","gender","address","is_registered"]
    search_fields = ["roll_no","name"]
    list_filter =["name","gender"]
    list_editable = ["email",]

class Contact_UsAdmin(admin.ModelAdmin):
    fields = ["contact_number","name","subject","message"]

    list_display = ["id","name","contact_number","subject","message","added_on"]
    search_fields = ["name"]
    list_filter = ["added_on","name"]
    list_editable = ["name"]

admin.site.register(Student,StudentAdmin)
admin.site.register(Contact_Us,Contact_UsAdmin)
