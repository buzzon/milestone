from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from mscore.api.views import SpaceList, SpaceDetail
from mscore.forms import TaskForm, SpaceForm
from mscore.models import Space, Task


def index(request):
    user = request.user
    spaces = []
    progress_tasks = Task.objects.none()
    if user.is_authenticated:
        spaces = SpaceList(request=request).get_queryset()
        progress_tasks_list = [sp.tasks.filter(status="P") for sp in spaces]
        for task in progress_tasks_list:
            progress_tasks = progress_tasks.union(task)
        if progress_tasks.count() > 0:
            progress_tasks = progress_tasks.order_by('deadline')
    return render(request, 'mscore/index.html', {'user': user, 'spaces': spaces, 'progress_tasks': progress_tasks})


# @login_required
# def space_create(request):
#     if request.method == 'POST':
#         form = SpaceForm(request.POST)
#         space_single = form.save(commit=False)
#         space_single.owner = request.user
#         space_single.save()
#     else:
#         form = SpaceForm()
#         form.declared_fields['members'].queryset = form.declared_fields['members'].choices.queryset.exclude(pk=request.user.id)
#     return render(request, 'mscore/form/base.html', {'form': form})


class SpaceCreateView(BSModalCreateView):
    template_name = 'mscore/form/create_space.html'
    form_class = SpaceForm
    success_message = 'Success: Space was created.'
    success_url = reverse_lazy('mscore:index')

    def form_valid(self, form):
        if not self.request.is_ajax():
            space_single = form.save(commit=False)
            space_single.owner = self.request.user
            space_single.save()
        return HttpResponseRedirect(self.success_url)


class TaskUpdateView(BSModalUpdateView):
    model = Task
    template_name = 'mscore/form/update_task.html'
    form_class = TaskForm
    success_message = 'Success: Task was updated.'
    success_url = reverse_lazy('mscore:index')


def space_task_list(request, pk):
    data = dict()
    return JsonResponse(data)


@login_required
def space_gantt(request, pk):
    try:
        space_single = SpaceDetail(request=request).get_queryset().get(id=pk)
    except Space.DoesNotExist:
        raise Http404("Space does not exist")
    return render(request, 'mscore/space_gantt.html', {'space': space_single})


@login_required
def space_constructor(request, pk):
    try:
        space_single = SpaceDetail(request=request).get_queryset().get(id=pk)
    except Space.DoesNotExist:
        raise Http404("Space does not exist")
    return render(request, 'mscore/space_constructor.html', {'space': space_single})


@login_required
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
        return HttpResponseRedirect(reverse('mscore:space_detail', args=(pk,)))
    else:
        form = TaskForm()
    return render(request, 'mscore/form/base.html', {'form': form})


@login_required
def task_nested_create(request, space_pk, task_pk):
    try:
        space_single = SpaceDetail(request=request).get_queryset().get(id=space_pk)
        task_single = space_single.tasks.get(pk=task_pk)
    except Space.DoesNotExist:
        raise Http404("Space does not exist")
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    if request.method == 'POST':
        form = TaskForm(request.POST)
        task = form.save(commit=False)
        task.space = space_single
        task.parent = task_single
        task.is_nested = True
        task.save()

        return HttpResponseRedirect(reverse('mscore:space_detail', args=(space_pk,)))
    else:
        form = TaskForm()
    return render(request, 'mscore/form/base.html', {'form': form})


@login_required
def task_change(request, space_pk, task_pk):
    try:
        task = Task.objects.get(pk=task_pk)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        form.save()
        return HttpResponseRedirect(reverse('mscore:space_detail', args=(space_pk,)))
    else:
        form = TaskForm(instance=task)
    return render(request, 'mscore/form/base.html', {'form': form})


@login_required
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
        form.declared_fields['members'].queryset = form.declared_fields['members'].choices.queryset.exclude(
            pk=request.user.id)
    return render(request, 'mscore/form/base.html', {'form': form})
