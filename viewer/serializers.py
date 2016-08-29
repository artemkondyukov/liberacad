from django.contrib.auth.models import User, Group
from rest_framework import serializers
from viewer.models import Institution, DicomImage


class InstitutionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Institution
        fields = ('pk', 'title')


class DicomImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DicomImage
        fields = ('pk', 'filename', 'acquisition_date', 'source')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    dicom_images = serializers.PrimaryKeyRelatedField(many=True, queryset=DicomImage.objects.all())

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'dicom_images')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
