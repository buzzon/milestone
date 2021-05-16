from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView

from mscore.api.views import SpaceList, SpaceDetail
from mscore.forms import TaskForm, UserForm, SpaceForm
from mscore.models import Space, Task
from mscore.utilities.date_list import get_time_list


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

    date_list = get_time_list(4, 16)

    context = {'space': space_single, 'date_list': date_list}
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
        return HttpResponseRedirect(reverse('space_detail', args=(pk,)))
    else:
        form = TaskForm()
    return render(request, 'mscore/form/base.html', {'form': form})


def task_change(request, space_pk, task_pk):
    try:
        task = Task.objects.get(pk=task_pk)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        form.save()
        return HttpResponseRedirect(reverse('space_detail', args=(space_pk,)))
    else:
        form = TaskForm(instance=task)
    return render(request, 'mscore/form/base.html', {'form': form})


def space_edit(request, pk):
    try:
        space_single = Space.objects.get(pk=pk)
    except Space.DoesNotExist:
        raise Http404("Space does not exist")

    if request.method == 'POST':
        form = SpaceForm(request.POST, instance=space_single)
        form.save()
    else:
        form = SpaceForm(instance=space_single)
    return render(request, 'mscore/form/base.html', {'form': form})


def user_change(request):
    user = request.user

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        form.save()
    else:
        form = UserForm(instance=user)
    return render(request, 'mscore/form/base.html', {'form': form})
