from django.conf.urls import url
from main.views import (IndexView, LibraryView, BookListOrAddView,
                        AuthorListOrAddView, BookDetailOrUpdateView,
                        AuthorDetailOrUpdateView)

urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'^library/$', LibraryView.as_view()),
    url(r'^book/', BookListOrAddView.as_view()),
    url(r'^author/', AuthorListOrAddView.as_view()),
    url(r'^book/(?P<code>[A-Za-z0-9\-_:]+)/$', BookDetailOrUpdateView.as_view()),
    url(r'^author/(?P<code>[A-Za-z0-9\-_:]+)/$', AuthorDetailOrUpdateView.as_view()),
]