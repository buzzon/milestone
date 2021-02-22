from rest_framework import generics
from mscore.api.serializers import *


class SpaceList(generics.ListCreateAPIView):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SpaceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
