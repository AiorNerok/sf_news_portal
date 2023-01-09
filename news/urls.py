from django.urls import path

from .views import NewsList, DetailNews, SearchList

urlpatterns = [
    path("", NewsList.as_view()),
    path("<int:pk>", DetailNews.as_view()),
    path("search/", SearchList.as_view()),
]
