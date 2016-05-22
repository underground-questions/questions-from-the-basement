from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView
from rest_framework import viewsets
from .forms import QuestionForm, AnswerForm
from .models import Question, Answer, Owner, Tag
from .serializers import QuestionSerializer, AnswerSerializer
from .serializers import OwnerSerializer, TagSerializer, UserSerializer


class QuestionsViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('created')
    serializer_class = QuestionSerializer


class AnswersViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all().order_by('-votes')
    serializer_class = AnswerSerializer


class OwnersViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def index(request):
    sort_by = request.GET.get('sort_by')
    if sort_by == 'popular':
        sort = 'Most Answered'
        paginator = get_popular_questions(15)
    else:
        sort = 'Most Recent'
        paginator = get_recent_questions(15)

    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        questions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        questions = paginator.page(paginator.num_pages)
    form = QuestionForm()
    context = {'questions': questions, 'form': form, 'sort': sort}
    return render(request, 'qna/index.html', context)


def get_recent_questions(count):
    questions = Question.objects.order_by('-created')
    return Paginator(questions, count)


def get_popular_questions(count):
    sql = '''
        SELECT q.*
        FROM qna_question q
        JOIN qna_answer a
            ON a.question_id = q.id
        GROUP BY q.id
        ORDER BY count(1) DESC
    '''
    questions = Question.objects.raw(sql)
    paginator = Paginator(questions, count)
    paginator._count = len(list(questions))
    return paginator


def get_most_voted_question(count):
    sql = '''
        SELECT q.*
        FROM qna_question q
        JOIN qna_answer a
            ON a.question_id = q.id
        JOIN q
    '''
    pass


def question_detail(request, pk):
    context = {}

    question = Question.objects.get(id=pk)
    context['question'] = question

    if request.method == "POST":
        form = AnswerForm(request.POST)
        vote = request.POST.get('vote', False)
        if vote == 'upvote':
            answer = Answer.objects.get(pk=request.POST['answer_object'])
            answer.voter = request.user
            answer.save()
            answer.votes += 1
            answer.save()
            answer.owner.score += 10
            answer.owner.save()
        elif vote == 'downvote':
            answer = Answer.objects.get(pk=request.POST['answer_object'])
            answer.voter = request.user
            answer.save()
            answer.votes -= 1
            answer.save()
            answer.owner.score -= 5
            answer.owner.save()
            request.user.owner.score -= 1
            request.user.owner.save()
        elif form.is_valid():
            answer = form.save(commit=False)
            answer.owner = request.user.owner
            answer.question = question
            answer.save()
        else:
            print(form.errors)

    answers = Answer.objects.filter(question=question)
    answers = answers.order_by('-votes')
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
        Question.handle_form(owner, form)

    questions = Question.objects.filter(owner=owner)
    questions = questions.order_by('-created')
    context['questions'] = questions

    context['form'] = QuestionForm()
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
