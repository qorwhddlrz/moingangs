#-*- coding: utf-8 -*-

from django import forms
from .models import Post, Comment,Search,Grade
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User #
from django.core.exceptions import ValidationError #

MONTH_LIST = (
    (1, ("3월")),
    (2, ("4월")),
    (3, ("6월")),
    (4, ("7월")),
    (5, ("9월")),
    (6, ("10월")),
)
SUBJECT_LIST = (
    (1, '국어'),
    (2, '수학(가)'),
    (3, '수학(나)'),
    (4, '영어'),
    (5, '한국사'),
)

MONTH_LIST_VALUE = ('3월', '4월', '6월', '7월', '9월', '10월')
SUBJECT_LIST_VALUE = ('국어', '수학(가)', '수학(나)', '영어', '한국사')


class SearchForm(forms.ModelForm):
    class Meta:
        model= Search
        fields=('search','search_what',)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','teacherName','price','grade','subject','url','text',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)

class CustomUserCreationForm(forms.Form): #
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username) #기존과 같은 이름있는지 검사
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2: #서로 유효하고 같은지 확인
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True): #유저에 저장한후 Return
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user
    
class GradeForm(forms.Form):
    month = forms.ChoiceField(choices=MONTH_LIST, label="월", initial="", widget=forms.Select(), required=True)
    subject = forms.ChoiceField(choices=SUBJECT_LIST, label="과목", initial="", widget=forms.Select(), required=True)
    grade = forms.IntegerField(initial=100, label="성적")

    def save(self, commit=True):
        grade = Grade(
            month = MONTH_LIST_VALUE[int(self.cleaned_data['month'])-1],
            subject = SUBJECT_LIST_VALUE[int(self.cleaned_data['subject'])-1],
            grade=self.cleaned_data['grade']
        )
        if commit:
            grade.save()
        return grade
