import datetime

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator

from .models import Post
from .filters import FilterPost


class NewsList(ListView):
    model = Post
    ordering = "-date"
    template_name = "news.html"
    context_object_name = "news"
    paginate_by = 2


class SearchList(ListView):
    model = Post
    ordering = "-date"
    template_name = "news_search.html"
    context_object_name = "news"
    paginate_by = 2

    # def get(self, request):
    #     post = Post.objects.order_by("-date")
    #     p = Paginator(post, 1)

    #     post = p.get_page(request.GET.get("page", 1))
    #     data = {
    #         "post": post,
    #     }
    #     return render(request, "news_search.html", data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = FilterPost(self.request.GET, queryset=self.get_queryset())
        return context


class DetailNews(DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["time"] = datetime.datetime.utcnow()
        return context
