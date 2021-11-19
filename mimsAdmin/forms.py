from django import forms
from django.forms import ModelForm, Textarea
from .models import *
from django.forms.widgets import CheckboxSelectMultiple

class DateInput(forms.DateInput):
    input_type = 'date'

class CountryForm(forms.Form):
    OPTIONS = (
        ("AUT", "Austria"),
        ("DEU", "Germany"),
        ("NLD", "Neitherlands"),
    )
    Countries = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS)

# class ProQualificationForm(ModelForm):
#     class Meta:
#         model = ProfessionalQualification
#         fields = [
#             'CourseName',
#             'SpecializationArea',
#             'YearOfPassing',
#             'QualificationRegNo',
#             'MedicalCouncilName',
#             'RegistrationValidUpto',
#             'Document'
#         ]

class RoleForm(ModelForm):
     class Meta:
         model = Role
         fields = ['roleName','roleStatus']

class OrganizerForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrganizerForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = ConferenceOrganizerTable
        fields = ("__all__")

class BooksForm(ModelForm):
    # content = forms.CharField(widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super(BooksForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
    class Meta:
        model = BooksTable
        widgets = {
            'Short_Summary': Textarea(attrs={'cols': 5, 'rows':4}),
        }
        fields = ['Books_Name','Auther_Name','Books_availability','Books_Edition','Department','Short_Summary']


class LogMasterForm(ModelForm):
    # TableHeads = forms.ModelMultipleChoiceField(
    #     queryset=tableHeads.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=True)

    def __init__(self, *args, **kwargs):
        super(LogMasterForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
            
        self.fields["TableHeads"].widget = CheckboxSelectMultiple()
        self.fields["TableHeads"].queryset = tableHeads.objects.all()
    class Meta:
        model = LogMasterTable
        fields = ['Name','TableHeads','status']

class PublicationForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(PublicationForm,self).__init__(*args, **kwargs)
        self.fields["Date"].widget = DateInput()
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class':'form-control',
            })
        
    class Meta:
        model = PublicationTable
        fields = ("__all__")

class JournalsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(JournalsForm,self).__init__(*args, **kwargs)
        self.fields["Published_Date"].widget = DateInput()
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class':'form-control',
            })
    class Meta:
        model = JournalsTable
        fields = ("__all__")
        widgets = {
            'Short_Summary': Textarea(attrs={'cols': 5, 'rows':4}),
        }

class formMasterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(formMasterForm,self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class':'form-control',
            })
        self.fields["Form"].widget.attrs.update({
            'id':'val',
            'onChange':'validate(this.value)',
        })
    class Meta:
        model = FormTable
        fields = ("__all__")

class NotificationForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(NotificationForm,self).__init__(*args, **kwargs)
        self.fields["Date"].widget = DateInput()
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class':'form-control',
            })
        
    class Meta:
        model = NotificationTable
        fields = ("__all__") 
        widgets = {
            'Details': Textarea(attrs={'cols': 5, 'rows':4}),
        }

class BatchForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BatchForm,self).__init__(*args, **kwargs)
        self.fields['From_Date'].widget = DateInput()
        self.fields['Date_To'].widget = DateInput()
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class':'form-control',
            })

    class Meta:
        model = BatchTable
        fields = ("__all__")
