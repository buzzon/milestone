from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS
from django import forms

from mscore.models import Task, Space


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['space']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class SpaceForm(forms.ModelForm):
    class Meta:
        model = Space
        # exclude = ['tasks']
        fields = ['title', 'members']

    members = forms.ModelMultipleChoiceField(
        required=False,
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
