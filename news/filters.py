from django_filters import FilterSet, CharFilter
from .models import Post


class FilterPost(FilterSet):

    class Meta:
        model = Post
        fields = {"date": ["gt"], "title": ["icontains"], "author": ""}
