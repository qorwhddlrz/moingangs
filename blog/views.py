from django.shortcuts import render, redirect, get_object_or_404 
from django.utils import timezone
from .models import Post, Comment, Search, Grade
from .forms import PostForm, CommentForm, SearchForm, GradeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages#
from django.contrib.auth.forms import UserCreationForm#
from django.http import HttpResponseRedirect
from django.db.models import Q

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts })


def post_searchpage(request):
    if request.method == "POST":
        form=SearchForm(request.POST)
        if form.is_valid():
            Search_Form=form.save(commit=False)
            Search_Form.save()
            return redirect('post_search',pk=Search_Form.pk)
    else:
        form=SearchForm()
    return render(request, 'blog/post_search.html', {'form':form})

def post_search(request,pk):
    Find=get_object_or_404(Search, pk=pk)
    posts=Post.objects.all()
    if Find.search_what=="선생님 이름":
        posts = Post.objects.filter(teacherName__contains=Find.search).order_by('created_date')
    elif Find.search_what=="가격":
        if not Find.search.isdigit():
            messages.warning(request, 'Please enter int.')
            return redirect('post_list')
        posts = Post.objects.filter(price__lte=Find.search).order_by('created_date')
    elif Find.search_what=="텍스트":
        posts = Post.objects.filter(text__contains=Find.search).order_by('created_date')
    elif Find.search_what=="제목":
        posts = Post.objects.filter(title__contains=Find.search).order_by('created_date')

    if request.method == "POST":
        form=SearchForm(request.POST)
        if form.is_valid():
            Search_Form=form.save(commit=False)
            Search_Form.save()
            return redirect('post_search',pk=Search_Form.pk)
    else:
        form=SearchForm()
    return render(request,'blog/post_search.html',{'form':form,'Find': Find ,'posts':posts})

def post_list_search(request,post_grade=None,name=None):#
    posts=Post.objects.all()
    if request.method == "POST":
        form=SearchForm(request.POST)
        if form.is_valid():
            Search_Form=form.save(commit=False)
            Search_Form.save()
            return redirect('post_search',pk=Search_Form.pk)
    else:
        form=SearchForm()
    posts = Post.objects.filter(grade=post_grade)
    if(name!=None and post_grade!=None):
        for SUBJECT_NAME,KEY in Post.SUBJECT_LIST:
            if SUBJECT_NAME==name:
                posts = Post.objects.filter(subject=SUBJECT_NAME).filter(grade=post_grade).order_by('created_date')
            elif name=="수학" and SUBJECT_NAME=="수학(가)":
                criterion1 = Q(subject="수학(가)")
                criterion2 = Q(subject="수학(나)")
                posts = Post.objects.filter(criterion1 | criterion2).filter(grade=post_grade).order_by('created_date')
    return render(request, 'blog/post_list.html', {'posts': posts , 'form':form ,'post_grade':post_grade,'name':name})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author=request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


def register(request):#
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    else:
        f = UserCreationForm()

    return render(request, 'registration/register.html', {'form': f})

@login_required
def add_grade_info(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)

        if form.is_valid():
            grade = form.save(commit=False)
            grade.user = request.user
            grade.save()
            return redirect('grade_detail', pk=grade.pk)
    else:
        form = GradeForm()

    return render(request, 'blog/grade.html', {'form': form})


@login_required
def grade_detail(request, pk):
    grades = get_object_or_404(Grade, pk=pk)
    return render(request, 'blog/grade_detail.html', { 'grades': grades })

@login_required
def grade_list(request):
    grades = Grade.objects.filter(user=request.user)
    return render(request, 'blog/grade_list.html', { 'grades': grades })
