from django.conf.urls import url
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    url(r'^api/institutions/$', views.InstitutionList.as_view()),
    url(r'^api/institutions/(?P<pk>[0-9]+)$', views.InstitutionDetail.as_view()),
    url(r'^api/dicom_images/$', views.DicomImageList.as_view()),
    url(r'^api/dicom_images/(?P<pk>[0-9]+)', views.DicomImageDetail.as_view()),
    url(r'^api/users/$', views.UserList.as_view()),
    url(r'^api/users/(?P<pk>[0-9]+)$', views.UserDetail.as_view())
]
