from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponseRedirect,JsonResponse
from .models import *
from django.db.models import Q
from .views import loginPerson
from .forms import RoleForm
from django.shortcuts import redirect


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



def role(request):
    container = loginPerson(request)
    container['role'] = Role.objects.all()
    return render(request,'role.html',container)

def addRole(request):
    Permission = hasPermission(request,'add role').PermissionStatus()
    print(Permission)
    if Permission:
        container = loginPerson(request)
        return render(request,'addRole.html',container)
    else:
        messages.warning(request, "ÿou can't access")
        return HttpResponseRedirect('role')

def roleAddition(request):
    if request.method == 'POST':
        roleForm = RoleForm(request.POST)
        if roleForm.is_valid():
            roleForm.save()
        # RoleName = request.POST['RoleName']
        # RoleStatus = request.POST['RoleStatus']
        # roleData = Role(
        #     roleName = RoleName,
        #     roleStatus = RoleStatus
        # )
        # roleData.save()

    return HttpResponseRedirect('role')
def actInact(request,pk):
    updateData = Role.objects.get(id=pk)
    container = {'update':updateData}
    if updateData.roleStatus == 'active':
        return render(request,'inactiverole.html',container)
    else:
        return render(request,'activerole.html',container)

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


def editRole(request,pk):
    container = loginPerson(request)
    roleData = Role.objects.get(id=pk)
    container['role'] = roleData
    return render(request,'editRole.html',container)

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

def path(request):
    container = loginPerson(request)
    container['path'] = ParentPath.objects.all()
    return render(request,'path.html',container)

def addPath(request):
    container = loginPerson(request)
    container['parentpath'] = ParentPath.objects.all()
    # container['countpath'] = Path.objects.all().count()
    return render(request,'addpath.html',container)

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

def editPath(request,pk):               
    container = loginPerson(request)
    container['parentpath'] = ParentPath.objects.all()
    container['pathDetails'] = ParentPath.objects.get(id=pk)
    return render(request,'editpath.html',container)

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


def savePermission(request):
    print('save Permissions')
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
      

def deletePath(request,pk):
    return HttpResponseRedirect('path')

def user(request):
    container = loginPerson(request)
    container['role'] = Role.objects.all()
    container['dep'] = department.objects.all()
    container['user1'] = UserTable.objects.all()
    return render(request,'user.html',container)

def addUser(request):
    container = loginPerson(request)
    container['dep'] = department.objects.all()
    container['role'] = Role.objects.all()
    return render(request,'adduser.html',container)

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

def viewUser(request,pk):
    container = loginPerson(request)
    container['user'] = UserTable.objects.get(id=pk)
    return render(request,'userView.html',container)

def ChangePSWD(request):
    print('change')
    if request.method == 'POST':
        OldPassword = request.POST['OldPSWD']
        PersonId = request.POST['IdOfPerson']
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
    
def EditUser(request,pk):
    container = loginPerson(request)
    container['user'] = UserTable.objects.get(id=pk)
    container['role'] = Role.objects.all()
    container['dep'] = department.objects.all()
    print(container['user'])
    return render(request,'edituser.html',container)

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

