#-*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.conf import settings

MONTH_LIST = (
    (1, ("3월")),
    (2, ("4월")),
    (3, ("6월")),
    (4, ("7월")),
    (5, ("9월")),
    (6, ("10월")),
)
GRADE_LIST=(
    ('고1','고1'),
    ('고2','고2'),
    ('고3','고3'),
)
class Search(models.Model):
    SEARCH_LIST = (
    ('선생님 이름','선생님 이름'),
    ('가격', '가격'),
    ('텍스트','텍스트'),
    ('제목','제목'),
    )
    search=models.CharField(max_length=20)
    search_what = models.CharField(max_length=6, choices=SEARCH_LIST, default='선생님 이름')


class Post(models.Model):
    SUBJECT_LIST = (
    ('국어', '국어'),
    ('수학(가)', '수학(가)'),
    ('수학(나)', '수학(나)'),
    ('영어', '영어'),
    ('한국사', '한국사'),
    ('사회','사회'),
    ('과학','과학'),
    ('제2외국어_한문','제2외국어_한문'),
    )
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    subject = models.CharField(
        max_length=10, choices=SUBJECT_LIST, default='국어')
    teacherName = models.CharField(max_length=10)
    price = models.IntegerField(
        validators=[MinValueValidator(50000), MaxValueValidator(100000000)])
    grade= models.CharField(max_length=6, choices=GRADE_LIST, default='고1')
    url = models.URLField()
    text = models.TextField()
    like = models.IntegerField(default=0)
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=20)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
    
class Grade(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    month = models.CharField(max_length=10)
    subject = models.CharField(max_length=10)
    grade = models.IntegerField(default=100, validators=[MaxValueValidator(100), MinValueValidator(1)])

    def get_user(self):
        return User.objects.get(pk=self.user_id)
