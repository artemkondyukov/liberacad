from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from viewer.serializers import UserSerializer, GroupSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

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
    queryset = DicomImage.objects.select_related("owner")
    serializer_class = DicomImageSerializer

    def list(self, request, **kwargs):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = DicomImageSerializer(queryset.filter(owner=self.request.user), many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
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


class DicomImageViewer(APIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'rest_framework/viewer.html'

    def get(self, request):
        dicomImages = DicomImage.objects.filter(owner=request.user)
        print(dicomImages[0].file)
        return Response({'dicomImages': dicomImages})
