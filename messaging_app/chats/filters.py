import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="timestamp", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="timestamp", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['conversation', 'start_date', 'end_date']
