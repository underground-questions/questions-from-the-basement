from django.conf.urls import include, url
from django.contrib import admin
from qna import views

urlpatterns = [
    url(r'^', include('qna.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^register/', views.register, name='register')
]
