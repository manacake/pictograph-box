from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView
from blogengine.models import Post, Category, Tag
from blogengine.views import CategoryListView, TagListView, PostsFeed

urlpatterns = patterns('',
        # Index
        url('^(?P<page>\d+)?/?$', ListView.as_view(model=Post,
                                                   paginate_by=5,
                                                   )),
        # Individual post
        url(r'^(?P<pub_date__year>\d{4})/(?P<pub_date__month>\d{1,2})'
            r'/(?P<slug>[a-zA-Z0-9-]+)/?$', DetailView.as_view(model=Post,
            )),

        # Categories
        url(r'^category/(?P<slug>[a-zA-Z0-9-]+)/?$', CategoryListView.as_view(
            model=Category,
            paginate_by=5,
            )),

        # Tags
        url(r'^tag/(?P<slug>[a-zA-Z0-9-]+)/?$', TagListView.as_view(
            model=Tag,
            paginate_by=5,
            )),

        # post RSS feed
        url(r'^feeds/posts/$', PostsFeed()),
)
