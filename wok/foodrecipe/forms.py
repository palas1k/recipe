from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory
from .models import *


# class AddPost(forms.ModelForm):
#     # def __init__(self):
#     #     super().__init__()
#     #     self.fields['type'].empty_label = 'Не выбрано'
#     class Meta:
#         model = Post
#         fields = ['title', 'content', 'ingredients', 'type']
#         widgets = {
#             'title':forms.TextInput(attrs={'class': 'form-input'}),
#             'content':forms.TextInput(attrs={'cols': 100, 'rows':20}),
#         }
#
class AddContent(forms.ModelForm):
    class Meta:
        model = PostContent
        fields = ['text', 'image']


PostFormset = inlineformset_factory(Post, PostContent, formset=BaseInlineFormSet, extra=2, fields= ['text', 'image'])
PostFormset.save()