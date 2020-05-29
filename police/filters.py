import django_filters
from citizen.models import User
from django_filters import DateFilter, CharFilter


class OrderFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name='date_created', lookup_expr='gte')
	end_date = DateFilter(field_name='date_created', lookup_expr='lte')
	
	class Meta:
		model = User
		fields = ['uid', 'name', 'phone', 'email', 'state']
		# exclude = ['password', 'last_login', 'is_active', 'is_staff', 'is_admin', ]
		