from django import forms
from .models import PlayList


class AddToPlayListForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(AddToPlayListForm, self).__init__(*args, **kwargs)
        self.fields['playlist'].queryset = PlayList.objects.filter(user=user)

    playlist = forms.ModelChoiceField(
        queryset=None,
        empty_label = 'Select a playlist',
        widget = forms.Select(attrs={
            'class': 'form-control',
        }),
        label = '',
    )