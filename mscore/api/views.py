from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from mscore.api.serializers import *


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'spaces': reverse('space-list-api', request=request, format=format),
    })


class SpaceList(generics.ListCreateAPIView):
    serializer_class = SpaceSerializer
    model = Space

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Space.objects.filter(owner=self.request.user)


class SpaceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SpaceSerializer
    model = Space

    def get_queryset(self):
        return Space.objects.filter(owner=self.request.user)
