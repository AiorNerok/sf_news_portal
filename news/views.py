import datetime

from django.views.generic import ListView, DetailView

from .models import Post
from .filters import FilterPost


class NewsList(ListView):
    model = Post
    ordering = "-date"
    template_name = "news.html"
    context_object_name = "news"
    paginate_by = 2


class DetailNews(DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["time"] = datetime.datetime.utcnow()
        return context


class SearchList(ListView):
    model = Post
    ordering = "-date"
    template_name = "news_search.html"
    context_object_name = "news"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = FilterPost(self.request.GET, queryset=self.get_queryset())
        return context
