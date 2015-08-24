from django.conf.urls import include, url
# from django.contrib import admin
from rest_framework.authtoken import views as view
from . import views
from django.contrib.auth.views import password_reset,login,logout

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^polls/', include('polls.urls', namespace="polls")),
     url(r'^account/reset_password', views.ResetPasswordRequestView.as_view(), name="reset_password"),

]

urlpatterns += [
    url(r'^api-token-auth/', view.obtain_auth_token)
]