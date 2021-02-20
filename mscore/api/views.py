from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from mscore.models import *
from mscore.api.serializers import *


@csrf_exempt
def space_list(request):
    if request.method == 'GET':
        spaces = Space.objects.all()
        serializer = SpaceSerializer(spaces, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SpaceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.data, status=400)


@csrf_exempt
def space_detail(request, pk):
    try:
        space = Space.objects.get(pk=pk)
    except Space.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SpaceSerializer(space)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SpaceSerializer(space, data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.data, status=400)

    elif request.method == 'DELETE':
        space.delete()
        return HttpResponse(status=204)
