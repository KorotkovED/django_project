from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    is_login = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

class chatMessages(models.Model):
    user_from = models.ForeignKey(User,
        on_delete=models.CASCADE,related_name="+")
    user_to = models.ForeignKey(User,
        on_delete=models.CASCADE,related_name="+")
    message = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message


class UploadFile(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,related_name='file_created' ,verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    # uploadedfile = models.FileField(upload_to='files/',null=True, verbose_name='Файл')
    description = models.TextField(blank=True, verbose_name='Описание')
    createdtime = models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена')
    number_course = models.IntegerField(null=True, blank=True, verbose_name='Курс')
    number_semestr = models.IntegerField(null=True, blank=True, verbose_name='Семестр')
    subjectt = models.CharField(max_length=200, null=True,verbose_name='Предмет')
    type_materials = models.CharField(max_length=200,null=True, verbose_name='Тип работы')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Загрузка файла'
        verbose_name_plural = 'Загрузка файлов'

class FeedFile(models.Model):
    file = models.FileField(upload_to="files/")
    feed = models.ForeignKey(UploadFile, on_delete=models.CASCADE)