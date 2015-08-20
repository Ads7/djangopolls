from django.conf.urls import include, url
# from django.contrib import admin
from rest_framework.authtoken import views

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^polls/', include('polls.urls', namespace="polls")),
]

# urlpatterns += [
#     url(r'^api-token-auth/', views.obtain_auth_token)
# ]