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


class SubTaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Task
        exclude = ['space']

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        exclude = kwargs.pop("exclude", None)
        nest = kwargs.pop("nest", None)

        if nest is not None:
            if nest:
                self.Meta.depth = 1

        super(SubTaskSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
            for field_name in exclude:
                self.fields.pop(field_name)


SubTaskSerializer._declared_fields['task'] = SubTaskSerializer(many=True, required=False)


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    task = SubTaskSerializer(many=True, required=False, nest=True)

    class Meta:
        model = Task
        fields = '__all__'


class SpaceSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    tasks = TaskSerializer(many=True, required=False)

    class Meta:
        model = Space
        fields = ['id', 'title', 'owner', 'publish_date', 'tasks']

    def create(self, validated_data):
        task_data = validated_data.pop('tasks', [])
        space = Space.objects.create(**validated_data)
        for task in task_data:
            Task.objects.create(space=space, **task)
        return space

    def update(self, instance, validated_data):
        tasks_data = validated_data.pop('tasks', [])
        instance.title = validated_data.get('title', instance.title)

        for data in tasks_data:
            task_id = data.get('id', None)
            if task_id is None:
                Task.objects.create(space=instance, **data)
            else:
                task, created = Task.objects.get_or_create(id=task_id, space=instance)
                task.title = data.get('title', task.title)
                task.description = data.get('description', task.description)
                task.save()

        instance.save()
        return instance
