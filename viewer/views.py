from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from viewer.serializers import UserSerializer, GroupSerializer
from rest_framework import generics

from viewer.models import Institution
from viewer.serializers import InstitutionSerializer, DicomImageSerializer
from viewer.models import DicomImage


class InstitutionList(generics.ListCreateAPIView):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


class InstitutionDetail(generics.RetrieveUpdateAPIView):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


class DicomImageList(generics.ListCreateAPIView):
    queryset = DicomImage.objects.all()
    serializer_class = DicomImageSerializer


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
