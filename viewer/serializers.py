from django.contrib.auth.models import User, Group
from rest_framework import serializers
from viewer.models import Institution, DicomImage, Contour


class InstitutionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Institution
        fields = ('pk', 'title')


class ContourSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contour
        fields = ('pk', 'contourFile', 'maskFile', 'dicomImage', 'by')


class DicomImageSerializer(serializers.HyperlinkedModelSerializer):
    contourFiles = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    source = InstitutionSerializer(required=False, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username', read_only=True)

    class Meta:
        model = DicomImage
        fields = ('pk', 'source', 'owner', 'file', 'acquisitionDate', 'contourFiles')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    dicomImages = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'groups', 'dicomImages')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name', )
