from django.conf.urls import url
from main.views import (IndexView, LoginAPIView, LogoutAPIView, LibraryView,
                        BookListOrAddView, AuthorListOrAddView, BookDetailOrUpdateView,
                        AuthorDetailOrUpdateView, GetTokenView)
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'^login/$', LoginAPIView.as_view()),
    url(r'^logout/$', LogoutAPIView.as_view()),
    url(r'^token/$', GetTokenView.as_view()),
    url(r'^library/$', LibraryView.as_view()),
    url(r'^book/$', BookListOrAddView.as_view()),
    url(r'^author/$', AuthorListOrAddView.as_view()),
    url(r'^book/(?P<pk>[0-9]+)/$', BookDetailOrUpdateView.as_view()),
    url(r'^author/(?P<pk>[0-9]+)/$', AuthorDetailOrUpdateView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
