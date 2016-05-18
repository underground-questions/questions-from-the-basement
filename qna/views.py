from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from .models import Question, Answer, Owner

def index(request):
    return render(request, 'qna/index.html')


def question_detail(request, pk):
    question = Question.objects.get(id=pk)
    return render(request, 'qna/question.html', context={'question': question})


def profile(request, pk):
    owner = Owner.objects.get(id=pk)
    questions = Question.objects.filter(owner=owner.user)
    return render(request, 'qna/profile.html', context={'owner': owner, 'questions': questions})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            owner = Owner(user=user)
            owner.save()
            return HttpResponseRedirect('/login')
        else:
            print(form.errors)
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', context={'form': form})


def user_redirect(request):
    url = '/profile/{}/'.format(request.user.owner.id)
    return HttpResponseRedirect(url)
