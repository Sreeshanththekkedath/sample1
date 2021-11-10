from django import forms
from django.forms import ModelForm
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