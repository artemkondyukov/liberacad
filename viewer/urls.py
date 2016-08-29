from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^api/institutions/$', views.InstitutionList.as_view()),
    url(r'^api/institutions/(?P<pk>[0-9]+)$', views.InstitutionDetail.as_view()),
    url(r'^api/dicom_images/$', views.DicomImageList.as_view())
]
