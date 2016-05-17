from django.shortcuts import render
from django.http import HttpResponse
from .models import Question, Answer, Owner

def index(request):
    return render(request, 'qna/index.html')


def question_detail(request, pk):
    question = Question.objects.get(id=pk)
    return render(request, 'qna/question.html', context={'question': question})


def profile(request, pk):
    owner = Owner.objects.get(id=pk)
    return render(request, 'qna/profile.html', context={'owner': owner})
