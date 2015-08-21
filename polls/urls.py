from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.conf.urls import include

urlpatterns = [
    # # ex: /polls/
    # url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /polls/5/
    url(r'^questions/$', views.QuestionView.as_view(), name='question'),
    url(r'^questions/(?P<question_id>[0-9]+)/$', views.QuestionDetailView.as_view()),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    # ex: /polls/5/results/
    url(r'^photo/(?P<question_id>[0-9]+)/$', views.FileUploadView.as_view()),

]
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
urlpatterns = format_suffix_patterns(urlpatterns)
