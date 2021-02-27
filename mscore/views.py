from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from mscore.api.views import SpaceList


def index(request):
    return render(request, 'mscore/index.html')


@login_required
def space(request):
    space_data = SpaceList(request=request).get_queryset()
    context = {'space_data': space_data}
    return render(request, 'mscore/space.html', context)
