# Create Forms for Note Input and Questions
from django import forms
from .models import Notes

class NoteForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'content']

class QuestionForm(forms.Form):
    question = forms.CharField(label='Ask something', max_length=500)
