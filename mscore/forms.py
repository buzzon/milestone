from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm

from mscore.models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        exclude = ['space']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }