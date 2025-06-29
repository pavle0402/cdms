import django_filters
from .models import Patient

#just a few filters, would improve this on a real-world project
class PatientFilter(django_filters.FilterSet):
    gender = django_filters.CharFilter(field_name='gender')
    phone = django_filters.CharFilter(field_name='phone', lookup_expr='icontains')
    full_name = django_filters.CharFilter(field_name='full_name', lookup_expr='icontains')

    class Meta:
        model = Patient
        fields = ['gender', 'phone', 'full_name']