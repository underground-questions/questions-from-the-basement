from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from .forms import QuestionForm, AnswerForm
from .models import Question, Answer, Owner
from django.db.models import Count


def index(request):
    recent_question = Question.objects.order_by('-created')[:5]
    context = {'recent_question': recent_question}
    return render(request, 'qna/index.html', context)


def question_detail(request, pk):
    context = {}

    question = Question.objects.get(id=pk)
    context['question'] = question

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.owner = request.user.owner
            answer.question = question
            answer.save()
        else:
            print(form.errors)

    answers = Answer.objects.filter(question=question)
    context['answers'] = answers

    form = AnswerForm()
    context['form'] = form
    return render(request, 'qna/question.html', context)


def profile(request, pk):
    context = {}

    owner = Owner.objects.get(id=pk)
    context['owner'] = owner

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.owner = owner
            question.save()
            owner.score += 5
            owner.save()
        else:
            print(form.errors)

    questions = Question.objects.filter(owner=owner)
    context['questions'] = questions

    form = QuestionForm()
    context['form'] = form
    return render(request, 'qna/profile.html', context)


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
