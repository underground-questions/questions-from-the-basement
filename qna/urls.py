from django.conf.urls import urls
from . import views

urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^questions/(?P<pk>[0-9]+)$', views.question_detail, name="question_detail"),
    url(r'^profile/(?P<pk>[0-9]+)$', views.profile, name="proflie"),
]
