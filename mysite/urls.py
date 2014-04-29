from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from onedir_app import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^onedir/', include('onedir_app.urls')),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^files_for_user/$', views.files_for_user, name='files_for_user'),
    url(r'^upload/', 'handle_requests.views.upload_handler'),
    url(r'^download/(?P<file>.+)', 'handle_requests.views.download_handler'),
    url(r'^delete/', 'handle_requests.views.delete_handler'),
    url(r'^loginrequest/', 'handle_requests.views.login_handler'),
    url(r'^latestchanges/', 'handle_requests.views.latest_changes'),
    url(r'^add_dir/', 'handle_requests.views.add_dir_handler'),
    url(r'^del_dir/', 'handle_requests.views.del_dir_handler'),
    url(r'^change_pass/', 'handle_requests.views.pass_change_handler'),
)
if settings.DEBUG:
        urlpatterns += patterns(
                'django.views.static',
                (r'media/(?P<path>.*)',
                'serve',
                {'document_root': settings.MEDIA_ROOT}), )
