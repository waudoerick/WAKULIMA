from django import forms

from .models import *

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['text']
        label = {'text': ''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': 'Entry:'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
class WakulimaForm(forms.ModelForm):
    class Meta:
        model = Wakulima
        fields ='__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

class ContactForm(forms.ModelForm):
    class Meta:
        fields ='__all__'
        

