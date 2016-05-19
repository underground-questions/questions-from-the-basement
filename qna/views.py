from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from .forms import QuestionForm, AnswerForm, TagForm
from .models import Question, Answer, Owner
from django.db.models import Count


def index(request):
    recent_question = Question.objects.order_by('-created')[:5]
    form = QuestionForm()
    context = {'recent_question': recent_question, 'form': form}
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
    answers.order_by('-votes')
    context['answers'] = answers

    form = AnswerForm()
    context['form'] = form
    return render(request, 'qna/question.html', context)


def profile(request, pk):
    context = {}

    owner = Owner.objects.get(id=pk)
    context['owner'] = owner

    if request.method == "POST":
        q_form = QuestionForm(request.POST)
        tags = request.POST.getlist('topic')
        print(tags)
        Question.handle_form(owner, q_form)

    questions = Question.objects.filter(owner=owner)
    context['questions'] = questions

    context['q_form'] = QuestionForm()
    context['t_form'] = TagForm()
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
