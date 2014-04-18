from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from onedir import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^request/', 'handle_requests.views.derp'),
    url(r'^onedir/', include('onedir.urls')),
    url(r'^register/$', views.register, name='register'), # ADD NEW PATTERN!
    url(r'^login/$', views.user_login, name='login'),
    url(r'^files_for_user/$', views.files_for_user, name='files_for_user'),
)
if settings.DEBUG:
        urlpatterns += patterns(
                'django.views.static',
                (r'media/(?P<path>.*)',
                'serve',
                {'document_root': settings.MEDIA_ROOT}), )
