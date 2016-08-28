from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from viewer.serializers import UserSerializer, GroupSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from viewer.models import Institution
from viewer.serializers import InstitutionSerializer


@csrf_exempt
def institution_list(request):
    """
    List all institutions, or create a new one.
    """
    if request.method == 'GET':
        snippets = Institution.objects.all()
        serializer = InstitutionSerializer(snippets, many=True)
        renderer = JSONRenderer()
        return HttpResponse(renderer.render(serializer.data))

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = InstitutionSerializer(data=data)
        renderer = JSONRenderer()
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(renderer.render(serializer.data), status=201)
        return HttpResponse(renderer.render(serializer.errors), status=400)


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


# Create your views here.
def index(request):
    return HttpResponse("FUCK YOU!")
