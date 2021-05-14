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
        return Space.objects.filter(owner=self.request.user)


@permission_classes([IsAuthenticated])
class SpaceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SpaceSerializer
    model = Space

    def get_queryset(self):
        return Space.objects.filter(owner=self.request.user)


@permission_classes([IsAuthenticated])
class TaskList(generics.ListAPIView):
    serializer_class = TaskSerializer
    model = Task

    def get_queryset(self):
        return Task.objects.filter(space=self.request.GET['space'])


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_TimePeriod(request):
#     if request.method == 'POST':
#         user = request.user
#         user.delete()