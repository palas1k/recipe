import requests
from django import forms
from django.forms import modelformset_factory, BaseModelFormSet, formset_factory, ModelForm
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
class AddContent(ModelForm):
    class Meta:
        model = PostContent
        fields = ['text', 'image']
def get_formset(request):
    PostFormset = modelformset_factory(model=PostContent, form=AddContent, extra=10, fields=('text', 'image'))
    formset = ''
    if request.method == 'POST':
        formset = PostFormset(request.POST, request.FILES)
        if formset.is_valid():
            # formset = PostFormset.save(commit=False)
            formset = PostFormset.save()
        else:
            formset = PostFormset()
    return render(request, 'foodrecipe/addpage.html', {'formset': formset, 'PostContent': PostContent})
