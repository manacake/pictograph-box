from django.conf.urls import patterns, url
from django.contrib.sitemaps.views import sitemap
from django.views.generic import ListView, DetailView
from blogengine.models import Post, Category, Tag
from blogengine.sitemap import PostSitemap, FlatpageSitemap
from blogengine.views import CategoryListView, TagListView, PostsFeed, CategoryPostsFeed, TagPostsFeed

# Define sitemaps
sitemaps = {
    'posts': PostSitemap,
    'pages': FlatpageSitemap
}

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

        # Category RSS feed
        url(r'^feeds/posts/category/(?P<slug>[a-zA-Z0-9-]+)/?$', CategoryPostsFeed()),

        # Tag RSS feed
        url(r'^feeds/posts/tag/(?P<slug>[a-zA-Z0-9-]+)/?$', TagPostsFeed()),

        # Search posts
        url(r'^search', 'blogengine.views.getSearchResults'),

        # Sitemap
        url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
            name='django.contrib.sitemaps.views.sitemap'),
)