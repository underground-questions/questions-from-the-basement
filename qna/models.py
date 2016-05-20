from django.db import models
from django.contrib.auth.models import User

class Answer(models.Model):
    text = models.TextField()
    votes = models.IntegerField(default=0)
    owner = models.ForeignKey('Owner', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    owner = models.ForeignKey('Owner', on_delete=models.CASCADE)
    categories = models.ManyToManyField('Tag')
    created = models.DateTimeField(auto_now_add=True)

    def handle_form(owner, form):
        if form.is_valid():
            tags = form['categories'].value()

            question = form.save(commit=False)
            question.owner = owner
            question.save()

            owner.score += 5
            owner.save()

            if tags:
                tag_objects = []
                for tag in tags:
                    t = Tag.objects.get_or_create(topic=tag)
                    tag_objects.append(t[0])

                question.categories = tag_objects
                question.save()

        else:
            print(q_form.errors)

class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    TAG_CHOICES = (('SQL', 'SQL'), ('Java', 'Java'), ('Python', 'Python'),
                   ('Javascript', 'Javascript'), ('Django', 'Django'),
                   ('C++', 'C++'), ('Ruby', 'Ruby'), ('PHP', 'PHP'))

    topic = models.CharField(max_length=25, choices=TAG_CHOICES)
