from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
from django.urls import reverse

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    is_login = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

class chatMessages(models.Model):
    user_from = models.ForeignKey(User,
        on_delete=models.CASCADE,related_name="sent")
    user_to = models.ForeignKey(User,
        on_delete=models.CASCADE,related_name="received")
    message = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    correspondents = models.ForeignKey(User,
        on_delete=models.CASCADE,related_name="correspondents", null=True)

    def __str__(self):
        return self.message




class UploadFile(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,related_name='file_created' ,verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Заголовок',blank=True)
    # uploadedfile = models.FileField(upload_to='files/',null=True, verbose_name='Файл')
    description = models.TextField(blank=True, verbose_name='Описание')
    createdtime = models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена')
    number_course = models.IntegerField(null=True, blank=True, verbose_name='Курс')
    number_semestr = models.IntegerField(null=True, blank=True, verbose_name='Семестр')
    subjectt = models.CharField(max_length=200, null=True,blank=True,verbose_name='Предмет')
    type_materials = models.CharField(max_length=200,null=True,blank=True, verbose_name='Тип работы')
    institute = models.CharField(max_length=200, null=True,blank=True, verbose_name='Институт')
    # default_UploadedFile = models.ForeignKey('Writehelp', related_name='+')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Загрузка файла'
        verbose_name_plural = 'Загрузка файлов'

class FeedFile(models.Model):
    file = models.FileField(upload_to="files/")
    feed = models.ForeignKey(UploadFile, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Файлы документа'
        verbose_name_plural = 'Файлы документов'

    def get_absolute_url(self):
        return reverse('file',kwargs={'file_id':self.pk})

class Writehelp(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,related_name='helped_user' ,verbose_name='Автор')
    titles = models.CharField(max_length=200, verbose_name='Заголовок', blank=True, null=True)
    descriptions = models.TextField(blank=True, verbose_name='Описание', null=True)
    createdtimes = models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
    prices = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена')
    course = models.IntegerField(null=True, blank=True, verbose_name='Курс')
    semestr = models.IntegerField(null=True, blank=True, verbose_name='Семестр')
    subjects = models.CharField(max_length=200, null=True, blank=True, verbose_name='Предмет')
    institutes = models.CharField(max_length=200, null=True, blank=True, verbose_name='Институт')
    time = models.TimeField(null=True)
    date = models.DateField(null=True)



    def __str__(self):
        return self.titles

    class Meta:
        verbose_name = 'Просьба о помощи'
        verbose_name_plural = 'Просьбы о помощи'

class WhiteHelpFile(models.Model):
    file= models.FileField(upload_to="files/writehelp/")
    feed = models.ForeignKey(Writehelp, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Файлы для помощника'
        verbose_name_plural = 'Файлы для помощников'

    def get_absolute_url(self):
        return reverse('help',kwargs={'help_id':self.pk})