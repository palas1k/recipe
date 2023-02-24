from django import forms
from .models import *
from django.forms.models import inlineformset_factory

# class AddPost(forms.ModelForm):
#     # def __init__(self):
#     #     super().__init__()
#     #     self.fields['type'].empty_label = 'Не выбрано'
#     class Meta:
#         model = Post
#         fields = ['title', 'content', 'image', 'ingredients', 'type']
#         widgets = {
#             'title':forms.TextInput(attrs={'class': 'form-input'}),
#             'content':forms.TextInput(attrs={'cols': 100, 'rows':20}),
#         }

# class AddPost(forms.ModelForm):
#     class Meta:
#         model = PostContent
#         fields = ['stage1','stage2','stage3','stage4','stage5',]

class AddPost