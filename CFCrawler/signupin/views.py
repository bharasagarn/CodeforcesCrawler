from django.shortcuts import render
from signupin.forms import UserForm,UserProfileInfoForm
from signupin.models import CFSchedules
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .cfschedules import *
import datetime

def index(request):
    return render(request,'signupin/index.html')

@login_required
def schedules(request):
    cntdata = getFutureContests()
    return render(request,'signupin/schedules.html',{'cntdata':cntdata})

@login_required
def pastcfschedules(request):
    cnt = getPages()
    for p in range(int(cnt)):
        url = 'https://codeforces.com/contests/page/'+str(p+1)
        print('fetching page '+url)
        cntdata = getPastContestsHelper(url)
        f = True
        for cn in cntdata:
            cid = cn['cid']
            try:
                cexists = CFSchedules.objects.get(cid=cid)
                print(cexists)
                print('no further fetching!')
                f = False
                break
            except CFSchedules.DoesNotExist:
                cname = cn['cname']
                months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
                year = int(cn['date'][7:11])
                day = int(cn['date'][4:6])
                
                hr = int(cn['time'][:2])+2
                min = int(cn['time'][3:5])+30
                if min>=60:
                    min = min%60
                    hr = hr+1
                if hr>=24:
                    hr = hr%24
                    day = day+1
                print(str(year)+","+str(months[cn['date'][:3]])+","+str(day))
                print(str(hr)+","+str(min))
                date = datetime.date(int(year),int(months[cn['date'][:3]]),int(day))
                time = datetime.time(hr,min,0)
                CFSchedules.objects.create(cid=cid,cname=cname,date=date,time=time)
                print('created object for '+cid)
        if f==False:
            break
        print('all done for this page')
    print('all pages done')
    cntdata = CFSchedules.objects.all().order_by('-date')

    return render(request,'signupin/pastcfschedules.html',{'cntdata':cntdata})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def profile(request):
    return render(request,'signupin/profile.html')

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('dp found')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'signupin/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account inactive.")
        else:
            print("Login failed")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login credentials.")
    else:
        return render(request, 'signupin/login.html', {})
