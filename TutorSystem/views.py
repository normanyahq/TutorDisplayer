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
    form = ProfileChangeForm(request.POST,instance=profile)
    if request.method == 'POST':   
       if form.is_valid():
           form.save()
    else:
       form = ProfileChangeForm(instance=profile)
           
    return render_to_response('profile_change.html',locals(), context_instance=RequestContext(request))

def imagehandle(request):
    user = request.user
    profile = user.get_profile()
    form = UploadImageForm(request.POST,request.FILES)
    if request.method == 'POST':
        if form.is_valid:
            #profile.potrait = request.FILES['file']
            sp = request
            sad
            profile.save()
    else:
        form = UploadImageForm()
    
    return render_to_response('image_upload_display.html',locals(), context_instance=RequestContext(request))
    

