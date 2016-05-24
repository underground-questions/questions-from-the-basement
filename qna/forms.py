from django import forms
from .models import Question, Answer, Tag


class QuestionForm(forms.ModelForm):
    categories = forms.MultipleChoiceField(
                    required=False,
                    widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Question
        fields = ['title', 'description', 'categories']


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['text']
