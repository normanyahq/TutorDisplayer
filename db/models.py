#coding=utf-8
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from django.db.models.signals import post_save


#constant
GENDER_CHOICES = (
    ('0','Unknown'),
    ('1','Male'),
    ('2','Female'),
    ('9','not applicatable'))   
    
'''      see if is qualified
TIME_CHOICES = (
     ('0', 'Monday_morning'),
     ('1', 'Monday_afternoon'),
     ('2', 'Monday_evening'),
     ('3', 'Tuesday_morning'),
     ........
     ('20', 'Sunday_evening'),     
                )
'''

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=50)

class TimePeriod(models.Model):
    description = models.CharField(max_length = 20)
    

class District(models.Model):
    name = models.CharField(max_length=40,blank = True, null = True)
    

class School(models.Model):
    name = models.CharField(max_length=40,blank = True, null = True)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=30, blank=True, null = True)
    school = models.CharField(max_length=40,blank = True, null = True)
    subject = models.ForeignKey(Subject, blank = True, null = True)
    cellphone = models.CharField(max_length=40,blank = True, null = True)
    honour = models.CharField(max_length=200,blank = True, null = True)
    speciality = models.CharField(max_length=200,blank = True, null = True)
    additional_info =  models.CharField(max_length=500,blank = True, null = True)
    course = models.CharField(max_length=200,blank = True)
    district = models.CharField(max_length=200,blank = True)
    time_period = models.ManyToManyField(TimePeriod, null = True, related_name = 'user')
    area = models.ManyToManyField(District, blank = True, related_name = 'user')
    taobao_link = models.URLField(blank = True,null = True)
    confirmed = models.BooleanField(default = False)
    def __unicode__(self):
            return self.name
  
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create user profile for new users at save user time, if it doesn't already exist
    """
    if created:
        p = UserProfile(user=instance)
        p.save()

post_save.connect(create_user_profile, sender=User)
 
