from django import forms
from .models import *

class AddPost(forms.ModelForm):
    # def __init__(self):
    #     super().__init__()
    #     self.fields['type'].empty_label = 'Не выбрано'
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'ingredients', 'type']
        widgets = {
            'title':forms.TextInput(attrs={'class': 'form-input'}),
            'content':forms.TextInput(attrs={'cols': 100, 'rows':20}),
        }
