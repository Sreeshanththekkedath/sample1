from django.db import models
import os

# Create your models here.

class Holidays(models.Model):
    Holiday_name = models.CharField(max_length=100)
    Holiday_date = models.CharField(max_length=100)
    Holiday_status = models.CharField(max_length=100)

    class Meta:
        db_table = 'Holidays'
    
    def __str__(self):
        return self.Holiday_status


class SuperAdmin(models.Model):
    username = models.CharField(max_length=100) 
    password = models.CharField(max_length=100) 

    class Meta:
        db_table = 'SuperAdmin'

class departmentHead(models.Model):
    DepHead_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'departmentHead'
    def __str__(self):
        return self.DepHead_name

# class LogBook(models.Model):
#     LogBook = models.CharField(max_length=100)

#     class Meta:
#         db_table = 'LogBook'
#     def __str__(self):
#         return self.LogBook

    
class department(models.Model):
    Department_name = models.CharField(max_length=100) 
    Department_Head = models.ForeignKey(departmentHead, on_delete=models.CASCADE)
    CourseDuration = models.IntegerField() 
    programName = models.CharField(max_length=100) 
    log_book = models.CharField(max_length=100) 
    AccreditationRenewalDate = models.DateField()
    FirstYearStipend = models.CharField(max_length=100) 
    SecondYearStipend = models.CharField(max_length=100) 
    ThirdYearStipend = models.CharField(max_length=100) 
    FourYearStipend = models.CharField(max_length=100,blank=True,default='N/A') 
    FiveYearStipend = models.CharField(max_length=100,blank=True,default='N/A') 
    SixYearStipend = models.CharField(max_length=100,blank=True,default='N/A')
    dep_status = models.CharField(max_length=100,default='active' )

    class Meta:
        db_table = 'department'
    
    def __str__(self):
        return self.Department_name

class course(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'course'
    def __str__(self):
        return self.name

class Faculty(models.Model):
    FacultyName = models.CharField(max_length=100)
    FacultyDepartment = models.ForeignKey(department,on_delete=models.CASCADE)
    Designation = models.CharField(max_length=100)
    DateOfBirth = models.DateField()
    PanNumber = models.CharField(max_length=100)
    FacultyEligibility = models.CharField(max_length=500)
    PresentResidential = models.CharField(max_length=500)
    PermenentResidential = models.CharField(max_length=500)
    Photo = models.ImageField(upload_to='Faculty_img')

    IdPhoto = models.ImageField(upload_to='Faculty_img')
    IdNumber = models.CharField(max_length=100)
    IssuingAuthority = models.CharField(max_length=100)

    Tele = models.CharField(max_length=100)
    Mobile = models.CharField(max_length=100)
    MobileAlt = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    PostPGExperience = models.IntegerField() 
    class Meta:
        db_table='Faculty'



    
class ProfessionalQualification(models.Model):
    CourseName = models.CharField(max_length=100)
    SpecializationArea = models.CharField(max_length=100)
    YearOfPassing = models.CharField(max_length=100)
    NameOfCollege = models.CharField(max_length=100)
    QualificationRegNo = models.CharField(max_length=100)
    MedicalCouncilName = models.CharField(max_length=100)
    RegistrationValidUpto = models.CharField(max_length=100)
    Document = models.FileField(upload_to='Documents/ProfessionalQualification')
    PersonOfQualification = models.ForeignKey(Faculty,on_delete=models.CASCADE)
    class Meta:
        db_table = 'ProfessionalQualification'
        
    def __str__(self):
        return self.CourseName

class Experience(models.Model):
    
    PeriodOfEmployment = models.CharField(max_length=100)
    From_PeriodOfEmployment = models.DateField()
    To_PeriodOfEmployment = models.DateField()
    DesignationHeld =models.CharField(max_length=100)
    HospitalInstitutionCityState = models.CharField(max_length=100)
    Department = models.CharField(max_length=100)
    EmploymentStatus = models.CharField(max_length=100)
    HoursSpentPerDay = models.IntegerField()
    WhetherAssociatedDNB_FND = models.CharField(max_length=100)
    PersonOfExperience = models.ForeignKey(Faculty,on_delete=models.CASCADE)
    class Meta:
        db_table = 'Experience'

    def __str__(self):
        return self.DesignationHeld


class Role(models.Model):
    roleName = models.CharField(max_length=100)
    roleStatus = models.CharField(max_length=100)
    class Meta:
        db_table = 'Role'

    def __str__(self):
        return self.roleName


class ParentPath(models.Model):
    ParentPath = models.CharField(max_length=100,unique=True)
    class Meta:
        db_table = 'Parent'

    def __str__(self):
        return self.ParentPath
    
class Path(models.Model):
    pathName = models.CharField(max_length=100,blank=True)
    parent = models.ForeignKey(ParentPath,on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    Path = models.CharField(max_length=100,blank=True)
    SortOrder = models.IntegerField(blank=True)
    class Meta:
        db_table = 'Path'
    def __str__(self):
        return self.pathName


class Permissions(models.Model):
    PermissionOfRole = models.ForeignKey(Role,on_delete=models.CASCADE)
    PathForPermission = models.ForeignKey(Path,on_delete=models.CASCADE)
    class Meta:
        db_table = 'Permissions'
        unique_together = [['PermissionOfRole','PathForPermission']]


class UserTable(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    PSWD = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    userRole = models.ForeignKey(Role,on_delete=models.CASCADE)
    userDepartMent = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    class Meta:
        db_table = 'UserTable'

    def __str__(self):
        return self.name

class ConferenceOrganizerTable(models.Model):
    choices = (
        ('active','Activate'),
        ('inactive','Inactivate')
    )
    Organizezr_Name = models.CharField(max_length=100)
    Organizezr_status = models.CharField(max_length=100,choices=choices)
    class Meta:
        db_table = 'ConferenceOrganizerTable'


class BooksTable(models.Model):
    Books_Name = models.CharField(max_length=100)
    Department = models.ManyToManyField(
        department,  
        verbose_name="list of department",
    )
    Auther_Name = models.CharField(max_length=100)
    Books_availability = models.IntegerField()
    Books_Edition = models.CharField(max_length=100)
    Short_Summary = models.TextField()
    Books_status = models.CharField(max_length=100,default='active')
    class Meta:
        db_table = 'BooksTable'
        unique_together = [['Books_Name','Auther_Name','Books_Edition']]

class tableHeads(models.Model):
    heads = models.CharField(max_length=100)
    class Meta:
        db_table="tableHeads"
    def __str__(self):
        return self.heads

class LogMasterTable(models.Model):
    choices = (
        ('active','Activate'),
        ('inactive','Inactivate')
    )
    Name = models.CharField(max_length=100)
    status = models.CharField(max_length=100,choices=choices,default='active')
    TableHeads = models.ManyToManyField(
        tableHeads,  
        verbose_name="Table Heads",
    )
    class Meta:
        db_table = "LogMasterTable"

class PublicationTable(models.Model):
    Publication_Title = models.CharField(max_length=100)
    Volume = models.IntegerField()
    Publication_Author = models.CharField(max_length=100)
    issue = models.CharField(max_length=100)
    Publisher_name =models.CharField(max_length=100)
    Website_Id = models.CharField(max_length=100)
    Journal = models.CharField(max_length=100)
    Date = models.DateField(auto_now_add=False,auto_now=False)
    choices = (
        ('active','Activate'),
        ('inactive','Inactivate')
    )
    status = models.CharField(max_length=100,default='active',choices=choices)
    class Meta:
        db_table = 'PublicationTable'
        unique_together = ['Publication_Title','Volume','Publication_Author']
    def __str__(self):
        return self.Publication_Title

class JournalsTable(models.Model):
    Journal_name=models.CharField(max_length=100)
    Edition = models.CharField(max_length=100)
    Journal_department = models.ManyToManyField(
        department,  
        verbose_name="Department",
    )
    Published_Date = models.DateField()
    Publisher_name = models.CharField(max_length=100)
    choices=(
        ('National','National'),
        ('International','International')
    )
    Journal_Type = models.CharField(max_length=100,choices=choices)
    Short_Summary = models.TextField()
    status = models.CharField(
        max_length=100,
        choices=(
            ('active','Activate'),
            ('inactive','Inactivate')
        )
    )
    class Meta:
        db_table="Journals"
        unique_together = ['Journal_name','Edition','Published_Date']

class FormTable(models.Model):
    Form_name = models.CharField(max_length=100)
    Form = models.FileField(upload_to='Documents/form')
    status = models.CharField(
        max_length=100,
        choices=(
            ('active','Activate'),
            ('inactive','Inactivate')
        ),
        default='active'
    )
    class Meta:
        db_table='form'
    def filename(self):
        return os.path.basename(self.Form.name)

class NotificationTable(models.Model):
    Notification_Title = models.CharField(max_length=100)
    Department = models.ManyToManyField(department,verbose_name="Departments")
    Added_By = models.ForeignKey(UserTable,on_delete=models.CASCADE)
    Details = models.TextField()
    Date = models.DateField()
    status = models.CharField(
        max_length=100,
        choices=(
            ('active','Activate'),
            ('inactive','Inactivate')
        ),
        default='active'
    )
    class Meta:
        db_table='Notifications'

class BatchTable(models.Model):
    Batch_Name = models.CharField(max_length=100)
    Department = models.ForeignKey(department,on_delete=models.CASCADE)
    From_Date = models.DateField()
    Date_To = models.DateField()
    Batch_Status = models.CharField(
        max_length=100,
        choices=(
            ('active','Activate'),
            ('inactive','Inactivate')
        ),
        default='active',
    )
    class Meta:
        db_table = 'Batch'