from django.shortcuts import render
from signupin.forms import UserForm,UserProfileInfoForm
from signupin.models import CFSchedules
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import requests
from bs4 import BeautifulSoup


def index(request):
    return render(request,'signupin/index.html')

@login_required
def schedules(request):
    page = requests.get('https://codeforces.com/contests')
    soup = BeautifulSoup(page.content,'html.parser')
    ctable = soup.find('div',{'class':'datatable'})
    crows = ctable.find_all('tr')
    for contest in crows[1:]:
        cn = {}
        cn['cid'] = contest.get('data-contestid')
        if CFSchedules.objects.filter(pk=cn['cid']).exists():
            print('already done')
            break
        cn['cname'] = contest.find('td').text[2:-6]
        atags = contest.find_all('a')
        csched = ''
        for atag in atags:
            if(atag['href'][:16]=='https://www.time'):
                csched = atag.text[1:-1]
                break
        cn['date'] = csched.split(' ')[0]
        cn['time'] = csched.split(' ')[1]
        print('saving to DB')
        cfobj = CFSchedules.objects.create(cid=cn['cid'],
                           cname=cn['cname'],
                           date=cn['date'],
                           time=cn['time'],)
    print('fetching done!')

    datas = CFSchedules.objects.all()
    cntdata = {
        "cnts": datas
        }
    return render(request,'signupin/schedules.html',cntdata)

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
