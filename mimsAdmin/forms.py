from django import forms
from django.forms import ModelForm, Textarea
from .models import *


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