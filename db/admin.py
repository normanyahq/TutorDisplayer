from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from models import *



class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)

class TimePeriodAdmin(admin.ModelAdmin):
    list_display = ('description',)
    search_fields = ('description',)
    list_filter = ('description',)

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)

#UserAdmin.list_display = ('username', 'email', 'is_active', 'is_staff', 'date_joined',)
admin.site.register(Subject, SubjectAdmin)

#admin.site.register(Subject)
admin.site.register(TimePeriod, TimePeriodAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(School, SchoolAdmin)
