from django.conf.urls import include, url, patterns
# from django.contrib import admin
from rest_framework.authtoken import views as view
from . import views
from django.contrib.auth.views import password_reset,login,logout,password_change,password_change_done,password_reset_complete,password_reset_confirm,password_reset_done

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^reset_password', views.form, name="reset_password"),
]
# urlpatterns +=[
#     url(r'^login/$', login, name='login'),
#     url(r'^logout/$', logout, name='logout'),
#     url(r'^password_change/$', password_change, name='password_change'),
#     url(r'^password_change/done/$', password_change_done, name='password_change_done'),
#     url(r'^password_reset/$', password_reset, name='password_reset'),
#     url(r'^password_reset/done/$', password_reset_done, name='password_reset_done'),
#     url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
#         password_reset_confirm, name='password_reset_confirm'),
#     url(r'^reset/done/$',password_reset_complete, name='password_reset_complete'),
#     # url(r'^reset/confirm/$',
#     #          'django.contrib.auth.views.password_reset_confirm'),
# ]

urlpatterns += [
    url(r'^api-token-auth/', view.obtain_auth_token)
]