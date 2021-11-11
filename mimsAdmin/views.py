from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponseRedirect,JsonResponse
from .models import *
from django.db.models import Q




class hasPermission:
    def __init__(self, request, Path):
        self.Path = Path
        self.request = request
    
    def PermissionStatus(self):
        LoginId = self.request.session['loginid'] 
        print(LoginId)
        if UserTable.objects.get(id=LoginId).status == 'active':
            RoleOfUser = UserTable.objects.get(id=LoginId).userRole
            PermissionOfUser = Permissions.objects.all().filter(PermissionOfRole=RoleOfUser)
            Parent = [str(x.ParentPath).lower() for x in ParentPath.objects.all()]
            PathForPermission = [str(x.PathForPermission).lower() for x in PermissionOfUser]
            if self.Path.lower() in PathForPermission:
                return True
            elif self.Path.lower() in Parent:
                return True
            else:
                return False
        else:
            return False
# Create your views here.

def admin(request):
    print('get admin')
    return render(request,'admin.html')


def login(request):
    if request.method=='POST':
        user_name = request.POST['username']
        passwd = request.POST['password']
        a=UserTable.objects.get(username=user_name,PSWD=passwd)
        print(a)
        if a:           
            request.session['loginid']=a.id
            container = {'LogPerson':a}
            messages.success(request, 'Login successfully!')
            return render(request,'index.html',container)
        else:
            messages.error(request, 'Username and Password mismatch')
            return render(request,'admin.html')

    return render(request,'admin.html')

def loginPerson(request):
    login_id = request.session['loginid']  
    if login_id:
        a=UserTable.objects.get(id=login_id)
        container = {'LogPerson':a}
        return container
    else:
        return HttpResponse('not')

def index(request):
    container = loginPerson(request)
    return render(request,'index.html',container)



def logout(request):
    try:
        print('logout')
        del request.session['loginid']
        return render(request,'admin.html')
    except KeyError:
        pass
    messages.success(request, 'Logout successfully Completed')
    return render(request,'admin.html')


def holiday(request):
    #check whether the logined user has permission to access this view
    #has_permission('holiday') ---loginuser read read role --read permission
    holiday_list = Holidays.objects.all()
    container = loginPerson(request)
    container['holiday_list'] = holiday_list
    return render(request,'Holiday.html',container)

def addholiday(request):
    return render(request,'addholiday.html')

def holiAddition(request):
    holiday_name = request.POST['holiday_name']
    holiday_date = request.POST['holiday_date']
    a=Holidays(Holiday_name=holiday_name,Holiday_date=holiday_date,Holiday_status='inactive')
    a.save()
    # print(holiday_name,holiday_date)
    return render(request,'addholiday.html')


def inverts(request,pk):
    Holiday = Holidays.objects.get(id=pk)
    container = {'update':Holiday}
    print(Holiday.id)
    if Holiday.Holiday_status == 'active':
        return render(request,'inactivate.html',container)
    else:
        return render(request,'activate.html',container)    

def active(request):
    if request.method=='POST':
        ActiveByID = request.POST['a_id']
        Holidays.objects.filter(id=ActiveByID).update(Holiday_status='active')
        holiday_list = Holidays.objects.all()
        container = loginPerson(request)
        container['holiday_list'] = holiday_list
        return render(request,'Holiday.html',container)


def inactive(request):
    if request.method=='POST':
        InactiveByID = request.POST['i_id']
        Holidays.objects.filter(id=InactiveByID).update(Holiday_status='inactive')
        holiday_list = Holidays.objects.all()
        container = loginPerson(request)
        container['holiday_list'] = holiday_list
        return render(request,'Holiday.html',container)       


def filterHoliday(request):
    container = loginPerson(request)
    if request.method=='POST':
        filterByName = request.POST['filterByName']
        filterByDate = request.POST['filterByDate']
        if filterByName:
            container['holiday_list'] = Holidays.objects.filter(Q(Holiday_name__icontains=filterByName))
        if filterByDate:
            container['holiday_list'] = Holidays.objects.filter(Holiday_date=filterByDate)
        if not filterByName and not filterByDate:
            container['holiday_list'] = Holidays.objects.all()
    return render(request,'Holiday.html',container) 



