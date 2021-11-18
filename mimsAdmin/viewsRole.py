from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponseRedirect,JsonResponse
from .models import *
from django.db.models import Q
from .views import loginPerson
from .forms import *
from django.shortcuts import redirect
from .views import hasPermission
from django.core import serializers






def role(request):
    container = loginPerson(request)
    container['role'] = Role.objects.all()
    return render(request,'role.html',container)

# add role
def addRole(request):
    Permission = hasPermission(request,'add role').PermissionStatus()
    print(Permission)
    if Permission:
        container = loginPerson(request)
        return render(request,'addRole.html',container)
    else:
        messages.warning(request, "You are not allowed to access")
        return HttpResponseRedirect('role')
def roleAddition(request):
    if request.method == 'POST':
        roleForm = RoleForm(request.POST)
        if roleForm.is_valid():
            roleForm.save()
    return HttpResponseRedirect('role')

#disable the role
def actInact(request,pk):
    Permission = hasPermission(request,'disable role').PermissionStatus()
    if Permission:
        updateData = Role.objects.get(id=pk)
        container = {'update':updateData}
        if updateData.roleStatus == 'active':
            return render(request,'inactiverole.html',container)
        else:
            return render(request,'activerole.html',container)
    else:
        messages.warning(request, "You are not allowed to access")
        return HttpResponseRedirect('role')
def roleinactive(request):
    if request.method == 'POST':
        UpdateId = request.POST['i_id']
        Role.objects.filter(id=UpdateId).update(roleStatus='inactive')
        data = Role.objects.get(id=UpdateId)
        msg = '{} Inactivated'.format(data.roleName)
        messages.warning(request, msg)
        return HttpResponseRedirect('role')
def roleactive(request):
    if request.method == 'POST':
        UpdateId = request.POST['i_id']
        Role.objects.filter(id=UpdateId).update(roleStatus='active')
        data = Role.objects.get(id=UpdateId)
        msg = '{} Activated'.format(data.roleName)
        messages.success(request, msg)
        return HttpResponseRedirect('role')

#edit role
def editRole(request,pk):
    Permission = hasPermission(request,'edit role').PermissionStatus()
    if Permission:
        container = loginPerson(request)
        roleData = Role.objects.get(id=pk)
        container['role'] = roleData
        return render(request,'editRole.html',container)
    else:
        messages.warning(request, "You are not allowed to access")
        return HttpResponseRedirect('role')
def roleEdit(request):
    if request.method == 'POST':
        roleName = request.POST['roleName']
        roleStatus = request.POST['roleStatus']
        UpdateId = request.POST['editId']
        if roleName and roleStatus:
            Role.objects.filter(id=UpdateId).update(
                roleName=roleName,
                roleStatus=roleStatus
            )
            messages.success(request,'successfully Updated')
        else:
            messages.warning(request,'Something went wrong')
    return HttpResponseRedirect('role')

#____path______
def path(request):
    container = loginPerson(request)
    container['path'] = ParentPath.objects.all()
    return render(request,'path.html',container)

# add path
def addPath(request):
    Permission = hasPermission(request,'add path').PermissionStatus()
    if Permission:
        container = loginPerson(request)
        container['parentpath'] = ParentPath.objects.all()
        # container['countpath'] = Path.objects.all().count()
        return render(request,'addpath.html',container)
    else:
        messages.warning(request, "You are not allowed to access")
        return HttpResponseRedirect('path')        
def pathAddition(request):
    container = loginPerson(request)
    if request.method == 'POST':
        pathName = request.POST['pathName']
        parent = request.POST['parent']
        path = request.POST['Path']
        status = request.POST['status']
        SortOrder = request.POST['SortOrder']
        if parent:
            if parent == 'none':
                try:
                    ParentPath(ParentPath=pathName).save()
                    messages.success(request,'{} Added as a Parent Path'.format(pathName))
                    return HttpResponseRedirect('path')
                except:
                    messages.warning(request,'This Parent Path Already Exist')
                    return HttpResponseRedirect('path')
            else:
                ParentDet = ParentPath.objects.get(id=parent)
                PathData = Path(
                    pathName = pathName,
                    parent = ParentDet,
                    status  = status,
                    Path = path,
                    SortOrder = SortOrder
                )
                PathData.save()
                messages.success(request,'{} Path Added'.format(pathName))
                return HttpResponseRedirect('path')
    return HttpResponseRedirect('path')

#edit path
def editPath(request,pk):
    Permission = hasPermission(request,'edit path').PermissionStatus()
    if Permission:                   
        container = loginPerson(request)
        container['parentpath'] = ParentPath.objects.all()
        container['pathDetails'] = ParentPath.objects.get(id=pk)
        return render(request,'editpath.html',container)
    else:
        messages.warning(request, "You are not allowed to access")
        return HttpResponseRedirect('path')         
def PathEdit(request):
    if request.method == 'POST':
        pathName = request.POST['pathName']
        parent = request.POST['parent']
        path = request.POST['Path']
        status = request.POST['status']
        SortOrder = request.POST['SortOrder']
        Pathid = request.POST['Pathid']
        if parent:
            if parent == 'none':                
                Parentdata = ParentPath.objects.get(id=Pathid)
                ParentPath.objects.filter(id=Pathid).update(ParentPath=pathName)
                messages.success(request,'{} succesfully updated to {} '.format(Parentdata.ParentPath,pathName))
                return HttpResponseRedirect('path')

            else:
                ParentPath.objects.filter(id=Pathid).delete()
                try:
                    ParentDet = ParentPath.objects.get(id=parent)
                    PathData = Path(
                        pathName = pathName,
                        parent = ParentDet,
                        status  = status,
                        Path = path,
                        SortOrder = SortOrder
                    )
                    PathData.save()
                    messages.success(request,'{} Path Added as child path'.format(pathName))
                    return HttpResponseRedirect('path')
                except:
                    messages.success(request,'selected Prent Path is same as the path you are taken')
                    return HttpResponseRedirect('path')

#__Permissions__
def permisson(request,pk):
    container = loginPerson(request)
    parentpath = ParentPath.objects.all()
    container['parentpath'] = parentpath
    path = Path.objects.all()
    #order path by sortby
    a=Path.objects.order_by('SortOrder')
    print(a)
    container['path'] = Path.objects.order_by('SortOrder')

    container['InRole'] = Role.objects.get(id=pk)
    DefaultPermission = Permissions.objects.all().filter(PermissionOfRole=pk)
    Checked=[]
    ParentChecked = []
    for i in DefaultPermission:
        ParentChecked.append(i.PathForPermission.parent.id)
        Checked.append(i.PathForPermission.id)
    container['Checked'] = Checked
    container['Parentcheck'] = ParentChecked
    print(ParentChecked)
    return render(request,'permission.html',container)

# set permission
def savePermission(request):
    print('save Permissions')
    Permission = hasPermission(request,'set permission').PermissionStatus()
    PersonId = request.POST['RoleId']
    if Permission:
        if request.method == 'POST':
            RoleId = request.POST['RoleId']
            PermissionList = request.POST.getlist('permissions[]')
            RoleData = Role.objects.get(id=RoleId)
            print(PermissionList)
            crossCheck = Permissions.objects.all().filter(PermissionOfRole=RoleData)
            if crossCheck:
                crossCheck.delete()
                for i in PermissionList:
                    PathData = Path.objects.get(id=i)
                    Permissions(
                        PermissionOfRole = RoleData,
                        PathForPermission = PathData
                    ).save()
                msg = 'Permission of {} updated'.format(RoleData.roleName)
            else:
                for i in PermissionList:
                    PathData = Path.objects.get(id=i)
                    Permissions(
                        PermissionOfRole = RoleData,
                        PathForPermission = PathData
                    ).save()  
                msg = 'Permission of {} saved'.format(RoleData.roleName)    
            messages.success(request,msg)
            return HttpResponseRedirect('role')
        return HttpResponseRedirect('role')
    else:
        messages.warning(request, "Only Super User Can set Permissions")
        return redirect('permisson',pk=PersonId)          


def deletePath(request,pk):
    return HttpResponseRedirect('path')


#___user___
def user(request):
    container = loginPerson(request)
    container['role'] = Role.objects.all()
    container['dep'] = department.objects.all()
    container['user1'] = UserTable.objects.all()
    return render(request,'user.html',container)

#add user
def addUser(request):
    Permission = hasPermission(request,'add user').PermissionStatus()
    if Permission:
        container = loginPerson(request)
        container['dep'] = department.objects.all()
        container['role'] = Role.objects.all()
        return render(request,'adduser.html',container)
    else:
        messages.warning(request, "You are not allowed to access")
        return HttpResponseRedirect('user')          
def userAddition(request):
    if request.method == 'POST':
        name = request.POST['Name']
        Phone = request.POST['Phone']
        role = request.POST['role']
        department = request.POST['department']
        Status = request.POST['Status']
        Email = request.POST['Email']
        username = request.POST['Username']
        password = request.POST['password']
        roledata = Role.objects.get(id=role)
        if name:
            UserTable(
                name=name,
                phone=Phone,
                userRole=roledata,
                userDepartMent=department,
                status=Status,
                Email=Email,
                username=username,
                PSWD=password
            ).save()
    return HttpResponseRedirect('user')
def userFilter(request):
    container = loginPerson(request)
    container['role'] = Role.objects.all()
    container['dep'] = department.objects.all()
    if request.method == "POST":
        filterByName = request.POST['filterByName']
        FilterByRole = request.POST['FilterByRole']
        FilterByDep = request.POST['FilterByDep']
        FilterByStatus = request.POST['FilterByStatus']
        print(filterByName)
        print(FilterByRole)
        print(FilterByDep)
        print(FilterByStatus)
        if filterByName:
            container['user1'] =  UserTable.objects.filter(Q(name__icontains=filterByName))
        if FilterByRole:
            container['user1'] =  UserTable.objects.filter(userRole=FilterByRole)
        if FilterByDep:
            container['user1'] =  UserTable.objects.filter(Q(userDepartMent__icontains=FilterByDep))
        if FilterByStatus:
            container['user1'] =  UserTable.objects.filter(status=FilterByStatus)
            print(container['user1'])
        if not filterByName  and not FilterByRole and not FilterByDep and not FilterByStatus:
            container['user1'] = UserTable.objects.all()
    return render(request,'user.html',container)

#view user
def viewUser(request,pk):
    Permission = hasPermission(request,'view user').PermissionStatus()
    if Permission:
        container = loginPerson(request)
        container['user'] = UserTable.objects.get(id=pk)
        return render(request,'userView.html',container)
    else:
        messages.warning(request, "You are not allowed to access")
        return HttpResponseRedirect('user') 
#set password or change password
def ChangePSWD(request):
    print('change')
    Permission = hasPermission(request,'change password').PermissionStatus()
    PersonId = request.POST['IdOfPerson']
    if Permission:
        if request.method == 'POST':
            OldPassword = request.POST['OldPSWD']
            if PersonId:
                print('person id get')
                SecurityCheck = UserTable.objects.filter(id=PersonId,PSWD=OldPassword)
                if SecurityCheck:
                    
                    NewPSWD = request.POST['NewPSWD']
                    ConfirmPSWD = request.POST['ConfirmPSWD']
                    if NewPSWD == ConfirmPSWD:
                        SecurityCheck.update(PSWD=NewPSWD)
                        messages.success(request,'Password succesfully changed')
                        return redirect('viewUser',pk=PersonId)
                    else:
                        messages.error(request,'Mismatch')
                        return redirect('viewUser',pk=PersonId)
                else:
                    messages.error(request,'Incorrect Old Password')
                    return redirect('viewUser',pk=PersonId)
    else:
        messages.warning(request, "You are not allowed to change password")
        return redirect('viewUser',pk=PersonId)

#edit user    
def EditUser(request,pk):
    Permission = hasPermission(request,'edit user').PermissionStatus()
    if Permission:
        container = loginPerson(request)
        container['user'] = UserTable.objects.get(id=pk)
        container['role'] = Role.objects.all()
        container['dep'] = department.objects.all()
        print(container['user'])
        return render(request,'edituser.html',container)
    else:
        messages.warning(request, "You are not allowed to access")
        return HttpResponseRedirect('user')        
def UpdateUser(request):
    if request.method == 'POST':
        name = request.POST['Name']
        Phone = request.POST['Phone']
        role = request.POST['role']
        department = request.POST['department']
        Status = request.POST['Status']
        Email = request.POST['Email']
        roledata = Role.objects.get(id=role)
        PersonId = request.POST['PersonId']
        
        if PersonId:
            Userdata = UserTable.objects.filter(id=PersonId)
            msg = '{} updated successfully'.format(UserTable.objects.get(id=PersonId).name)
            Userdata.update(
                name = name,
                phone = Phone,
                Email = Email,
                userRole = roledata,
                userDepartMent = department,
                status = Status
            )
            messages.success(request,msg)
            return HttpResponseRedirect('user')
        else:
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect('user')
#disable user            
def statuser(request,pk):
    Permission = hasPermission(request,'edit user').PermissionStatus()
    if Permission:    
        if request.method=='GET':
            container = loginPerson(request)
            container['user'] = UserTable.objects.get(id=pk)
            if UserTable.objects.get(id=pk).status=='active':
                return render(request,'inactiveuser.html',container)
            else:
                return render(request,'activeuser.html',container)
    else:
        messages.warning(request, "You are not allowed to access")
        return HttpResponseRedirect('user')         
def inactivateUser(request):
    if request.method=='POST':
        UserId = request.POST['a_id']
        if UserId:
            UserTable.objects.filter(id=UserId).update(
                status='inactive'
            )
            msg = '{} is inactivated'.format(UserTable.objects.get(id=UserId).name)
            messages.warning(request,msg)
            return HttpResponseRedirect('user')
    return HttpResponseRedirect('user')
def activateUser(request):
    if request.method=='POST':
        UserId = request.POST['a_id']
        if UserId:
            UserTable.objects.filter(id=UserId).update(
                status='active'
            )
            msg = '{} is activated'.format(UserTable.objects.get(id=UserId).name)
            messages.success(request,msg)
            return HttpResponseRedirect('user')
    return HttpResponseRedirect('user')


#__conferenceOrganizer__
def conferenceOrganizer(request):
    if 'loginid' in request.session:
        container = loginPerson(request)
        container['Organizers'] = ConferenceOrganizerTable.objects.all()
        if request.method=="POST":
            filterByName = request.POST['filterByName']
            container['Organizers'] = ConferenceOrganizerTable.objects.filter(Q(Organizezr_Name__icontains=filterByName))
            return render(request,'conferenceOrganizer.html',container)
        return render(request,'conferenceOrganizer.html',container)
    else:
        return HttpResponseRedirect('/')
#add conference organizer
def addOrganizer(request):
    if 'loginid' in request.session:
        container = loginPerson(request)
        Permission = hasPermission(request,'add conference organizer').PermissionStatus()
        if Permission:   
            container['Form']=OrganizerForm()
            if request.method == 'POST':
                OrganizerFormData = OrganizerForm(request.POST)
                if OrganizerFormData.is_valid():
                    OrganizerFormData.save()
                    return HttpResponseRedirect('conferenceOrganizer')
            return render(request,'addorganizer.html',container)
        else:
            messages.warning(request, "You are not allowed to access")
            return HttpResponseRedirect('conferenceOrganizer')             
    else:
        return HttpResponseRedirect('/')
#edit conference organizer
def editOrganizer(request,pk):
    if 'loginid' in request.session:
        Permission = hasPermission(request,'edit conference organizer').PermissionStatus()
        if Permission: 
            container = loginPerson(request)
            if request.method=='POST':
                instance = ConferenceOrganizerTable.objects.get(id=pk)
                OrganizerFormData = OrganizerForm(request.POST,instance=instance)
                if OrganizerFormData.is_valid():
                    OrganizerFormData.save()
                    return HttpResponseRedirect('conferenceOrganizer')
                else:
                    pass
            form = OrganizerForm(initial = {
                'Organizezr_Name':ConferenceOrganizerTable.objects.get(id=pk).Organizezr_Name,
                'Organizezr_status':ConferenceOrganizerTable.objects.get(id=pk).Organizezr_status
            })
            container['form'] = form
            container['userid'] = pk
            return render(request,'editOrganizer.html',container)
        else:
            messages.warning(request, "You are not allowed to access")
            return HttpResponseRedirect('conferenceOrganizer')
    else:
        return HttpResponseRedirect('/')
    return render(request,'editOrganizer.html',container)
#disable organizer
def disableOrganizer(request): 
    if 'loginid' in request.session:  
        Permission = hasPermission(request,'disable organizer').PermissionStatus()
        if Permission: 
            if request.method=="POST":
                getById = request.POST['getById']
                if ConferenceOrganizerTable.objects.get(id=getById).Organizezr_status == 'active':
                    ConferenceOrganizerTable.objects.filter(id=getById).update(Organizezr_status='inactive')
                    messages.warning(request, "{} is Inactivated".format(ConferenceOrganizerTable.objects.get(id=getById).Organizezr_Name))
                else:
                    ConferenceOrganizerTable.objects.filter(id=getById).update(Organizezr_status='active')
                    messages.success(request, "{} is Activated".format(ConferenceOrganizerTable.objects.get(id=getById).Organizezr_Name))
            return HttpResponseRedirect('conferenceOrganizer')
        else:
            messages.warning(request, "You are not allowed to access")
            return HttpResponseRedirect('conferenceOrganizer')            
    else:
        return HttpResponseRedirect('/')

#__books__
def books(request):
    container = loginPerson(request)
    container['books'] = BooksTable.objects.all()
    container['dep'] = department.objects.all()
    if request.method=="POST":
        FilterByDep=request.POST['FilterByDep']
        filterByAuther=request.POST['filterByAuther']
        filterByName=request.POST['filterByName']      
        if FilterByDep:
            container['books'] = BooksTable.objects.filter(Department__id=FilterByDep)
        if filterByAuther:
            container['books']=BooksTable.objects.filter(Q(Auther_Name__icontains=filterByAuther))
        if filterByName:
            container['books']=BooksTable.objects.filter(Q(Books_Name__icontains=filterByName))
        else:
            container['books'] = BooksTable.objects.all()
    else:
        pass
    return render(request,'books.html',container)
    
#add books
def addbook(request):
    if 'loginid' in request.session: 
        Permission = hasPermission(request,'add books').PermissionStatus()
        if Permission: 
            container = loginPerson(request)
            container['form'] = BooksForm()
            if request.method=="POST":
                BookData=BooksForm(request.POST)
                if BookData.is_valid():
                    BookData.save() 
                    messages.success(request, "{} added".format(BookData.cleaned_data['Books_Name']))
                    return HttpResponseRedirect('books')
                else:
                    messages.warning(request, "{} is alreday existed".format(BookData.cleaned_data['Books_Name']))
                    return HttpResponseRedirect('books')
            return render(request,'addbook.html',container)
        else:
            messages.warning(request, "You are not allowed to access")
            return HttpResponseRedirect('books')  
    else:
        return HttpResponseRedirect('/')
#view book
def viewBook(request,pk):
    if 'loginid' in request.session:
        Permission = hasPermission(request,'edit book').PermissionStatus()
        if Permission: 
            container = loginPerson(request)
            container['book'] = BooksTable.objects.get(id=pk)
            return render(request,'viewbooks.html',container)
        else:
            messages.warning(request, "You are not allowed to access")
            return HttpResponseRedirect('books')  
    else:
        return HttpResponseRedirect('/')          
#edit book
def editBook(request,pk):
    if 'loginid' in request.session:
        Permission = hasPermission(request,'edit book').PermissionStatus()
        if Permission: 
            container = loginPerson(request)
            if request.method=="POST":
                instance = BooksTable.objects.get(id=pk)
                BooksTableDate = BooksForm(request.POST,instance=instance)
                if BooksTableDate.is_valid():
                    BooksTableDate.save()
                    messages.success(request,'{} successfully updated'.format(BooksTableDate.cleaned_data['Books_Name']))
                    return HttpResponseRedirect('books')
                else:
                    messages.warning(request,'something went wrong')
                    return HttpResponseRedirect('books')
            form = BooksForm(initial = {
                'Books_Name':BooksTable.objects.get(id=pk).Books_Name,
                'Auther_Name':BooksTable.objects.get(id=pk).Auther_Name,
                'Books_availability':BooksTable.objects.get(id=pk).Books_availability,
                'Books_Edition':BooksTable.objects.get(id=pk).Books_Edition,
                'Short_Summary':BooksTable.objects.get(id=pk).Short_Summary,
                'Department':BooksTable.objects.get(id=pk).Department.all()
            })
            container['form'] = form
            container['userid'] = pk
            return render(request,'editBooks.html',container)
        else:
            messages.warning(request, "You are not allowed to access")
            return HttpResponseRedirect('books')            
    else:
        return HttpResponseRedirect('/')
#disable book
def disableBook(request):
    if 'loginid' in request.session:
        Permission = hasPermission(request,'edit book').PermissionStatus()
        if Permission: 
            if request.method=="POST":
                getById = request.POST['getById']
                if BooksTable.objects.get(id=getById).Books_status == 'active':
                    BooksTable.objects.filter(id=getById).update(Books_status='inactive')
                    messages.warning(request, "{} is Inactivated".format(BooksTable.objects.get(id=getById).Books_Name))
                else:
                    BooksTable.objects.filter(id=getById).update(Books_status='active')
                    messages.success(request, "{} is Activated".format(BooksTable.objects.get(id=getById).Books_Name))
            return HttpResponseRedirect('books')
        else:
            messages.warning(request, "You are not allowed to access")
            return HttpResponseRedirect('books') 
    else:
        return HttpResponseRedirect('/')

#__log master__
def logMaster(request):
    container = loginPerson(request)
    container['logMasters'] = LogMasterTable.objects.all()
    if request.method=="POST":
        filterByName=request.POST['filterByName']
        if filterByName:
            container['logMasters']=LogMasterTable.objects.filter(Q(Name__icontains=filterByName))
    return render(request,'logmaster.html',container)
#add log master
def addLogMaster(request):
    if 'loginid' in request.session:
        Permission = hasPermission(request,'add log master').PermissionStatus()
        if Permission: 
            container = loginPerson(request)
            container['form'] = LogMasterForm()
            if request.method=="POST":
                LogData = LogMasterForm(request.POST)
                if LogData.is_valid():
                    LogData.save()
                    return HttpResponseRedirect('logMaster')
            return render(request,'addLog.html',container)
        else:
            messages.warning(request, "You are not allowed to access")
            return HttpResponseRedirect('logMaster') 
    else:
        return HttpResponseRedirect('/')
#disable log master
def disableLog(request):
    if 'loginid' in request.session:
        Permission = hasPermission(request,'disable log master').PermissionStatus()
        if Permission:
            if request.method=="POST":
                getById=request.POST['getById']
                if getById:
                    if LogMasterTable.objects.get(id=getById).status=='inactive':
                        LogMasterTable.objects.filter(id=getById).update(status='active')
                        messages.success(request,'{} activated'.format(LogMasterTable.objects.get(id=getById).Name))
                        return HttpResponseRedirect('logMaster')
                    else:
                        messages.warning(request,'{} inactivated'.format(LogMasterTable.objects.get(id=getById).Name))
                        LogMasterTable.objects.filter(id=getById).update(status='inactive')
                        return HttpResponseRedirect('logMaster')
            return HttpResponseRedirect('logMaster')
        else:
            messages.warning(request, "You are not allowed to access")
            return HttpResponseRedirect('logMaster') 
    else:
        return HttpResponseRedirect('/')
#edit log master
def editLog(request,pk):
    if 'loginid' in request.session:
        Permission = hasPermission(request,'edit log master').PermissionStatus()
        if Permission:
            container=loginPerson(request)
            if request.method=="POST":
                instance = LogMasterTable.objects.get(id=pk)
                LogMasterData = LogMasterForm(request.POST,instance=instance)
                if LogMasterData.is_valid():
                    LogMasterData.save()
                    messages.success(request,'{} successfully updated'.format(LogMasterData.cleaned_data['Name']))
                    return HttpResponseRedirect('logMaster')
                else:
                    pass
            form = LogMasterForm(initial = {
                'Name':LogMasterTable.objects.get(id=pk).Name,
                'status':LogMasterTable.objects.get(id=pk).status,
                'TableHeads':LogMasterTable.objects.get(id=pk).TableHeads.all()
            })
            container['form'] = form
            container['userid'] = pk
            return render(request,'editLog.html',container)
        else:
            messages.warning(request, "You are not allowed to access")
            return HttpResponseRedirect('logMaster') 
    else:
        return HttpResponseRedirect('/')
#view log master
def viewLog(request,pk):
    if 'loginid' in request.session:
        Permission = hasPermission(request,'view log master').PermissionStatus()
        if Permission:
            container=loginPerson(request)
            container['logMaster'] = LogMasterTable.objects.get(id=pk)
            return render(request,'viewLog.html',container)
        else:
            messages.warning(request, "You are not allowed to access")
            return HttpResponseRedirect('logMaster') 
    else:
        return HttpResponseRedirect('/')

#__publications__
def publications(request):
    container = loginPerson(request)
    container['publications'] = PublicationTable.objects.all()
    if request.method=="POST":
        filterByTitle=request.POST['filterByTitle']
        if filterByTitle:
            container['publications'] = PublicationTable.objects.filter(Q(Publication_Title__icontains=filterByTitle))
    return render(request,'publications.html',container)
#add publications
def addPublications(request):
    if 'loginid' in request.session:
        Permission = hasPermission(request,'add publications').PermissionStatus()
        if Permission:
            if request.method=="POST":
                PublicationData = PublicationForm(request.POST)
                if PublicationData.is_valid():
                    PublicationData.save()
                    messages.success(request,'publication {} added'.format(PublicationData.cleaned_data['Publication_Title']))
                    return HttpResponseRedirect('publications')
                else:
                    pass
            container = loginPerson(request)
            container['form'] = PublicationForm()
            return render(request,'addpublications.html',container)
        else:
            messages.warning(request, "You are not allowed to access")
            return HttpResponseRedirect('publications') 
    else:
        return HttpResponseRedirect('/')
#edit publications
def editPublications(request,pk):
    if 'loginid' in request.session:
        Permission = hasPermission(request,'edit publications').PermissionStatus()
        if Permission:
            if request.method=="POST":
                instance = PublicationTable.objects.get(id=pk)
                PublicationData = PublicationForm(request.POST,instance=instance)
                if PublicationData.is_valid():
                    PublicationData.save()
                    messages.success(request,'{} updated successfully'.format(PublicationData.cleaned_data['Publication_Title']))
                    return HttpResponseRedirect('publications')
                else:
                    pass
            container=loginPerson(request)
            form = PublicationForm(initial = {
                'Publication_Title':PublicationTable.objects.get(id=pk).Publication_Title,
                'Volume':PublicationTable.objects.get(id=pk).Volume,
                'Publication_Author':PublicationTable.objects.get(id=pk).Publication_Author,
                'issue':PublicationTable.objects.get(id=pk).issue,
                'Publisher_name':PublicationTable.objects.get(id=pk).Publisher_name,
                'Website_Id':PublicationTable.objects.get(id=pk).Website_Id,
                'Journal':PublicationTable.objects.get(id=pk).Journal,
                'Date':PublicationTable.objects.get(id=pk).Date,
                'status':PublicationTable.objects.get(id=pk).status,
            })
            container['form'] = form
            container['userid'] = pk
            return render(request,'editpublications.html',container)
        else:
            messages.warning(request, "You are not allowed to access")
            return HttpResponseRedirect('publications') 
    else:
        return HttpResponseRedirect('/')
#disable publications
def disablePublications(request):
    if 'loginid' in request.session:
        Permission = hasPermission(request,'edit publications').PermissionStatus()
        if Permission:
            if request.method=="POST":
                getById=request.POST['getById']
                if getById:
                    if PublicationTable.objects.get(id=getById).status=='inactive':
                        PublicationTable.objects.filter(id=getById).update(status='active')
                        messages.success(request,'{} activated'.format(PublicationTable.objects.get(id=getById).Publication_Title))
                        return HttpResponseRedirect('publications')
                    else:
                        messages.warning(request,'{} inactivated'.format(PublicationTable.objects.get(id=getById).Publication_Title))
                        PublicationTable.objects.filter(id=getById).update(status='inactive')
                        return HttpResponseRedirect('publications')
            return HttpResponseRedirect('publications')
        else:
            messages.warning(request, "You are not allowed to access")
            return HttpResponseRedirect('publications') 
    else:
        return HttpResponseRedirect('/')
#view publications
def viewPublications(request,pk):
    container=loginPerson(request)
    container['publication']=PublicationTable.objects.get(id=pk)
    return render(request,'viewpublications.html',container)

#__journals__
def journals(request):
    container = loginPerson(request)
    container['journals'] = JournalsTable.objects.all()
    container['dep'] = department.objects.all()
    if request.method=="POST":
        filterByTitle =request.POST['filterByTitle']
        filterByPublisher =request.POST['filterByPublisher']
        FilterByDep =request.POST['FilterByDep']
        if filterByTitle:
            container['journals'] = JournalsTable.objects.filter(Q(Journal_name__icontains=filterByTitle))
        if filterByPublisher:
            container['journals'] = JournalsTable.objects.filter(Q(Publisher_name__icontains=filterByPublisher))
        if FilterByDep:
            container['journals'] = JournalsTable.objects.filter(Q(Journal_department__id=FilterByDep))
    return render(request,'journals.html',container)
#add journals
def addJournals(request):
    if 'loginid' in request.session:
        Permission = hasPermission(request,'add journals').PermissionStatus()
        if Permission:
            if request.method=="POST":
                JournalData=JournalsForm(request.POST)
                if JournalData.is_valid():
                    JournalData.save()
                    messages.success(request,'{} added succesfully'.format(JournalData.cleaned_data['Journal_name']))
                    return HttpResponseRedirect('journals')
                else:
                    pass
            container=loginPerson(request)
            container['form']=JournalsForm()
            return render (request,'addjournals.html',container)
        else:
            messages.warning(request, "You are not allowed to access")
            return HttpResponseRedirect('journals') 
    else:
        return HttpResponseRedirect('/')
#disable journals
def disableJournals(request):
    if 'loginid' in request.session:
        Permission = hasPermission(request,'disable journals').PermissionStatus()
        if Permission:
            if request.method=="POST":
                getById=request.POST['getById']
                if getById:
                    if JournalsTable.objects.get(id=getById).status=='inactive':
                        JournalsTable.objects.filter(id=getById).update(status='active')
                        messages.success(request,'{} activated'.format(JournalsTable.objects.get(id=getById).Journal_name))
                        return HttpResponseRedirect('journals')
                    else:
                        messages.warning(request,'{} inactivated'.format(JournalsTable.objects.get(id=getById).Journal_name))
                        JournalsTable.objects.filter(id=getById).update(status='inactive')
                        return HttpResponseRedirect('journals')
            return HttpResponseRedirect('journals')
        else:
            messages.warning(request, "You are not allowed to access")
            return HttpResponseRedirect('journals') 
    else:
        return HttpResponseRedirect('/')
#view journals
def viewJournal(request,pk):
    if 'loginid' in request.session:
        Permission = hasPermission(request,'view journals').PermissionStatus()
        if Permission:
            container=loginPerson(request)
            container['journal'] = JournalsTable.objects.get(id=pk)
            return render(request,'viewjournals.html',container)
        else:
            messages.warning(request, "You are not allowed to access")
            return HttpResponseRedirect('journals') 
    else:
        return HttpResponseRedirect('/')
#edit journals
def editJournals(request,pk):
    if 'loginid' in request.session:
        Permission = hasPermission(request,'edit journals').PermissionStatus()
        if Permission:
            if request.method=="POST":
                instance = JournalsTable.objects.get(id=pk)
                JournalData = JournalsForm(request.POST,instance=instance)
                if JournalData.is_valid():
                    JournalData.save()
                    messages.success(request,'{} successfully updated'.format(JournalData.cleaned_data['Journal_name']))
                    return HttpResponseRedirect('journals')
            container=loginPerson(request)
            form = JournalsForm(initial = {
                'Journal_name':JournalsTable.objects.get(id=pk).Journal_name,
                'Edition':JournalsTable.objects.get(id=pk).Edition,
                'Journal_department':JournalsTable.objects.get(id=pk).Journal_department.all(),
                'Published_Date':JournalsTable.objects.get(id=pk).Published_Date,
                'Publisher_name':JournalsTable.objects.get(id=pk).Publisher_name,
                'Journal_Type':JournalsTable.objects.get(id=pk).Journal_Type,
                'Short_Summary':JournalsTable.objects.get(id=pk).Short_Summary,
                'status':JournalsTable.objects.get(id=pk).status,
            })
            container['form'] = form
            container['userid'] = pk
            return render(request,'editjournal.html',container)
        else:
            messages.warning(request, "You are not allowed to access")
            return HttpResponseRedirect('journals') 
    else:
        return HttpResponseRedirect('/')

#__forms__
def form(request):
    container=loginPerson(request)
    container['forms'] = FormTable.objects.all()
    if request.method=="POST":
        filterByTitle=request.POST['filterByTitle']
        if filterByTitle:
            container['forms'] = FormTable.objects.filter(Q(Form_name__icontains=filterByTitle))
    return render(request,"forms.html",container)
#add form
def addForm(request):
    if 'loginid' in request.session:
        Permission = hasPermission(request,'add form').PermissionStatus()
        if Permission:
            if request.method=="POST":
                formData = formMasterForm(request.POST, request.FILES)
                print('check')
                if formData.is_valid():
                    print('valid')
                    formData.save()
                    messages.success(request,'{} successfully added'.format(formData.cleaned_data['Form_name']))
                    return HttpResponseRedirect('form')
            container=loginPerson(request)
            container['form'] = formMasterForm()
            return render(request,'addforms.html',container)
        else:
            messages.warning(request, "You are not allowed to access")
            return HttpResponseRedirect('form') 
    else:
        return HttpResponseRedirect('/')    
#disable form
def disableForms(request):
    if 'loginid' in request.session:
        Permission = hasPermission(request,'disable form').PermissionStatus()
        if Permission:
            if request.method=="POST":
                getById=request.POST['getById']
                if getById:
                    if FormTable.objects.get(id=getById).status=='inactive':
                        FormTable.objects.filter(id=getById).update(status='active')
                        messages.success(request,'{} activated'.format(FormTable.objects.get(id=getById).Form_name))
                        return HttpResponseRedirect('form')
                    else:
                        messages.warning(request,'{} inactivated'.format(FormTable.objects.get(id=getById).Form_name))
                        FormTable.objects.filter(id=getById).update(status='inactive')
                        return HttpResponseRedirect('form')
            return HttpResponseRedirect('form')
        else:
            messages.warning(request, "You are not allowed to access")
            return HttpResponseRedirect('form') 
    else:
        return HttpResponseRedirect('/') 
#edit form
def editForm(request,pk):
    if 'loginid' in request.session:
        Permission = hasPermission(request,'edit form').PermissionStatus()
        if Permission:
            if request.method=="POST":
                print('im here')
                instance = FormTable.objects.get(id=pk)
                formData = formMasterForm(request.POST,instance=instance)
                if formData.is_valid():
                    formData.save()
                    messages.success(request,'{} successfully updated'.format(formData.cleaned_data['Form_name']))
                    return HttpResponseRedirect('form')
                else:
                    pass
            container=loginPerson(request)
            container['userid']=pk
            form=formMasterForm(initial={
                'Form_name' : FormTable.objects.get(id=pk).Form_name,
                'Form' : FormTable.objects.get(id=pk).Form,
                'status' : FormTable.objects.get(id=pk).status
            })
            print(form)
            container['form']=form
            return render(request,'editform.html',container)
        else:
            messages.warning(request, "You are not allowed to access")
            return HttpResponseRedirect('form') 
    else:
        return HttpResponseRedirect('/') 
#view form
def viewForm(request,pk):
    if 'loginid' in request.session:
        Permission = hasPermission(request,'edit form').PermissionStatus()
        if Permission:
            container = loginPerson(request)
            container['form'] = FormTable.objects.get(id=pk)
            return render(request,'viewform.html',container)
        else:
            messages.warning(request, "You are not allowed to access")
            return HttpResponseRedirect('form') 
    else:
        return HttpResponseRedirect('/') 
# def filterForm(request):
#     if request.method == "GET":
#         FilterByName=request.GET['filterByName']
#         print(FilterByName)
#         data = FormTable.objects.filter(Q(Form_name__icontains=FilterByName))
#         print(data)
#         data1 = serializers.serialize('json', list(data), fields=('Form_name','Form'))
#         response={'data':data1}
#         return JsonResponse(response)