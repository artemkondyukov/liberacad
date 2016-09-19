from django.contrib.auth.models import User, Group, AnonymousUser
from django.conf import settings
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status

import dicom
import numpy as np
import os
# from png import Image
import png
from wsgiref.util import FileWrapper

from viewer.models import Institution
from viewer.serializers import InstitutionSerializer, DicomImageSerializer
from viewer.models import DicomImage
from viewer.serializers import UserSerializer, GroupSerializer


class InstitutionList(generics.ListCreateAPIView):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


class InstitutionDetail(generics.RetrieveUpdateAPIView):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


class DicomImageList(generics.ListCreateAPIView):
    queryset = DicomImage.objects.select_related("owner")
    serializer_class = DicomImageSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, **kwargs):
        # Note the use of `get_queryset()` instead of `self.queryset`
        if self.request.user == AnonymousUser:
            return Response(None, status=status.HTTP_403_FORBIDDEN)
        queryset = self.get_queryset()
        serializer = DicomImageSerializer(queryset.filter(owner=self.request.user), many=True)
        return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     print(123)
    #     return Response(None, status=status.HTTP_301_MOVED_PERMANENTLY)

    def perform_create(self, serializer):
        print(self.request.data)
        serializer.save(owner=self.request.user)


class DicomImageDetail(generics.RetrieveAPIView):
    queryset = DicomImage.objects.all()
    serializer_class = DicomImageSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class DicomImageRepresentation(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, **kwargs):
        print(request, kwargs)
        dicomImages = DicomImage.objects.filter(pk=kwargs["pk"])
        if len(dicomImages) > 1:
            print("There are several instances for pk=", kwargs["pk"])
            return Response(None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif len(dicomImages) == 0:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        pixel_array = dicom.read_file(os.path.join(settings.VIEWER_MEDIA_ROOT, str(dicomImages[0].file)))\
            .pixel_array
        print(pixel_array.min(), pixel_array.max())
        # image = Image.fromarray(pixel_array)
        image = png.from_array(pixel_array, 'L;16')
        response = HttpResponse(content_type="image/png")
        image.save(response)
        return response


class DicomImageViewer(APIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'rest_framework/viewer.html'

    def get(self, request, **kwargs):
        dicom_images = DicomImage.objects.filter(owner=request.user)
        pk = kwargs.get("pk", None)
        return Response({'dicomImages': dicom_images, 'pk': pk})
