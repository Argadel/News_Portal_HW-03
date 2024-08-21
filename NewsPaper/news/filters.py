from django_filters import FilterSet, DateTimeFilter, CharFilter
from django.forms import DateTimeInput
from .models import Post


class PostFilter(FilterSet):

    added_after = DateTimeFilter(
        field_name='date',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Post

        fields = {

            'title': ['icontains'],
            'category': ['exact'],

        }
