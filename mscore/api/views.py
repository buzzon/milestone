from rest_framework import generics
from mscore.api.serializers import *


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
