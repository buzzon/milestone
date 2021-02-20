from rest_framework import serializers
from mscore.models import *


class SpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component