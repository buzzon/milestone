from django.db.models import Q
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from mscore.api.serializers import *


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_root(request, format=None):
    return Response({
        'spaces': reverse('space-list-api', request=request, format=format),
    })


@permission_classes([IsAuthenticated])
class SpaceList(generics.ListCreateAPIView):
    serializer_class = SpaceSerializer
    model = Space

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        owned_spaces = Space.objects.filter(owner=self.request.user)
        membered_spaces = Space.objects.filter(members=self.request.user)
        return (membered_spaces | owned_spaces).distinct()


@permission_classes([IsAuthenticated])
class SpaceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SpaceSerializer
    model = Space

    def get_queryset(self):
        owned_spaces = Space.objects.filter(owner=self.request.user)
        membered_spaces = Space.objects.filter(members=self.request.user)
        return (membered_spaces | owned_spaces).distinct()


@permission_classes([IsAuthenticated])
class TaskList(generics.ListAPIView):
    serializer_class = TaskSerializer
    model = Task

    def get_queryset(self):
        return Task.objects.filter(space=self.request.GET['space'])


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_time_period(request):
    if request.method == 'GET':
        # tasks = Task.objects.filter(space=request.GET['space']).filter(initial_date__range=["2021-04-01", "2021-06-01"])
        tasks = Task.objects.filter(space=request.GET['space']).filter(initial_date__range=["2021-05-01", "2021-06-01"])
        return Response({'tasks': TaskSerializer(tasks, many=True).data})

