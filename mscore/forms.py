from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS
from django import forms

from mscore.models import Task, Space
from bootstrap_modal_forms.forms import BSModalModelForm


class TaskForm(BSModalModelForm):
    class Meta:
        model = Task
        exclude = ['parent', 'space', 'is_nested']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }


class SpaceForm(BSModalModelForm):
    class Meta:
        model = Space
        fields = ['title', 'members']

    members = forms.ModelMultipleChoiceField(
        required=False,
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


