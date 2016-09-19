from django.contrib.auth.models import User, Group
from rest_framework import serializers
from viewer.models import Institution, DicomImage, Contour

from datetime import datetime
import dicom


class InstitutionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Institution
        fields = ('pk', 'title')


class ContourSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contour
        fields = ('pk', 'contourFile', 'maskFile', 'dicomImage', 'by')


class DicomImageSerializer(serializers.HyperlinkedModelSerializer):
    # contourFiles = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    source = InstitutionSerializer(required=False, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username', read_only=True)
    acquisitionDate = serializers.DateField(read_only=True)

    def validate(self, data):
        acquisitionDate = datetime.strptime(dicom.read_file(data["file"]).ContentDate, "%Y%m%d").date()
        data["acquisitionDate"] = acquisitionDate
        return data

    class Meta:
        model = DicomImage
        fields = ('pk', 'source', 'owner', 'file', 'acquisitionDate')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    dicomImages = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'groups', 'dicomImages')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name', )
