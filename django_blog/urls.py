from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # Blog urls
    url(r'', include('blogengine.urls', namespace='blogengine')),

    # Flat pages
    url(r'', include('django.contrib.flatpages.urls')),
)
