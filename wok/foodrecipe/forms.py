from django import forms
from .models import *

class AddPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
