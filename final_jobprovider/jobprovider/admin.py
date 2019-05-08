from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import Job, Other, Employer, Student, Skill


class EmployerAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'phone', 'company']
    list_filter = ['company']

class JobAdmin(admin.ModelAdmin):
    list_display = ['create_by', 'id', 'job_title', 'faculty', 'age', 'salary', 'gender', 'area', 'job_type']
    list_filter = ['create_by', 'faculty', 'gender', 'job_type']

class OtherAdmin(admin.ModelAdmin):
    list_display = ['job', 'id', 'requirement']
    search_fields = ['requirement']

class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'faculty', 'age', 'phone', 'gender', 'is_unemp']
    list_filter = ['faculty', 'gender', 'is_unemp']

class SkillAdmin(admin.ModelAdmin):
    list_display = ['student', 'id', 'skill']
    search_fields = ['skill']

admin.site.register(Employer, EmployerAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Other, OtherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Permission)