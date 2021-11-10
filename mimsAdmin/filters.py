import django_filters
from .models import *

class DepartmentFilter(django_filters.FilterSet):
    class Meta:
        model = department
        fields = ['Department_name','Department_Head']