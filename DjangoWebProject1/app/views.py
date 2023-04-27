"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .forms import AnketaForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.db import models
from .models import Comment # использование модели комментариев
from .forms import CommentForm # использование формы ввода комментария
from .models import Blog
from .forms import BlogForm
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Домашняя страница',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
def links(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
    )

def anketa(request):
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Мужчина', '2': 'Женщина'}
    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data=dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['gender'] = gender[ form.cleaned_data['gender'] ]
            if (form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['message'] = form.cleaned_data['message']
            data['email'] = form.cleaned_data['email']
            form = None
    else:
        form = AnketaForm()
    return render(
        request,
        'app/anketa.html',
        {
            'form':form,
            'data':data,
        }
    )

def registration(request):
    assert isinstance(request, HttpRequest)
    if request.method == "POST": #после отправки формы
        regform = UserCreationForm (request.POST)
        if regform.is_valid(): #Валидация последней формы
            reg_f = regform.save(commit=False) #Не сохранять автоматически данные формы
            reg_f.is_staff = False # Запрет на вход в админ-раздел
            reg_f.is_active = True # Активный юзер
            reg_f.is_superuser = False # Не является суперюзером
            reg_f.date_joined = datetime.now() # Дата регистрации
            reg_f.last_login = datetime.now() # Дата последней авторизации
            reg_f.save() # Сохранить изменения после добавления данных
            return redirect('home') # Переадресация на гл. страницу
    else:
        regform = UserCreationForm() #Создание объекта формы для ввода данных нового юзера
    
    return render (
        request,
        'app/registration.html',
        {
            'regform':regform, #Передача формы в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )

def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr)
    if request.method == "POST": # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
            comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save() # сохраняем изменения после добавления полей
            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария
    else:
        form = CommentForm() # создание формы для ввода комментария
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1, # передача конкретной статьи в шаблон веб-страницы
            'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
            'form': form, # передача формы добавления комментария в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )

def blog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all() # запрос на выбор всех статей блога из модели
    return render(
        request, 
        'app/blog.html',
        {
            'title':'Блог',
            'posts': posts, # передача списка статей в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )

def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.autor = request.user
            blog_f.save()

            return redirect('blog')
    else:
        blogform = BlogForm()

    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Добавить статью блога',

            'year':datetime.now().year,
        }
    )
def videopost(request):
    """Renders the videopost page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'message':'Сведения о нас.',
            'year':datetime.now().year,
        }
    )