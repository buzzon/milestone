from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate

from user_manager.forms import UserSignUpForm, UserSignInForm, UserForm


def sign_up(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            login(request, new_user)
            return redirect('mscore:index')
    else:
        form = UserSignUpForm()
    return render(request, 'user_manager/sign_up.html', {'form': form})


def sign_in(request):
    if request.method == 'POST':
        form = UserSignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('mscore:index')
    else:
        form = UserSignInForm()
    return render(request, 'user_manager/sign_in.html', {'form': form})


@login_required
def sign_out(request):
    logout(request)
    return redirect('mscore:index')


@login_required
def user_update(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid:
            form.save()
            return redirect('mscore:index')
    else:
        form = UserForm(instance=request.user)
    return render(request, 'user_manager/user_update.html', {'form': form})
