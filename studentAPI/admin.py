from django.contrib import admin
from .models import Student


# Register your models here.


class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'rollNo', 'marks', 'subjects']


admin.site.register(Student, StudentAdmin)
