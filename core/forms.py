from django import forms
from .models import List
from django.contrib.auth.models import User

class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['title', 'description', 'user']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ListForm, self).__init__(*args, **kwargs)

        self.fields['title'].label = 'Title'
        self.fields['description'].label = 'Description'


        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Title',
        })

        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Description',
        })


        if user and user.is_superuser:
            self.fields['user'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Username',
            })
        else:
            self.fields['user'].initial = user
            self.fields['user'].widget = forms.HiddenInput()
