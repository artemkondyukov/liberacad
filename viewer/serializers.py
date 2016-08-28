from django.contrib.auth.models import User, Group
from rest_framework import serializers
from viewer.models import Institution, LANGUAGE_CHOICES, STYLE_CHOICES


class InstitutionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Institution
        fields = ('pk', 'title')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
