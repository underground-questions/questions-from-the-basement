from django import forms
from .models import Question, Answer


class QuestionForm(forms.ModelForm):
    TAG_CHOICES = (('SQL', 'SQL'), ('Java', 'Java'), ('Python', 'Python'),
                   ('Javascript', 'Javascript'), ('Django', 'Django'),
                   ('C++', 'C++'), ('Ruby', 'Ruby'), ('PHP', 'PHP'))

    categories = forms.MultipleChoiceField(
        required=False, widget=forms.CheckboxSelectMultiple,
        choices=TAG_CHOICES)

    class Meta:
        model = Question
        fields = ['title', 'description', 'categories']


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['text']
