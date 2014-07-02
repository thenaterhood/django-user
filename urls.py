from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

  url(r'^register/$',        'user.views.register_user'),
  url(r'^login/$',             'user.views.login_user'),
  url(r'^auth/$',             'user.views.auth_user'),
  url(r'^welcome/$',      'user.views.welcome'),
  url(r'^logout/$',          'user.views.logout'),
  url(r'^edit/$',              'user.views.edit_profile'),
  url(r'^password/$',    'user.views.change_password'),
  url(r'^settings/$',       'user.views.settings_dashboard'),

  url(r'^profile/(?P<username>[a-zA-Z0-9_.-]+)/$',
                                    'user.views.view_profile'),
  url(r'^about/$',        'user.views.about_app'),

)
