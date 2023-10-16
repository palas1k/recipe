import requests
from django import forms
from django.forms import modelformset_factory, BaseModelFormSet, formset_factory, ModelForm, inlineformset_factory
from django.shortcuts import render

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
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
PostContentFormset = inlineformset_factory(Post, PostContent, fields= ('text','image'), extra= 3, can_delete= False)
