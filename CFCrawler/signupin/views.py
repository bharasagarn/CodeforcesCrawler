from django.shortcuts import render
from signupin.forms import UserForm,UserProfileInfoForm
from signupin.models import CFSchedules
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .cfschedules import *

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
                date = cn['date']
                time = cn['time']
                CFSchedules.objects.create(cid=cid,cname=cname,date=date,time=time)
                print('created object for '+cid)
        if f==False:
            break
        print('all done for this page')
    print('all pages done')
    cntdata = CFSchedules.objects.all()

    return render(request,'signupin/pastcfschedules.html',{'cntdata':cntdata})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

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
