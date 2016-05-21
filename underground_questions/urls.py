from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from qna import views

router = routers.DefaultRouter()
router.register(r'questions', views.QuestionsViewSet)
router.register(r'answers', views.AnswersViewSet)
router.register(r'owners', views.OwnersViewSet)
router.register(r'tags', views.TagsViewSet)
router.register(r'users', views.UsersViewSet)

urlpatterns = [
    url(r'^', include('qna.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^register/', views.register, name='register'),
    url(r'^user_redirect/', views.user_redirect, name='user_redirect'),
]
