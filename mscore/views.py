from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from mscore.api.views import SpaceList, SpaceDetail
from mscore.forms import TaskForm, UserForm, SpaceForm, UserRegistrationForm
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


@login_required
def space_create(request):
    if request.method == 'POST':
        form = SpaceForm(request.POST)
        space_single = form.save(commit=False)
        space_single.owner = request.user
        space_single.save()
    else:
        form = SpaceForm()
    return render(request, 'mscore/form/base.html', {'form': form})


@login_required
def space_detail(request, pk):
    try:
        space_single = SpaceDetail(request=request).get_queryset().get(id=pk)
    except Space.DoesNotExist:
        raise Http404("Space does not exist")

    context = {'space': space_single}
    return render(request, 'mscore/space_detail.html', context)


@login_required
def space_constructor(request, pk):
    try:
        space_single = SpaceDetail(request=request).get_queryset().get(id=pk)
    except Space.DoesNotExist:
        raise Http404("Space does not exist")

    context = {'space': space_single }
    return render(request, 'mscore/space_constructor.html', context)


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
        return HttpResponseRedirect(reverse('space_detail', args=(pk,)))
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
        return HttpResponseRedirect(reverse('space_detail', args=(space_pk,)))
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
    return render(request, 'mscore/form/base.html', {'form': form})


@login_required
def user_change(request):
    user = request.user

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        form.save()
    else:
        form = UserForm(instance=user)
    return render(request, 'mscore/form/base.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})
