from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS
from django import forms

from mscore.models import Task, Space


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['parent', 'space', 'is_nested']
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


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
