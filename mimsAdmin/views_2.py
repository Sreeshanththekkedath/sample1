from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponseRedirect,JsonResponse
from .models import *
from .views import loginPerson
from .forms import *
from .filters import DepartmentFilter
from django.db.models import Q
from .views import hasPermission

#__department__
def Department(request):
    container = loginPerson(request)
    depList = department.objects.all()
    container['dep_list'] = depList
    return render(request,'department.html',container)
#add department
def add_department(request):
    container = loginPerson(request)
    depHead = departmentHead.objects.all()
    logBook = [
        'test1_logBook',
        'test2_logBook',
        'test3_logBook',
    ]
    container['departmentHead'] = depHead
    container['logBook'] = logBook
    return render(request,'add_department.html',container)
def depAddition(request):
    container = loginPerson(request)
    depHead = departmentHead.objects.all()
    logBook = [
        'test1_logBook',
        'test2_logBook',
        'test3_logBook',
    ]
    container['departmentHead'] = depHead
    container['logBook'] = logBook
    if request.method == 'POST':
        Department_name = request.POST['DepartmentName']
        Department_Head = request.POST['DepartmentHead']
        CourseDuration = request.POST['CourseDuration']
        programName = request.POST['programName']
        AccreditationRenewalDate = request.POST['AccreditationRenewalDate']
        FirstYearStipend = request.POST['FirstYearStipend']
        SecondYearStipend = request.POST['SecondYearStipend']
        ThirdYearStipend = request.POST['ThirdYearStipend']
        FourYearStipend = request.POST['FourYearStipend']
        FiveYearStipend = request.POST['FiveYearStipend']
        SixYearStipend = request.POST['SixYearStipend']
        log_book = request.POST.getlist('logBook[]')
        log_book = ','.join(log_book)
        # print(log_book)
        if not FiveYearStipend:
            FiveYearStipend='N/A'
        if not FourYearStipend:
            FourYearStipend='N/A'
        if not SixYearStipend:
            SixYearStipend='N/A'
        DepHead = departmentHead.objects.get(DepHead_name=Department_Head)
        try:
            crosCheck = department.objects.get(Department_name=Department_name,programName=programName,CourseDuration=CourseDuration)
        except:
            crosCheck = None
        if crosCheck:
            pass
        else:
            departmentTable = department(
                Department_name=Department_name,
                Department_Head=DepHead,
                CourseDuration=CourseDuration,
                programName=programName,
                log_book=log_book,
                AccreditationRenewalDate=AccreditationRenewalDate,
                FirstYearStipend=FirstYearStipend,
                SecondYearStipend=SecondYearStipend,
                ThirdYearStipend=ThirdYearStipend,
                FourYearStipend=FourYearStipend,
                FiveYearStipend=FiveYearStipend,
                SixYearStipend=SixYearStipend
            )
            departmentTable.save()
            messages.success(request, 'Department Added!')
    return render(request,'add_department.html',container)
#view department
def view_dep(request,pk):
    try:
        container = loginPerson(request)
    except:
        return render(request,'admin.html')
    depDetails = department.objects.get(id=pk)
    print(depDetails.Department_name)
    container['depDetails'] = depDetails
    # print(depDetails)
    return render(request,'depView.html',container) 
#edit department
def edit_dep(request,pk):
    try:
        container = loginPerson(request)
    except:
        return render(request,'admin.html')
    depHead = departmentHead.objects.all()
    logBook = [
        'test1_logBook',
        'test2_logBook',
        'test3_logBook',
    ]
    container['departmentHead'] = depHead
    container['logBook'] = logBook
    depDetails = department.objects.get(id=pk)
    print(depDetails.AccreditationRenewalDate)
    container['depDetails'] = depDetails
    return render(request,'depEdit.html',container) 
def UpdateDepartment(request):
    try:
        container = loginPerson(request)
    except:
        return render(request,'admin.html')
    if request.method == 'POST':
        Dep_id = request.POST['d_id']
        Department_name = request.POST['DepartmentName']
        Department_Head = request.POST['DepartmentHead']
        CourseDuration = request.POST['CourseDuration']
        programName = request.POST['programName']
        AccreditationRenewalDate = request.POST['AccreditationRenewalDate']
        FirstYearStipend = request.POST['FirstYearStipend']
        SecondYearStipend = request.POST['SecondYearStipend']
        ThirdYearStipend = request.POST['ThirdYearStipend']
        FourYearStipend = request.POST['FourYearStipend']
        FiveYearStipend = request.POST['FiveYearStipend']
        SixYearStipend = request.POST['SixYearStipend']
        status = request.POST['status']
        log_book = request.POST.getlist('logBook[]')
        log_book = ','.join(log_book)
        DepHead = departmentHead.objects.get(DepHead_name=Department_Head)
        # print(log_book)
        if not FiveYearStipend:
            FiveYearStipend='N/A'
        if not FourYearStipend:
            FourYearStipend='N/A'
        if not SixYearStipend:
            SixYearStipend='N/A'
        department.objects.filter(id=Dep_id).update(
            Department_name=Department_name,
            Department_Head=DepHead,
            CourseDuration=CourseDuration,
            programName=programName,
            log_book=log_book,
            AccreditationRenewalDate=AccreditationRenewalDate,
            FirstYearStipend=FirstYearStipend,
            SecondYearStipend=SecondYearStipend,
            ThirdYearStipend=ThirdYearStipend,
            FourYearStipend=FourYearStipend,
            FiveYearStipend=FiveYearStipend,
            SixYearStipend=SixYearStipend,
            dep_status=status
        )
        msg = '{} updated'.format(Department_name)
        messages.success(request, msg)
        return HttpResponseRedirect('Department')     
    return render(request,'department.html',container)
#disable department
def depinverts(request,pk):
    try:
        container = loginPerson(request)
    except:
        return render(request,'admin.html')
    depDetails = department.objects.get(id=pk)
    container['status'] = depDetails
    if depDetails.dep_status=='active':
        return render(request,'InactiveDep.html',container)
    else:
        return render(request,'ActiveDep.html',container)

    return render(request,'department.html',container)
def active_dep(request):
    try:
        container = loginPerson(request)
    except:
        return render(request,'admin.html')
    if request.method=='POST':
        InactiveByID = request.POST['a_id']
        dep = department.objects.get(id=InactiveByID)
        if dep.dep_status == 'inactive':
            department.objects.filter(id=InactiveByID).update(dep_status='active')
            depDetails = department.objects.all() 
            container['dep_list'] = depDetails
            msg = '{} Activated !'.format(dep.Department_name)
            messages.success(request, msg)
        else:
            depDetails = department.objects.all()
            container['dep_list'] = depDetails
    return render(request,'department.html',container)
def inactive_dep(request):
    try:
        container = loginPerson(request)
    except:
        return render(request,'admin.html')
    if request.method=='POST':
        InactiveByID = request.POST['i_id']
        dep = department.objects.get(id=InactiveByID)
        if dep.dep_status == 'active':
            department.objects.filter(id=InactiveByID).update(dep_status='inactive')
            depDetails = department.objects.all()
            container['dep_list'] = depDetails
            msg = '{} Inactivated !'.format(dep.Department_name)
            messages.warning(request, msg)
        else:
            depDetails = department.objects.all()
            container['dep_list'] = depDetails
    return render(request,'department.html',container)
def filterdepartment(request):
    try:
        container = loginPerson(request)
    except:
        return render(request,'admin.html')
    if request.POST:
        depName = request.POST['filterByName']
        print(depName)
        depList = department.objects.filter(Department_name__startswith=depName)
        container['dep_list'] = depList
    return render(request,'department.html',container)



#__faculty__
def faculty(request):
    container = loginPerson(request)
    FacultyDetails = Faculty.objects.all()
    departments = department.objects.all()
    container['dep'] = departments
    container['Faculty'] = FacultyDetails
    return render(request,'faculty.html',container)
#add faculty
def addfaculty(request):
    Permission = hasPermission(request,'add faculty').PermissionStatus()
    if Permission:
        departmets = department.objects.all()
        Course = course.objects.all()
        try:
            container = loginPerson(request)
        except:
            return render(request,'admin.html')
        container['dep'] = departmets
        container['course'] = Course
        return render(request,'addfaculty.html',container)
    else:
        messages.warning(request, "You are not allowed to access")
        return HttpResponseRedirect('faculty')
def additionFaculty(request):
    if request.method=='POST':
        FacultyName = request.POST['FacultyName']
        FacultyDepartment = request.POST['FacultyDepartment']
        Designation = request.POST['Designation']
        DateOfBirth = request.POST['DateOfBirth']
        PanNumber = request.POST['PanNumber']
        Photo = request.FILES['Photo']
        FacultyEligibility = request.POST['FacultyEligibility']
        PresentResidentialAddress = request.POST['PresentResidentialAddress']
        PermenentResidentialAddress = request.POST['PermenentResidentialAddress']
        PhotoIdProof = request.FILES['Photo1']
        PhotoId = request.POST['PhotoId']
        IssuingAuthority = request.POST['IssuingAuthority']
        Telephone = request.POST['Telephone']
        MobileNumber = request.POST['MobileNumber']
        MobileNumberAlt = request.POST['MobileNumberAlt']
        EmailId = request.POST['EmailId']
        PGExperience = request.POST['PGExperience']

        CourseName=request.POST.getlist('CourseName[]')
        SpecializationArea=request.POST.getlist('SpecializationArea[]')
        YearOfPassing = request.POST.getlist('YearOfPassing[]')
        NameOfCollege = request.POST.getlist('NameOfCollege[]')
        QualificationRegNo = request.POST.getlist('QualificationRegNo[]')
        MedicalCouncilName = request.POST.getlist('MedicalCouncilName[]')
        RegistrationValidUpto = request.POST.getlist('RegistrationValidUpto[]')
        Document = request.FILES.getlist('Document[]')
        count = request.POST.getlist('count[]')

        print(FacultyDepartment)
        FDepartment = department.objects.get(id = FacultyDepartment)
        try:
            crosCheck = Faculty.objects.get(
                FacultyName = FacultyName,
                FacultyDepartment = FDepartment,
                Designation = Designation,
                DateOfBirth = DateOfBirth,
                PanNumber = PanNumber,
                FacultyEligibility = FacultyEligibility,
                PresentResidential = PresentResidentialAddress,
                PermenentResidential = PermenentResidentialAddress,
                Photo = Photo,
                IdPhoto = PhotoIdProof,
                IdNumber = PhotoId,
                IssuingAuthority = IssuingAuthority,
                Tele = Telephone,
                Mobile = MobileNumber,
                MobileAlt = MobileNumberAlt,
                Email = EmailId,
                PostPGExperience = PGExperience
            )
        except:
            crosCheck = None
        if crosCheck:
            messages.warning(request, 'Already  Exist')
            return HttpResponseRedirect('faculty')
        else:
            print('you can add')
            facultyTable = Faculty(
                FacultyName = FacultyName,
                FacultyDepartment = FDepartment,
                Designation = Designation,
                DateOfBirth = DateOfBirth,
                PanNumber = PanNumber,
                FacultyEligibility = FacultyEligibility,
                PresentResidential = PresentResidentialAddress,
                PermenentResidential = PermenentResidentialAddress,
                Photo = Photo,
                IdPhoto = PhotoIdProof,
                IdNumber = PhotoId,
                IssuingAuthority = IssuingAuthority,
                Tele = Telephone,
                Mobile = MobileNumber,
                MobileAlt = MobileNumberAlt,
                Email = EmailId,
                PostPGExperience = PGExperience
            )
            facultyTable.save()
            obj = Faculty.objects.latest('id')
            for i in range(len(count)):
                ProfessionalQualificationTable = ProfessionalQualification(
                    CourseName = CourseName[i],
                    SpecializationArea = SpecializationArea[i],
                    YearOfPassing = YearOfPassing[i],
                    NameOfCollege = NameOfCollege[i],
                    QualificationRegNo = QualificationRegNo[i],
                    MedicalCouncilName = MedicalCouncilName[i],
                    RegistrationValidUpto = RegistrationValidUpto[i],
                    Document = Document[i],
                    PersonOfQualification = obj
                )
                ProfessionalQualificationTable.save()

            PeriodOfEmployment = request.POST.getlist('PeriodOfEmployment[]')
            From = request.POST.getlist('From[]')
            To = request.POST.getlist('To[]')
            Designation = request.POST.getlist('Designation[]')
            Hospital = request.POST.getlist('Hospital[]')
            Department = request.POST.getlist('Department[]')
            EmploymentStatus = request.POST.getlist('EmploymentStatus[]')
            HoursSpent = request.POST.getlist('HoursSpent[]')
            associated = request.POST.getlist('associated[]')
            for i in range(len(PeriodOfEmployment)):
                ExperienceTable = Experience(
                        
                    PeriodOfEmployment = PeriodOfEmployment[i],
                    From_PeriodOfEmployment = From[i],
                    To_PeriodOfEmployment = To[i],
                    DesignationHeld = Designation[i],
                    HospitalInstitutionCityState = Hospital[i],
                    Department = Department[i],
                    EmploymentStatus = EmploymentStatus[i],
                    HoursSpentPerDay = HoursSpent[i],
                    WhetherAssociatedDNB_FND = associated[i],
                    PersonOfExperience = obj
                )
                ExperienceTable.save()
                
            messages.success(request, 'New Faculty added')
            return HttpResponseRedirect('faculty')
    return HttpResponseRedirect('faculty')
#view faculty
def view_faculty(request,pk):
    Permission = hasPermission(request,'add faculty').PermissionStatus()
    if Permission:
        container = loginPerson(request)
        FacultyDetails = Faculty.objects.get(id=pk)
        Qualification = ProfessionalQualification.objects.filter(PersonOfQualification=pk)
        Exp = Experience.objects.all().filter(PersonOfExperience=pk)
        container['Faculty'] = FacultyDetails
        container['Qualification'] = Qualification
        container['Experience'] = Exp
        return render(request,'view_faculty.html',container)
    else:
        messages.warning(request, "You are not allowed to access")
        return HttpResponseRedirect('faculty')
#edit faculty
def EditFaculty(request,pk):
    print("edit of",pk)
    Permission = hasPermission(request,'edit faculty').PermissionStatus()
    if Permission:
        container = loginPerson(request)
        FacultyDetails = Faculty.objects.get(id=pk)
        Qualification = ProfessionalQualification.objects.filter(PersonOfQualification=pk)
        Exp = Experience.objects.all().filter(PersonOfExperience=pk)
        departmets = department.objects.all()
        Course = course.objects.all()
        container['dep'] = departmets
        container['course'] = Course
        container['Faculty'] = FacultyDetails
        container['Qualification'] = Qualification
        container['Experience'] = Exp
        return render(request,'Edit_faculty.html',container)
    else:
        messages.warning(request, "You are not allowed to access")
        return HttpResponseRedirect('faculty')
def updateFaculty(request,pk):
    if request.method=='POST':
        FacultyName = request.POST['FacultyName']
        FacultyDepartment = request.POST['FacultyDepartment']
        Designation = request.POST['Designation']
        DateOfBirth = request.POST['DateOfBirth']
        PanNumber = request.POST['PanNumber']
        Photo = request.FILES['Photo']
        FacultyEligibility = request.POST['FacultyEligibility']
        PresentResidentialAddress = request.POST['PresentResidentialAddress']
        PermenentResidentialAddress = request.POST['PermenentResidentialAddress']
        PhotoIdProof = request.FILES['Photo1']
        PhotoId = request.POST['PhotoId']
        IssuingAuthority = request.POST['IssuingAuthority']
        Telephone = request.POST['Telephone']
        MobileNumber = request.POST['MobileNumber']
        MobileNumberAlt = request.POST['MobileNumberAlt']
        EmailId = request.POST['EmailId']
        PGExperience = request.POST['PGExperience']
        FDepartment = department.objects.get(id = FacultyDepartment)
        Faculty.objects.filter(id=pk).update(
            FacultyName = FacultyName,
            FacultyDepartment = FDepartment,
            Designation = Designation,
            DateOfBirth = DateOfBirth,
            PanNumber = PanNumber,
            FacultyEligibility = FacultyEligibility,
            PresentResidential = PresentResidentialAddress,
            PermenentResidential = PermenentResidentialAddress,
            Photo = Photo,
            IdPhoto = PhotoIdProof,
            IdNumber = PhotoId,
            IssuingAuthority = IssuingAuthority,
            Tele = Telephone,
            Mobile = MobileNumber,
            MobileAlt = MobileNumberAlt,
            Email = EmailId,
            PostPGExperience = PGExperience
        )    
    return HttpResponseRedirect('faculty')
# add qualification
def addQalification(request,pk):
    Permission = hasPermission(request,'add qualification').PermissionStatus()
    if Permission:   
        container = loginPerson(request)
        Course = course.objects.all()
        container['course'] = Course
        container['personid'] = pk
        return render(request,'addQalification.html',container)
    else:
        messages.warning(request, "You are not allowed to access")
        return redirect('EditFaculty',pk=pk)
def QualiAddition(request,pk):
    if request.method=='POST':
        CourseName=request.POST.getlist('CourseName[]')
        SpecializationArea=request.POST.getlist('SpecializationArea[]')
        YearOfPassing = request.POST.getlist('YearOfPassing[]')
        NameOfCollege = request.POST.getlist('NameOfCollege[]')
        QualificationRegNo = request.POST.getlist('QualificationRegNo[]')
        MedicalCouncilName = request.POST.getlist('MedicalCouncilName[]')
        RegistrationValidUpto = request.POST.getlist('RegistrationValidUpto[]')
        Document = request.FILES.getlist('Document[]')
        count = request.POST.getlist('count[]')
        person = Faculty.objects.get(id=pk)
        for i in range(len(count)):
            ProfessionalQualificationTable = ProfessionalQualification(
                CourseName = CourseName[i],
                SpecializationArea = SpecializationArea[i],
                YearOfPassing = YearOfPassing[i],
                NameOfCollege = NameOfCollege[i],
                QualificationRegNo = QualificationRegNo[i],
                MedicalCouncilName = MedicalCouncilName[i],
                RegistrationValidUpto = RegistrationValidUpto[i],
                Document = Document[i],
                PersonOfQualification = person
            )
            ProfessionalQualificationTable.save()
        messages.success(request, 'New Qualification Added')
    return HttpResponseRedirect('faculty')
#delete qualification
def deleteQua(request,pk):
    pid = ProfessionalQualification.objects.get(id=pk).PersonOfQualification.id
    Permission = hasPermission(request,'delete qualification').PermissionStatus()
    if Permission: 
        data = ProfessionalQualification.objects.get(id=pk)
        container = {'data':data}
        return render(request,'deleteConfo.html',container)
    else:
        messages.warning(request, "You are not allowed to access")
        return redirect('EditFaculty',pk=pid)        
def delete(request):
    if request.method == 'POST':
        deleteId = request.POST['d_id']
        delData=ProfessionalQualification.objects.get(id=deleteId)
        msg = '{} Removed'.format(delData)
        delData.delete()
        messages.success(request, msg)
    return HttpResponseRedirect('faculty')
#delete experience
def deleteExp(request,pk):
    pid = Experience.objects.get(id=pk).PersonOfExperience.id
    Permission = hasPermission(request,'delete qualification').PermissionStatus()
    if Permission: 
        data = Experience.objects.get(id=pk)
        container = {'data':data}
        return render(request,'deleteConfo1.html',container)
    else:
        messages.warning(request, "You are not allowed to access")
        return redirect('EditFaculty',pk=pid)         
def deleteE(request):
    if request.method == 'POST':
        deleteId = request.POST['d_id']
        delData=Experience.objects.get(id=deleteId)
        msg = '{} period of Experience Removed'.format(delData)
        delData.delete()
        messages.success(request, msg)
    return HttpResponseRedirect('faculty')
#add experience
def addExperience(request,pk):
    Permission = hasPermission(request,'add experience').PermissionStatus()
    if Permission: 
        container = loginPerson(request)
        container['personid'] = pk
        return render(request,'addExperience.html',container)
    else:
        messages.warning(request, "You are not allowed to access")
        return redirect('EditFaculty',pk=pk) 
def ExpAddition(request,pk):
    if request.method=='POST':
        person = Faculty.objects.get(id=pk)
        PeriodOfEmployment = request.POST.getlist('PeriodOfEmployment[]')
        From = request.POST.getlist('From[]')
        To = request.POST.getlist('To[]')
        Designation = request.POST.getlist('Designation[]')
        Hospital = request.POST.getlist('Hospital[]')
        Department = request.POST.getlist('Department[]')
        EmploymentStatus = request.POST.getlist('EmploymentStatus[]')
        HoursSpent = request.POST.getlist('HoursSpent[]')
        associated = request.POST.getlist('associated[]')
        for i in range(len(PeriodOfEmployment)):
            ExperienceTable = Experience(
                PeriodOfEmployment = PeriodOfEmployment[i],
                From_PeriodOfEmployment = From[i],
                To_PeriodOfEmployment = To[i],
                DesignationHeld = Designation[i],
                HospitalInstitutionCityState = Hospital[i],
                Department = Department[i],
                EmploymentStatus = EmploymentStatus[i],
                HoursSpentPerDay = HoursSpent[i],
                WhetherAssociatedDNB_FND = associated[i],
                PersonOfExperience = person
            )
            ExperienceTable.save()
        messages.success(request, 'New Experience Added')
    return HttpResponseRedirect('faculty')
def filterfaculty(request):
    container = loginPerson(request)
    departments = department.objects.all()
    container['dep'] = departments   
    if request.method == 'POST':
        filterByName = request.POST['filterByName']
        FilterByDep = request.POST['FilterByDep']
        filterByPhone = request.POST['filterByPhone']
        if filterByName:
            FilteredFac = Faculty.objects.filter(Q(FacultyName__icontains=filterByName))
            container['Faculty'] = FilteredFac
        if FilterByDep:
            container['Faculty'] = Faculty.objects.filter(FacultyDepartment=FilterByDep)
        if filterByPhone:
            container['Faculty'] = Faculty.objects.filter(Mobile=filterByPhone)
        if not filterByName and not FilterByDep and not filterByPhone:
            container['Faculty'] = Faculty.objects.all()
    return render(request,'faculty.html',container)
#delete faculty
def facultyDelete(request,pk):
    Permission = hasPermission(request,'edit faculty').PermissionStatus()
    if Permission:
        data = Faculty.objects.get(id=pk)
        container = {'data':data}
        return render(request,'deleteFac.html',container)
    else:
        messages.warning(request, "You are not allowed to access")
        return HttpResponseRedirect('faculty')       
def deleteFac(request):
    deleteId = request.POST['d_id']
    delData = Faculty.objects.get(id=deleteId)
    ExpDelData = Experience.objects.all().filter(PersonOfExperience=delData)
    QaliDelData = ProfessionalQualification.objects.all().filter(PersonOfQualification=delData)
    msg = '{} Deleted'.format(delData.FacultyName)
    QaliDelData.delete()
    ExpDelData.delete()
    delData.delete()
    messages.success(request, msg)
    return HttpResponseRedirect('faculty')