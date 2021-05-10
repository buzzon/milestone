import calendar
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView

from mscore.api.views import SpaceList, SpaceDetail
from mscore.forms import TaskForm
from mscore.models import Space, Task


def index(request):
    context = {'user': request.user}
    return render(request, 'mscore/index.html', context)


@login_required
def space(request):
    space_data = SpaceList(request=request).get_queryset()
    context = {'space_data': space_data,
               'user': request.user}
    return render(request, 'mscore/space_list.html', context)


class SpaceCreate(CreateView):
    model = Space
    fields = '__all__'

    def get_form_kwargs(self):
        kwargs = super(SpaceCreate, self).get_form_kwargs()
        if kwargs['instance'] is None:
            kwargs['instance'] = Space()
        kwargs['instance'].owner = self.request.user
        return kwargs


@login_required
def space_detail(request, pk):
    try:
        space_single = SpaceDetail(request=request).get_queryset().get(id=pk)
    except Space.DoesNotExist:
        raise Http404("Space does not exist")

    c = calendar.HTMLCalendar()
    html_out = c.formatmonth(datetime.today().year, datetime.today().month)

    context = {'space_single': space_single,
               'user': request.user,
               'html_out': html_out}
    return render(request, 'mscore/space_detail.html', context)


def task_create(request, pk):
    try:
        space_single = SpaceDetail(request=request).get_queryset().get(id=pk)
    except Space.DoesNotExist:
        raise Http404("Space does not exist")

    if request.method == 'POST':
        form = TaskForm(request.POST)
        task = form.save(commit=False)
        task.space = space_single
        task.save()
        return HttpResponseRedirect(reverse('space-detail', args=(pk,)))
    else:
        form = TaskForm()
    return render(request, 'mscore/form/base.html', {'form': form})
