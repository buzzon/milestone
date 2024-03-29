import pytz
from django.http import JsonResponse
from django.template.loader import render_to_string
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.reverse import reverse

from mscore.api.serializers import *


@api_view(['GET'])
@permission_classes([IsAdminUser])
def api_root(request, format=None):
    return Response({
        'spaces': reverse('mscore_api:space-list', request=request, format=format),
        # 'tasks': reverse('mscore_api:task-list', request=request, format=format),
    })


@permission_classes([IsAdminUser])
class SpaceList(generics.ListCreateAPIView):
    serializer_class = SpaceSerializer
    model = Space


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        owned_spaces = Space.objects.filter(owner=self.request.user)
        membered_spaces = Space.objects.filter(members=self.request.user)
        return (membered_spaces | owned_spaces).distinct()


def space_tasks(request, pk):
    data = dict()
    if request.method == 'GET':
        tasks = Space.objects.get(pk=pk).tasks.filter(is_nested=False)
        data['tasks'] = render_to_string('mscore/parts/gantt_tasks.html', {'tasks': tasks}, request=request)
    return JsonResponse(data)


@permission_classes([IsAuthenticated])
class SpaceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SpaceSerializer
    model = Space

    def get_queryset(self):
        owned_spaces = Space.objects.filter(owner=self.request.user)
        membered_spaces = Space.objects.filter(members=self.request.user)
        return (membered_spaces | owned_spaces).distinct()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_time_period(request):
    if request.method == 'GET':
        space = request.GET['space_id']
        first_date = datetime.strptime(request.GET['first_date'], "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=pytz.UTC)
        last_date = datetime.strptime(request.GET['last_date'], "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=pytz.UTC)
        tasks = Task.objects.filter(space=space).filter(is_nested=False, initial_date__range=[first_date, last_date])
        return Response({'task': TaskSerializer(tasks, many=True).data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_change(request):
    if request.method == 'POST':
        task = Task.objects.filter(space=request.POST['space_id']).get(pk=request.POST['pk'])
        task.title = request.POST['title']
        task.save()
        return Response({'task': TaskSerializer(task).data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_create(request):
    if request.method == 'POST':
        space_single = Space.objects.get(pk=request.POST['space_id'])
        is_nested = request.POST['is_nested']
        if request.POST.get('pk', None) is None:
            new_task = Task(space=space_single)
        else:
            task = Task.objects.filter(space=request.POST['space_id']).get(pk=request.POST['pk'])
            if is_nested == '1':
                new_task = Task(space=space_single, parent=task, is_nested=True)
            else:
                new_task = Task(space=space_single, parent=task.parent, is_nested=task.parent is not None)
        new_task.save()
        return Response({'task': TaskSerializer(new_task).data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_delete(request):
    if request.method == 'POST':
        task = Task.objects.filter(space=request.POST['space_id']).get(pk=request.POST['pk'])
        task.delete()
        return Response({'task': 'deleted'})
