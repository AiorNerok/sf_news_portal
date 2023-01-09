from django_filters import FilterSet
from .models import Post


class FilterPost(FilterSet):
    class Meta:
        model = Post
        fields = {
            "date": ["gt"],
            "title": ["icontains"],
        }
