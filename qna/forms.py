from django import forms
from .models import Question, Answer, Tag


class QuestionForm(forms.ModelForm):
    categories = forms.MultipleChoiceField(
                    required=False,
                    widget=forms.CheckboxSelectMultiple,
                    choices=Tag.TAG_CHOICES)

    class Meta:
        model = Question
        fields = ['title', 'description', 'categories']


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['text']


class TagForm(forms.ModelForm):
    topic = forms.MultipleChoiceField(
                    required=False,
                    widget=forms.CheckboxSelectMultiple,
                    choices=Tag.TAG_CHOICES)

    class Meta:
        model = Tag
        fields = ('__all__')
