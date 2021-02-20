from rest_framework import serializers
from mscore.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'last_login', 'date_joined',
                  'groups', 'user_permissions',
                  'is_superuser', 'is_staff', 'is_active']


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class SpaceSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Space
        fields = ['id', 'title', 'owner', 'publish_date', 'tasks']
