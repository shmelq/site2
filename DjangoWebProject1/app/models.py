"""
Definition of models.
"""

from tabnanny import verbose
from django.db import models
from django.contrib import admin
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length= 100, unique_for_date= "posted", verbose_name="Заголовок")
    description = models.TextField(verbose_name= "Краткое содержание")
    content = models.TextField(verbose_name= "Полное содержание")
    posted = models.DateTimeField(default= datetime.now(), db_index= True, verbose_name= "Опубликована")
    image = models.FileField(default= 'temp.jpg', verbose_name = "Путь к картине")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    #Методы класса
    def get_absolute_url(self): #Метод возвращает строку с URL-адресом записи
        return reverse("blogpost", args=[str(self.id)])
    def __str__(self): #Метод возвращает название для представления отдельных записей в адм. разделе
        return self.title
    #Метаданные- вложенный класс, который задает доп. параметры модели:
    class Meta:
        db_table = "Posts" #Имя таблицы для модели
        ordering = ["-posted"] #Порядок сортировки данных в модели
        verbose_name = "Статья блога" #Имя, под которым модель будет отобр. в адм. разделе
        verbose_name_plural = "Статьи блога" #То же для всех статей блога
admin.site.register(Blog)
posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликована")

class Comment(models.Model):
    text = models.TextField(verbose_name = "Текст комментария")
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата комментария")
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Статья удалена")
    post = models.ForeignKey(Blog, on_delete = models.CASCADE, verbose_name = "Статья комментария")
    #Методы класса
    def __str__(self):
        return 'Комментарий %d %s к %s' % (self.id, self.author, self.post)
    class Meta:
        db_table = "Comment"
        ordering = ["-date"]
        verbose_name = "Комментарий к статье блога"
        verbose_name_plural = "Комментарии к статьям блога"
admin.site.register(Comment)

