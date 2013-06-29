from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.template import RequestContext
from django.db.models import *
from db.models import *
from db.forms import *
from forms import *
import json

def submit_tutor_request(request):
    if request.method == "GET":
        return HttpResponse("Invalid Post")
    tutor_request_form = SubmitRequest(request.POST)
    if tutor_request_form.is_valid():
        tutor_request_form.save()
        return HttpResponse("Succeeded")
    else:
        return HttpResponse("Invalid Post")

def fill_tutor_request(request):
    form = SubmitRequest()
    return render_to_response('fill_request.html', locals(), context_instance=RequestContext(request))
    

def tutorinfo(request):
    if 'user_id' in request.GET and request.GET['user_id']:
        print int(request.GET['user_id'])
        user = User.objects.get(id=int(request.GET['user_id']))
    else:
        return HttpResponse(u"no such tutor")
    return render_to_response('detailed_info.html', locals(), context_instance=RequestContext(request))

def tutordisplay(request):
    candidate = User.objects.all()
    timeslot = TimePeriod.objects.all()
#    print candidate
    if 'TimePeriod' in request.GET and request.GET['TimePeriod']:
        time_period = json.loads(request.GET['TimePeriod'])
        for time_period_id in time_period:
            candidate = candidate.filter(profile__time_period__id = time_period_id)
    if 'Subject' in request.GET and request.GET['Subject']:
        subject = json.loads(request.GET['Subject'])
        for subject_id in subject:
            candidate = candidate.filter(profile__subject__id = subject_id)
    if 'District' in request.GET and request.GET['District']:
        district = json.loads(request.GET['District'])
        for district_id in district:
            candidate = candidate.filter(profile__area__id = district_id)
    candidate.order_by('salary_per_hour')
#    print candidate
    return render_to_response('display.html', locals(), context_instance=RequestContext(request))

def home(request):
    user = request.user
    return render_to_response('home.html',locals(),context_instance=RequestContext(request))
    
def login(request):
    path = request.get_full_path()
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/login_success/")
        else:
            return render_to_response('login.html',{'errors':'True'},context_instance=RequestContext(request))
        request.session.modified = True
    return render_to_response('login.html', context_instance=RequestContext(request))
    
@login_required
def login_success(request):
    return render_to_response('login_success.html',locals(),context_instance=RequestContext(request))

    
@login_required
def passwordchange(request):
    user = request.user
    if request.method == 'POST':     
        if request.POST['origin'] != '' :
            if not user.check_password(request.POST['origin']):
                return render_to_response('password_change.html',{'passerror':'True'}, context_instance=RequestContext(request))    
            if request.POST['word1'] !=  request.POST['word2']:
                return render_to_response('password_change.html',{'sameerror':'True'}, context_instance=RequestContext(request))   
            if len(request.POST['word1']) < 6:
                return render_to_response('password_change.html',{'short':'True'}, context_instance=RequestContext(request))    
            user.set_password(request.POST['word1'])
            user.save()
            return render_to_response('password_change.html',{'change':'True'}, context_instance=RequestContext(request))
        else:
            return render_to_response('password_change.html',{'blank':'True'}, context_instance=RequestContext(request))
    
    return render_to_response('password_change.html',context_instance=RequestContext(request))
    
    
@login_required
def profilechange(request):
    user = request.user
    profile = user.get_profile()
    change = False
    form = ProfileChangeForm(request.POST)
    if request.method == 'POST':   
       if form.is_valid():
            cd = form.cleaned_data
            course.prerequisites = cd['prerequisites']
            course.max_student = cd['max_student']
            course.save()              
        
       
    else:
        form = ProfileChangeForm()
       
       
       
        user.save()
        profile.save()
        change = True
        return render_to_response('profile_change.html',locals(), context_instance=RequestContext(request))             
    return render_to_response('profile_change.html',locals(), context_instance=RequestContext(request))
    
    

